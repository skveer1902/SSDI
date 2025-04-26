# backend/app/routers/gpt.py

import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise Exception("Please set the OPENAI_API_KEY environment variable")

client = OpenAI(api_key=api_key)

# Initialize router
router = APIRouter()

# Request model
class Message(BaseModel):
    text: str

# Chat with GPT endpoint
@router.post("/chat")
async def chat_with_gpt(message: Message):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message.text}
            ],
            temperature=0.7,
            max_tokens=200
        )
        reply = response.choices[0].message.content.strip()
        return {"response": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
