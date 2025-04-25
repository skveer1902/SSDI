# ✅ backend/app/models.py
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# ✅ Students Table
class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    gpa = Column(Float)
    id_number = Column(String(50), unique=True)
    emergency_contact = Column(String(100))
    personal_address = Column(String(200))
    password = Column(String(100), nullable=False)

# ✅ Tuition Table
class Tuition(Base):
    __tablename__ = "tuition"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, nullable=False)
    status = Column(String(50), nullable=False)
    amount_due = Column(Float, nullable=False)

# ✅ ID Card Table
class IDCard(Base):
    __tablename__ = "id_card"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, nullable=False)
    name = Column(String(100), nullable=False)
    issue_date = Column(String(50), nullable=False)
    id_number = Column(String(50), unique=True, nullable=False)

# ✅ Academic Calendar Table
class AcademicCalendar(Base):
    __tablename__ = "calender"
    id = Column(Integer, primary_key=True)
    event = Column(String(100), nullable=False)
    date = Column(String(50), nullable=False)

# ✅ Faculty Table
class Faculty(Base):
    __tablename__ = "faculty"
    id = Column(Integer, primary_key=True)
    faculty_id = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    department = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    designation = Column(String(100), nullable=False)
    office = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)

# ✅ Admin Table
class Admin(Base):
    __tablename__ = "university_admins"
    id = Column(Integer, primary_key=True)
    admin_id = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    role = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
