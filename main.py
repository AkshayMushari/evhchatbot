from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store conversations in memory
conversations: Dict[str, List[Dict[str, str]]] = {}

# Replace with your Groq API key
GROQ_API_KEY = "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"
# GROQ_API_URL = "https://api.groq.com/v1/chat/completions"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


class ChatRequest(BaseModel):
    session_id: str
    message: str


GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "mixtral-8x7b-32768"  # Replace with a valid model

@app.post("/chat/")
def chat(request: ChatRequest):
    session_id = request.session_id
    message = request.message

    if session_id not in conversations:
        conversations[session_id] = []

    conversations[session_id].append({"role": "user", "content": message})

    try:
        response = requests.post(
            GROQ_API_URL,
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            json={
                "model": GROQ_MODEL,  # Use a valid model
                "messages": conversations[session_id]
            }
        )

        print("Groq API Response:", response.status_code, response.text)

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Groq API Error: {response.text}")

        response_data = response.json()
        bot_reply = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")

        conversations[session_id].append({"role": "assistant", "content": bot_reply})

        return {"response": bot_reply}

    except Exception as e:
        print("Error:", str(e))
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
