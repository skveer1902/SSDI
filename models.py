from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    gpa = Column(Float)
    id_number = Column(String(50), unique=True)
    emergency_contact = Column(String(100))
    personal_address = Column(String(200))

class Tuition(Base):
    __tablename__ = "tuition"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer)
    status = Column(String(50))
    amount_due = Column(Float)

class IDCard(Base):
    __tablename__ = "id_cards"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer)
    id_number = Column(String(50))
    issue_date = Column(String(50))

class AcademicCalendar(Base):
    __tablename__ = "calendar"
    id = Column(Integer, primary_key=True)
    event = Column(String(100))
    date = Column(String(50))