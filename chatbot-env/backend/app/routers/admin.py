from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Admin, Student, Tuition, IDCard, AcademicCalendar

router = APIRouter()

@router.get("/admin/get_tuition_details/{student_id}")
def get_tuition_details(student_id: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id_number == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    tuition = db.query(Tuition).filter(Tuition.student_id == student.id_number).first()
    if not tuition:
        raise HTTPException(status_code=404, detail="Tuition details not found")
    
    response = f"""
    Student Name    : {student.name}
    ID Number       : {student.id_number}
    Tuition Status  : {tuition.status}
    Amount Due      : ₹{tuition.amount_due}
    """
    return response.strip()

@router.get("/admin/get_id_card/{student_id}")
def get_id_card(student_id: str, db: Session = Depends(get_db)):
    id_card = db.query(IDCard).filter(IDCard.student_id == student_id).first()
    if not id_card:
        raise HTTPException(status_code=404, detail="ID card not found")
    
    response = f"""
    Student ID  : {id_card.student_id}
    Name        : {id_card.name}
    Issue Date  : {id_card.issue_date}
    """
    return response.strip()

@router.get("/admin/get_student_info/{student_id}")
def get_student_info(student_id: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id_number == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    response = f"""
    Name              : {student.name}
    Email             : {student.email}
    GPA               : {student.gpa}
    ID Number         : {student.id_number}
    Emergency Contact : {student.emergency_contact}
    Address           : {student.personal_address}
    """
    return response.strip()

@router.get("/admin/get_student_attendance/{student_id}")
def get_student_attendance(student_id: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id_number == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    attendance_value = f"{student.attendance}%" if student.attendance is not None else "N/A"

    response = f"""
    Student ID            : {student.id_number}
    Attendance Percentage : {attendance_value}
    """
    return response.strip()

@router.get("/admin/get_info/{admin_id}")
def get_admin_info(admin_id: str, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.admin_id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    response = f"""
    Name      : {admin.name}
    Role      : {admin.role}
    Admin ID  : {admin.admin_id}
    """
    return response.strip()

@router.get("/admin/get_calendar_events")
def get_calendar(db: Session = Depends(get_db)):
    events = db.query(AcademicCalendar).all()
    
    if not events:
        return "No calendar events found."

    formatted_events = "\n\n".join(
        f"Event : {e.event}\nDate  : {e.date}" for e in events
    )
    return formatted_events.strip()
