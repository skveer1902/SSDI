# backend/app/main.py

from fastapi import FastAPI, HTTPException
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

# CORS setup for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from routers import student  # assuming it's in routers/student.py
app.include_router(student.router)


# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# In-memory session context
user_context: Dict[str, Dict[str, str]] = {}

# Request schemas
class ChatRequest(BaseModel):
    user_id: str
    message: str

class LoginRequest(BaseModel):
    role: str
    user_id: str

#  Login endpoint
@app.post("/login")
def login(req: LoginRequest):
    role = req.role.lower()
    user_id = req.user_id.strip()

    table_map = {
        "student": ("students", "id_number"),
        "faculty": ("faculty", "faculty_id"),
        "admin": ("admin", "admin_id")
    }

    if role not in table_map:
        raise HTTPException(status_code=400, detail="Invalid role")

    table_name, id_column = table_map[role]

    try:
        with engine.connect() as conn:
            result = conn.execute(
                text(f"SELECT * FROM {table_name} WHERE {id_column} = :id"),
                {"id": user_id}
            )
            user = result.first()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not user:
        return {"status": "error", "message": f"No {role} found with ID {user_id}"}

    # Store role + ID in user_context
    user_context[user_id] = {
        "role": role,
        "id": user_id,
        "verified": True
    }

    return {"status": "success", "message": f"{role.title()} {user_id} successfully logged in."}

# ✅ Chat endpoint (for conversation only)
@app.post("/chat")
async def chat(req: ChatRequest):
    sid = req.user_id
    msg = req.message.strip()

    # Check session
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
        - students(id, name, email, gpa, id_number, emergency_contact, personal_address)
        - tuition(id, student_id, status, amount_due)
        - id_cards(id, student_id, id_number, issue_date)
        - calendar(id, event, date)
        - faculty(faculty_id, name, ...)
        - admin(admin_id, name, ...)

        The user is a {role} with ID: {identifier}.
        Use this ID to filter appropriately (e.g., id_number for students).
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

        # Execute query
        with engine.connect() as conn:
            result = conn.execute(text(sql_query))
            rows = [dict(row) for row in result.mappings()]

        if not rows:
            return {"response": "No records found."}

        # Post-process known patterns (like GPA)
        row = rows[0]
        if "gpa" in row:
            return {"response": f"Your GPA is {row['gpa']}."}
        elif "emergency_contact" in row:
            return {"response": f"Your emergency contact number is {row['emergency_contact']}."}
        else:
            return {"response": "\n".join(f"{k}: {v}" for k, v in row.items())}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
