import os
import re
import traceback
from typing import Dict

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from openai import OpenAI
from sqlalchemy import text
from database import engine, get_db
from dotenv import load_dotenv
import httpx

# Routers
from routers import student, faculty, admin

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(student.router)
app.include_router(faculty.router)
app.include_router(admin.router)

# OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# In-memory user sessions
user_context: Dict[str, Dict[str, str]] = {}

# Request Models
class LoginRequest(BaseModel):
    role: str
    user_id: str
    password: str

class ChatRequest(BaseModel):
    user_id: str
    message: str

# ✅ Login Endpoint
@app.post("/login")
def login(req: LoginRequest):
    role = req.role.lower()
    user_id = req.user_id.strip()
    password = req.password.strip()

    table_map = {
        "student": ("students", "id_number"),
        "faculty": ("faculty", "faculty_id"),
        "admin": ("university_admins", "admin_id"),
    }

    if role not in table_map:
        raise HTTPException(status_code=400, detail="Invalid role selected.")

    table_name, id_column = table_map[role]

    try:
        with engine.connect() as conn:
            result = conn.execute(
                text(f"""
                    SELECT * FROM {table_name}
                    WHERE {id_column} = :id AND password = :password
                """),
                {"id": user_id, "password": password}
            )
            user = result.first()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not user:
        raise HTTPException(status_code=401, detail="Invalid ID or password.")

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

# ✅ Logout Endpoint
@app.post("/logout")
async def logout():
    return JSONResponse(content={"message": "Successfully logged out."})

# ✅ Chat Endpoint (updated)
@app.post("/chat")
async def chat(req: ChatRequest):
    sid = req.user_id
    msg = req.message.strip()

    if sid not in user_context or not user_context[sid].get("verified"):
        return {"response": "🔒 You must log in first."}

    context = user_context[sid]
    role = context["role"]
    identifier = context["id"]

    # 📢 Role-specific dynamic system prompt
    if role == "student":
        system_prompt = f"""
        You assist a student.
        Only respond with one line: CALL API: /endpoint

        Endpoints:
        - /get_student_info/{identifier}
        - /get_tuition_details/{identifier}
        - /get_id_card/{identifier}
        - /get_academic_calendar
        - /get_job_postings
        - /get_emergency_contacts
        """

    elif role == "faculty":
        system_prompt = f"""
        You assist a faculty member.
        Only respond with one line: CALL API: /endpoint

        Endpoints:
        - /faculty/get_student_info/{{student_id}}
        - /faculty/get_attendance/{{student_id}}
        - /faculty/get_academic_record/{{student_id}}
        - /faculty/get_info/{identifier}
        - /faculty/get_calendar
        """

    elif role == "admin":
        system_prompt = f"""
        You assist an admin user.
        Only respond with one line: CALL API: /endpoint

        Endpoints:
        - /admin/get_student_info/{{student_id}}
        - /admin/get_tuition_details/{{student_id}}
        - /admin/get_id_card/{{student_id}}
        - /admin/get_info/{identifier}
        - /admin/get_calendar_events
        """

    else:
        system_prompt = "Invalid role."

    try:
        # 🔥 OpenAI call
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": msg}
            ]
        )

        raw_reply = response.choices[0].message.content.strip()

        if not raw_reply.startswith("CALL API:"):
            return {"response": f"⚠️ Invalid output from GPT. Full reply:\n\n{raw_reply}"}

        api_path = raw_reply.replace("CALL API:", "").strip()

        # ✅ Make internal API call
        async with httpx.AsyncClient(base_url="http://localhost:8000") as async_client:
            api_response = await async_client.get(api_path)

        if api_response.status_code != 200:
            return {"response": "⚠️ Could not fetch the information. Please try again."}

        data = api_response.json()

        # ✅ Pretty format
        if isinstance(data, dict):
            formatted = "\n".join(f"{k.replace('_', ' ').title()}: {v}" for k, v in data.items())
        else:
            formatted = str(data)

        return {"response": formatted}

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
