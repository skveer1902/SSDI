import os
from dotenv import load_dotenv
load_dotenv()
import openai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI()

# Load your OpenAI API key from an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")
# Check if the API key is set
if not openai.api_key:
    raise Exception("Please set the OPENAI_API_KEY environment variable")

# Request model
class Message(BaseModel):
    text: str

# Define a chat endpoint that calls the OpenAI GPT API
@app.post("/chat")
async def chat_with_gpt(message: Message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use "gpt-4" if you have access and wish to use it
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message.text},
            ],
            max_tokens=150,  # Adjust as needed
            temperature=0.7,
        )
        # Get the reply text
        reply = response.choices[0].message.content.strip()
        return {"response": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# A simple home route to test if the server is running
@app.get("/")
def read_root():
    return {"message": "Welcome to the Student Chatbot API!"}