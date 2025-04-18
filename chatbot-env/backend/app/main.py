from fastapi import FastAPI, HTTPException
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


# Initialize FastAPI and OpenAI
app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# In-memory user context store
user_context: Dict[str, Dict[str, str]] = {}


# Request model
class ChatRequest(BaseModel):
    user_id: str
    message: str


@app.post("/chat")
async def chat(req: ChatRequest):
    sid = req.user_id
    msg = req.message.strip()


    if sid not in user_context:
        user_context[sid] = {}
    context = user_context[sid]


    # Step 1: Ask for role
    if "role" not in context:
        role = msg.lower()
        if role in ("student", "faculty", "admin"):
            context["role"] = role
            return {
                "response": f"👍 Got it. You’re logged in as **{role.title()}**. What’s your {role.title()} ID?"
            }
        return {"response": "Hello! Are you a **student**, **faculty**, or **admin**?"}


    # Step 2: Ask for ID and verify
    if "id" not in context:
        context["id"] = msg


        table_map = {
            "student": "students",
            "faculty": "faculty",  # Adjust to your schema
            "admin": "admin"
        }
        id_col_map = {
            "student": "id_number",
            "faculty": "faculty_id",
            "admin": "admin_id"
        }


        table = table_map.get(context["role"])
        id_col = id_col_map.get(context["role"])


        if not table or not id_col:
            user_context.pop(sid, None)
            raise HTTPException(status_code=500, detail="Role → table mapping not configured.")


        try:
            with engine.connect() as conn:
                result = conn.execute(
                    text(f"SELECT * FROM {table} WHERE {id_col} = :id"),
                    {"id": context["id"]}
                )
                row = result.first()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


        if not row:
            context.pop("id", None)
            return {
                "response": f"❌ No **{context['role']}** found with ID **{msg}**. Please re-enter your {context['role']} ID."
            }


        context["verified"] = True
        return {
            "response": f"✅ Successfully logged in as {context['role'].title()} {context['id']}. You can now ask your questions like 'What is my GPA?' or 'What’s my tuition fee?'"
        }


    # Step 3: Already logged in — start GPT conversation
    if context.get("verified"):
        try:
            role = context["role"]
            identifier = context["id"]


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


            # Check if GPT response looks like SQL before executing
            if not re.match(r"^\s*(SELECT|UPDATE|INSERT|DELETE)\s", sql_query, re.IGNORECASE):
                return {"response": f"⚠️ GPT returned a non-SQL message: {sql_query}"}


            # Execute the validated SQL query
            with engine.connect() as conn:
                result = conn.execute(text(sql_query))
                rows = [dict(row) for row in result.mappings()]


            return {
                "query": sql_query,
                "results": rows
            }


        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


    # Fallback for broken session
    user_context.pop(sid, None)
    return {"response": "Something went wrong. Let’s start over. Are you a student, faculty, or admin?"}


