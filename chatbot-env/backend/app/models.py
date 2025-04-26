from sqlalchemy import Column, Integer, String, Float, DECIMAL
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Student(Base):
    __tablename__ = "students"
    id_number = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    gpa = Column(Float, nullable=True)
    emergency_contact = Column(String(100), nullable=True)
    personal_address = Column(String(200), nullable=True)
    password = Column(String(100), nullable=False)

class Tuition(Base):
    __tablename__ = "tuition"
    student_id = Column(String(50), primary_key=True)  
    status = Column(String(50), nullable=False)
    amount_due = Column(DECIMAL(10, 2), nullable=False)

class IDCard(Base):
    __tablename__ = "id_card"
    student_id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    issue_date = Column(String(50), nullable=False)

class AcademicCalendar(Base):
    __tablename__ = "calendar"
    id = Column(Integer, primary_key=True, autoincrement=True)  
    event = Column(String(150), nullable=False)
    date = Column(String(50), nullable=False)

class Faculty(Base):
    __tablename__ = "faculty"
    faculty_id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    department = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    designation = Column(String(100), nullable=False)
    office = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)

class Admin(Base):
    __tablename__ = "university_admins"
    admin_id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    role = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
