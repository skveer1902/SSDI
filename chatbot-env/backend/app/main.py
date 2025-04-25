# ✅ backend/app/main.py
import traceback
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from sqlalchemy import text
from database import engine
from dotenv import load_dotenv
from typing import Dict
import os
import re

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
from routers import student, faculty, admin
app.include_router(student.router)
app.include_router(faculty.router)
app.include_router(admin.router)

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Session store
user_context: Dict[str, Dict[str, str]] = {}

# Request Schemas
class ChatRequest(BaseModel):
    user_id: str
    message: str

class LoginRequest(BaseModel):
    role: str
    user_id: str
    password: str

class LogoutRequest(BaseModel):
    user_id: str

#  login endpoint
@app.post("/login")
def login(req: LoginRequest):
    role = req.role.lower()
    user_id = req.user_id.strip()
    password = req.password.strip()

    table_map = {
        "student": ("students", "id_number"),
        "faculty": ("faculty", "faculty_id"),
        "admin": ("university_admins", "admin_id")
    }

    if role not in table_map:
        raise HTTPException(status_code=400, detail="Invalid role")

    table_name, id_column = table_map[role]

    try:
        with engine.connect() as conn:
            result = conn.execute(
                text(f"SELECT * FROM {table_name} WHERE {id_column} = :id AND password = :password"),
                {"id": user_id, "password": password}
            )
            user = result.first()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not user:
        raise HTTPException(status_code=401, detail="Invalid ID or password")

    user_context[user_id] = {
        "role": role,
        "id": user_id,
        "verified": True
    }

    return {
        "status": "success",
        "message": f"{role.title()} {user_id} successfully logged in.",
        "role": role,
        "user_id": user_id
    }

# ✅ Logout endpoint
@app.post("/logout")
def logout(req: LogoutRequest):
    user_context.pop(req.user_id, None)
    return {"status": "success", "message": "User logged out successfully."}

# ✅ Chat endpoint
@app.post("/chat")
async def chat(req: ChatRequest):
    sid = req.user_id
    msg = req.message.strip()

    if sid not in user_context or not user_context[sid].get("verified"):
        return {
            "response": "🔒 You must log in first. Please go back to the login page."
        }

    context = user_context[sid]
    role = context["role"]
    identifier = context["id"]

    try:
        system_prompt = f"""
        You are an assistant that converts natural language to SQL.
        Only output raw SQL. Do not include explanations.
        Use only valid column names based on the schema below.

        Tables and columns:
        - students(id, name, email, gpa, id_number, emergency_contact, personal_address, password)
        - tuition(id, student_id, status, amount_due)
        - id_card(id, student_id, name, issue_date, id_number)
        - calendar(id, event, date)
        - faculty(faculty_id, name, department, email, phone, designation, office, password)
        - university_admins(admin_id, name, role, password)

        The user is a {role} with ID: {identifier}.
        Use this ID to filter appropriately (e.g., id_number for students, faculty_id for faculty).
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": msg}
            ]
        )

        sql_query = response.choices[0].message.content.strip()
        if "```" in sql_query:
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

        if not re.match(r"^\s*(SELECT|UPDATE|INSERT|DELETE)\s", sql_query, re.IGNORECASE):
            return {"response": f"⚠️ GPT returned a non-SQL message: {sql_query}"}

        with engine.connect() as conn:
            result = conn.execute(text(sql_query))
            rows = [dict(row) for row in result.mappings()]

        if not rows:
            return {"response": "No records found."}

        row = rows[0]

        # Format nicely if it's student personal details
        if set(["name", "email", "gpa", "id_number", "emergency_contact", "personal_address"]).issubset(row.keys()):
            return {
                "response": (
                    f"Name: {row['name']}\n"
                    f"Email: {row['email']}\n"
                    f"GPA: {row['gpa']}\n"
                    f"ID Number: {row['id_number']}\n"
                    f"Emergency Contact: {row['emergency_contact']}\n"
                    f"Address: {row['personal_address']}"
                )
            }

        return {
            "response": "\n".join(f"{k}: {v}" for k, v in row.items())
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    
