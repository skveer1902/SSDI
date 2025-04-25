# ✅ backend/app/routers/faculty.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Faculty, Student

router = APIRouter()

# Faculty can view a student's personal info
@router.get("/faculty/get_student_info/{student_id}")
def get_student_info(student_id: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id_number == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {
        "name": student.name,
        "email": student.email,
        "emergency_contact": student.emergency_contact,
        "personal_address": student.personal_address
    }

# Faculty can view a student's attendance (Mocked for now)
@router.get("/faculty/get_attendance/{student_id}")
def get_attendance(student_id: str):
    # Assume 90% attendance mock
    return {
        "student_id": student_id,
        "attendance_percentage": "90%"
    }

# Faculty can view a student's academic record (Mocked for now)
@router.get("/faculty/get_academic_record/{student_id}")
def get_academic_record(student_id: str):
    return {
        "student_id": student_id,
        "gpa": 3.2,  # Mock GPA
        "grades": {
            "AI Course": "A",
            "Software Engineering": "B+",
            "Database Systems": "A-"
        }
    }

# Faculty can view their own personal info (ProfileCard purpose)
@router.get("/faculty/get_info/{faculty_id}")
def get_faculty_info(faculty_id: str, db: Session = Depends(get_db)):
    faculty = db.query(Faculty).filter(Faculty.faculty_id == faculty_id).first()
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
    
    return {
        "name": faculty.name,
        "email": faculty.email,
        "department": faculty.department,
        "phone": faculty.phone,
        "designation": faculty.designation,
        "office": faculty.office
    }
