from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Faculty, Student, IDCard, AcademicCalendar

router = APIRouter()

# 1. Faculty view student personal + ID card info
@router.get("/faculty/get_student_info/{student_id}")
def get_student_info(student_id: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id_number == student_id).first()
    id_card = db.query(IDCard).filter(IDCard.student_id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return {
        "name": student.name,
        "email": student.email,
        "emergency_contact": student.emergency_contact,
        "personal_address": student.personal_address,
        "id_card": {
            "student_id": id_card.student_id if id_card else None,
            "issue_date": id_card.issue_date if id_card else None,
        }
    }

# 2. Faculty view student attendance (mocked attendance + academic calendar holidays)
@router.get("/faculty/get_student_attendance/{student_id}")
def get_attendance(student_id: str, db: Session = Depends(get_db)):
    holidays = db.query(AcademicCalendar).all()
    upcoming_holidays = [{"event": h.event, "date": h.date} for h in holidays]

    return {
        "student_id": student_id,
        "attendance_percentage": "90%",  # mocked
        "upcoming_holidays": upcoming_holidays
    }

# 3. Faculty view student academic record
@router.get("/faculty/get_student_academic_records/{student_id}")
def get_academic_record(student_id: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id_number == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return {
        "student_id": student.id_number,
        "gpa": student.gpa,
        "grades": {
            "Artificial Intelligence": "A",  # still mocked
            "Software Engineering": "B+",
            "Database Systems": "A-"
        }
    }

# 4. Faculty view their own info
@router.get("/faculty/get_info/{faculty_id}")
def get_faculty_info(faculty_id: str, db: Session = Depends(get_db)):
    # Validation: Prevent sending {faculty_id} literally
    if faculty_id.startswith("{") and faculty_id.endswith("}"):
        raise HTTPException(status_code=400, detail="Invalid faculty ID provided.")

    faculty = db.query(Faculty).filter(Faculty.faculty_id == faculty_id).first()
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
    
    return {
        "faculty_id": faculty.faculty_id,
        "name": faculty.name,
        "email": faculty.email,
        "department": faculty.department,
        "phone": faculty.phone,
        "designation": faculty.designation,
        "office": faculty.office
    }

# 5. Faculty view academic calendar
@router.get("/faculty/get_calendar")
def get_calendar(db: Session = Depends(get_db)):
    events = db.query(AcademicCalendar).all()
    return [{"event": e.event, "date": e.date} for e in events]
