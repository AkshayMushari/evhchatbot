hi
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import os
from langchain.llms import AzureOpenAI
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

# Set Azure OpenAI environment variables
os.environ['SSL_CERT_FILE'] = r"C:\path\to\cacert.pem"  # Path to your cert file
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_KEY"] = "your_azure_openai_api_key"  # Replace with your key
os.environ["OPENAI_API_VERSION"] = "2023-05-15"

# Initialize Azure OpenAI with LangChain
llm = AzureOpenAI(
    deployment_name="your_azure_deployment_name",  # Replace with your deployment name
    model_name="gpt-35-turbo",
    max_tokens=200,
)

class ChatRequest(BaseModel):
    session_id: str
    message: str

@app.post("/chat/")
def chat(request: ChatRequest):
    session_id = request.session_id
    message = request.message

    if session_id not in conversations:
        conversations[session_id] = []

    conversations[session_id].append({"role": "user", "content": message})

    try:
        # Generate response from Azure OpenAI
        response = llm.generate([{"role": "user", "content": message}])
        bot_reply = response.generations[0][0].text

        conversations[session_id].append({"role": "assistant", "content": bot_reply})

        return {"response": bot_reply}

    except Exception as e:
        print("Error:", str(e))
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
