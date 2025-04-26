# ✅ backend/app/routers/nl_to_sql.py

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise Exception("Please set the OPENAI_API_KEY environment variable")

client = OpenAI(api_key=api_key)

def get_sql_from_prompt(prompt: str) -> str:
    system_prompt = (
        "You are an expert assistant that ONLY outputs valid MySQL queries based on user natural language queries.\n"
        "Database Tables:\n"
        "- students(id, name, email, gpa, id_number, emergency_contact, personal_address, password)\n"
        "- tuition(id, student_id, status, amount_due)\n"
        "- id_card(id, student_id, name, issue_date, id_number)\n"
        "- calendar(id, event, date)\n\n"
        "⚡ Important Notes:\n"
        "- tuition.student_id matches students.id_number (NOT students.id)\n"
        "- JOIN using tuition.student_id = students.id_number\n"
        "- id_card.student_id matches students.id_number as well\n"
        "- Only output pure SQL — no explanations, no markdown, no extra text.\n"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=300
        )

        sql = response.choices[0].message.content.strip()

        # Remove Markdown format if present
        if "```" in sql:
            sql = sql.replace("```sql", "").replace("```", "").strip()

        return sql

    except Exception as e:
        raise Exception(f"Error while generating SQL: {e}")
