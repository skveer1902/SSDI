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
    
    response = f"""
    Name              : {student.name}
    Email             : {student.email}
    GPA               : {student.gpa}
    Emergency Contact : {student.emergency_contact}
    Address           : {student.personal_address}
    Attendance        : {student.attendance}%
    """
    return response.strip()

@router.get("/get_tuition_details/{student_id}")
def get_tuition_details(student_id: str, db: Session = Depends(get_db)):
    tuition = db.query(Tuition).filter(Tuition.student_id == student_id).first()
    if not tuition:
        raise HTTPException(status_code=404, detail="Tuition details not found")
    
    response = f"""
    Student ID   : {tuition.student_id}
    Status       : {tuition.status}
    Amount Due   : ₹{float(tuition.amount_due)}
    """
    return response.strip()

@router.get("/get_id_card/{student_id}")
def get_id_card(student_id: str, db: Session = Depends(get_db)):
    id_card = db.query(IDCard).filter(IDCard.student_id == student_id).first()
    if not id_card:
        raise HTTPException(status_code=404, detail="ID card not found")
    
    response = f"""
    Student ID   : {id_card.student_id}
    Name         : {id_card.name}
    Issue Date   : {id_card.issue_date}
    """
    return response.strip()

@router.get("/get_academic_calendar")
def get_academic_calendar(db: Session = Depends(get_db)):
    events = db.query(AcademicCalendar).all()

    if not events:
        return "No academic events found."

    formatted_events = "\n\n".join(
        f"Event : {event.event}\nDate  : {event.date}" for event in events
    )
    return formatted_events.strip()

@router.get("/get_job_postings")
def get_job_postings():
    response = """
    1. Title    : Software Engineer Intern
       Company  : Google
       Location : Remote

    2. Title    : Data Analyst
       Company  : Microsoft
       Location : Charlotte, NC
    """
    return response.strip()

@router.get("/get_emergency_contacts")
def get_emergency_contacts():
    response = """
    Campus Police     : 123-456-7890
    Medical Emergency : 987-654-3210
    """
    return response.strip()
