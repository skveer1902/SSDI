from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Student, Tuition, IDCard, AcademicCalendar

router = APIRouter()

# Personal Info
@router.get("/get_student_info/{student_id}")
def get_student_info(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# Tuition Info
@router.get("/get_tuition_details/{student_id}")
def get_tuition_details(student_id: int, db: Session = Depends(get_db)):
    tuition = db.query(Tuition).filter(Tuition.student_id == student_id).first()
    if not tuition:
        raise HTTPException(status_code=404, detail="Tuition details not found")
    return tuition

# ID Card
@router.get("/get_id_card/{student_id}")
def get_id_card(student_id: int, db: Session = Depends(get_db)):
    card = db.query(IDCard).filter(IDCard.student_id == student_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="ID card not found")
    return card

# Job Postings (Mocked for now)
@router.get("/get_job_postings")
def get_job_postings():
    return {
        "jobs": [
            {"title": "Software Engineer Intern", "company": "Google", "location": "Remote"},
            {"title": "Data Analyst", "company": "Microsoft", "location": "Charlotte, NC"}
        ]
    }

# Academic Calendar
@router.get("/get_academic_calendar")
def get_academic_calendar(db: Session = Depends(get_db)):
    events = db.query(AcademicCalendar).all()
    return {"calendar": events}

# Emergency Contacts (Static for now)
@router.get("/get_emergency_contacts")
def get_emergency_contacts():
    return {
        "contacts": [
            {"type": "Campus Police", "number": "123-456-7890"},
            {"type": "Medical Emergency", "number": "987-654-3210"}
        ]
    }
