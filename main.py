from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List

app = FastAPI()

GRADE_TO_POINT = {
    "A+": 4.5, "A": 4.0, "B+": 3.5, "B": 3.0,
    "C+": 2.5, "C": 2.0, "D+": 1.5, "D": 1.0, "F": 0.0
}

class Course(BaseModel):
    course_code: str
    course_name: str
    credits: int = Field(gt=0)
    grade: str

class StudentRequest(BaseModel):
    student_id: str
    name: str
    courses: List[Course]

@app.post("/score")
def calculate_gpa(data: StudentRequest):
    total_credits = sum(course.credits for course in data.courses)
    total_points = 0.0
    for course in data.courses:
        if course.grade not in GRADE_TO_POINT:
            raise HTTPException(status_code=400, detail=f"Invalid grade: {course.grade}")
        total_points += GRADE_TO_POINT[course.grade] * course.credits

    gpa = round(total_points / total_credits, 2)
    return {
        "student_summary": {
            "student_id": data.student_id,
            "name": data.name,
            "gpa": gpa,
            "total_credits": total_credits
        }
    }
