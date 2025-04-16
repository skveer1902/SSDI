import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_sql_from_prompt(prompt):
    system_prompt = (
        "You are a helpful assistant that converts natural language queries into MySQL queries. "
        "Assume the database has the following tables: students(id, name, email, gpa, id_number, emergency_contact, personal_address), "
        "tuition(id, student_id, status, amount_due), id_cards(id, student_id, id_number, issue_date), calendar(id, event, date). "
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    return response.choices[0].message["content"].strip()
