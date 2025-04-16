# backend/app/routers/gpt.py

import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Raise error if key is not found
if not openai.api_key:
    raise Exception("Please set the OPENAI_API_KEY environment variable")

# Initialize router
router = APIRouter()

# Request body model
class Message(BaseModel):
    text: str

# Chat with GPT endpoint
@router.post("/chat")
async def chat_with_gpt(message: Message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # You can change this to "gpt-3.5-turbo" if needed
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message.text}
            ],
            max_tokens=150,
            temperature=0.7
        )
        reply = response.choices[0].message.content.strip()
        return {"response": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))