# ✅ backend/app/routers/student.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Student, Tuition, IDCard, AcademicCalendar

router = APIRouter()

@router.get("/get_student_info/{student_id}")
def get_student_info(student_id: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id_number == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {
        "name": student.name,
        "email": student.email,
        "gpa": student.gpa,
        "emergency_contact": student.emergency_contact,
        "personal_address": student.personal_address
    }

@router.get("/get_tuition_details/{student_id}")
def get_tuition_details(student_id: str, db: Session = Depends(get_db)):
    tuition = db.query(Tuition).filter(Tuition.student_id == student_id).first()
    if not tuition:
        raise HTTPException(status_code=404, detail="Tuition details not found")
    return {
        "student_id": tuition.student_id,
        "status": tuition.status,
        "amount_due": float(tuition.amount_due)
    }

@router.get("/get_id_card/{student_id}")
def get_id_card(student_id: str, db: Session = Depends(get_db)):
    id_card = db.query(IDCard).filter(IDCard.student_id == student_id).first()
    if not id_card:
        raise HTTPException(status_code=404, detail="ID card not found")
    return {
        "student_id": id_card.student_id,
        "name": id_card.name,
        "issue_date": id_card.issue_date
    }

@router.get("/get_academic_calendar")
def get_academic_calendar(db: Session = Depends(get_db)):
    events = db.query(AcademicCalendar).all()
    return [{"event": event.event, "date": event.date} for event in events]

@router.get("/get_job_postings")
def get_job_postings():
    return {
        "jobs": [
            {"title": "Software Engineer Intern", "company": "Google", "location": "Remote"},
            {"title": "Data Analyst", "company": "Microsoft", "location": "Charlotte, NC"}
        ]
    }

@router.get("/get_emergency_contacts")
def get_emergency_contacts():
    return {
        "contacts": [
            {"type": "Campus Police", "number": "123-456-7890"},
            {"type": "Medical Emergency", "number": "987-654-3210"}
        ]
    }
