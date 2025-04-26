from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Faculty, Student, IDCard, AcademicCalendar

router = APIRouter()

@router.get("/faculty/get_student_info/{student_id}")
def get_student_info(student_id: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id_number == student_id).first()
    id_card = db.query(IDCard).filter(IDCard.student_id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    response = f"""
    Name              : {student.name}
    Email             : {student.email}
    Emergency Contact : {student.emergency_contact}
    Address           : {student.personal_address}

    --- ID Card ---
    Student ID  : {id_card.student_id if id_card else 'N/A'}
    Issue Date  : {id_card.issue_date if id_card else 'N/A'}
    """

    return response.strip()

@router.get("/faculty/get_student_attendance/{student_id}")
def get_attendance(student_id: str, db: Session = Depends(get_db)):
    holidays = db.query(AcademicCalendar).all()

    if not holidays:
        holidays_text = "No upcoming holidays."
    else:
        holidays_text = "\n\n".join(
            f"Event : {h.event}\nDate  : {h.date}" for h in holidays
        )

    response = f"""
    Student ID            : {student_id}
    Attendance Percentage : 90%

    --- Upcoming Holidays ---
    {holidays_text}
    """

    return response.strip()

@router.get("/faculty/get_student_academic_records/{student_id}")
def get_academic_record(student_id: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id_number == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    response = f"""
    Student ID : {student.id_number}
    GPA        : {student.gpa}

    --- Grades ---
    Artificial Intelligence : A
    Software Engineering    : B+
    Database Systems         : A-
    """

    return response.strip()

@router.get("/faculty/get_info/{faculty_id}")
def get_faculty_info(faculty_id: str, db: Session = Depends(get_db)):
    if faculty_id.startswith("{") and faculty_id.endswith("}"):
        raise HTTPException(status_code=400, detail="Invalid faculty ID provided.")

    faculty = db.query(Faculty).filter(Faculty.faculty_id == faculty_id).first()
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")

    response = f"""
    Faculty ID  : {faculty.faculty_id}
    Name        : {faculty.name}
    Email       : {faculty.email}
    Department  : {faculty.department}
    Phone       : {faculty.phone}
    Designation : {faculty.designation}
    Office      : {faculty.office}
    """

    return response.strip()

@router.get("/faculty/get_calendar")
def get_calendar(db: Session = Depends(get_db)):
    events = db.query(AcademicCalendar).all()

    if not events:
        return "No academic calendar events found."

    formatted_events = "\n\n".join(
        f"Event : {e.event}\nDate  : {e.date}" for e in events
    )

    return formatted_events.strip()
