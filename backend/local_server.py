from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
import sys

# Add the backend directory to the path
sys.path.append(os.path.dirname(__file__))

from app.services.ai_agent import AIAgent

app = FastAPI(title="AI Apple Support Agent API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001", 
        "http://localhost:3002",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:3002"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    conversation_id: str = None
    user_id: str = "anonymous"

class ChatResponse(BaseModel):
    response: str
    sources: list = []
    conversation_id: str = None

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "message": "AI Apple Support Agent API is running",
        "version": "1.0.0"
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Initialize AI agent
        ai_agent = AIAgent()
        
        # Get response
        response = ai_agent.get_response(request.message)
        
        return ChatResponse(
            response=response,
            sources=[],
            conversation_id=request.conversation_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("Starting local development server...")
    print("API will be available at: http://localhost:8000")
    print("Health check: http://localhost:8000/health")
    print("Chat endpoint: http://localhost:8000/chat")
    uvicorn.run(app, host="0.0.0.0", port=8000) 