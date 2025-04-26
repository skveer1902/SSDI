from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Admin, Student, Tuition, IDCard, AcademicCalendar

router = APIRouter()

# 1. Admin view a student's tuition details
@router.get("/admin/get_tuition_details/{student_id}")
def get_tuition_details(student_id: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id_number == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    tuition = db.query(Tuition).filter(Tuition.student_id == student.id_number).first()
    if not tuition:
        raise HTTPException(status_code=404, detail="Tuition details not found")
    
    return {
        "student_name": student.name,
        "id_number": student.id_number,
        "tuition_status": tuition.status,
        "amount_due": str(tuition.amount_due)
    }

# 2. Admin view a student's ID card info
@router.get("/admin/get_id_card/{student_id}")
def get_id_card(student_id: str, db: Session = Depends(get_db)):
    id_card = db.query(IDCard).filter(IDCard.student_id == student_id).first()
    if not id_card:
        raise HTTPException(status_code=404, detail="ID card not found")
    
    return {
        "student_id": id_card.student_id,
        "name": id_card.name,
        "issue_date": id_card.issue_date
    }

# 3. Admin view basic student information
@router.get("/admin/get_student_info/{student_id}")
def get_student_info(student_id: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id_number == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return {
        "name": student.name,
        "email": student.email,
        "gpa": student.gpa,
        "id_number": student.id_number,
        "emergency_contact": student.emergency_contact,
        "personal_address": student.personal_address
    }

# 4. Admin's own profile
@router.get("/admin/get_info/{admin_id}")
def get_admin_info(admin_id: str, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.admin_id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    return {
        "name": admin.name,
        "role": admin.role,
        "admin_id": admin.admin_id
    }

# 5. Admin view all calendar events (bonus)
@router.get("/admin/get_calendar_events")
def get_calendar(db: Session = Depends(get_db)):
    events = db.query(AcademicCalendar).all()
    return [{"event": e.event, "date": e.date} for e in events]
