from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from database import engine
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        system_prompt = """
        You are an assistant that converts natural language into **raw SQL**.
        ⚠️ Do NOT include markdown (no triple backticks), explanations, or comments.
        Only return a plain SQL query that can be directly executed on a MySQL database.

        The available tables are:
        - students(id, name, email, gpa, id_number, emergency_contact, personal_address)
        - tuition(id, student_id, status, amount_due)
        - id_cards(id, student_id, id_number, issue_date)
        - calendar(id, event, date)
        """

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": req.message}
            ]
        )

        sql_query = response.choices[0].message.content.strip()

        # Execute the query
        with engine.connect() as connection:
            result = connection.execute(text(sql_query))
            rows = result.mappings().all()  # 👈 this avoids the dict conversion error

        return {"query": sql_query, "results": rows}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
