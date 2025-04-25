# ✅ backend/app/routers/admin.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Admin, Student, Tuition, IDCard

router = APIRouter()

# Admin can view tuition details
@router.get("/admin/get_tuition_details/{student_id}")
def get_tuition_details(student_id: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id_number == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    tuition = db.query(Tuition).filter(Tuition.student_id == student.id).first()
    if not tuition:
        raise HTTPException(status_code=404, detail="Tuition details not found")
    
    return {
        "student_name": student.name,
        "tuition_status": tuition.status,
        "amount_due": tuition.amount_due
    }

# Admin can view ID card info
@router.get("/admin/get_id_card/{student_id}")
def get_id_card(student_id: str, db: Session = Depends(get_db)):
    card = db.query(IDCard).filter(IDCard.id_number == student_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="ID card not found")
    
    return {
        "id_number": card.id_number,
        "name": card.name,
        "issue_date": card.issue_date
    }

# ✅ Admin can view basic student information
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

# Admin's own profile
@router.get("/admin/get_info/{admin_id}")
def get_admin_info(admin_id: str, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.admin_id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    return {
        "name": admin.name,
        "role": admin.role
    }
