from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import uuid
from datetime import datetime
import httpx

from app.models.voice import VoiceSessionRequest, VoiceSessionResponse, VoiceSessionEndRequest, VoiceSessionEndResponse
from app.core.config import settings

router = APIRouter()

# In-memory storage for voice sessions (use database in production)
voice_sessions = {}

@router.post("/start", response_model=VoiceSessionResponse)
async def start_voice_session(request: VoiceSessionRequest):
    """Start a voice session with Vapi"""
    try:
        if not settings.vapi_api_key:
            raise HTTPException(status_code=500, detail="Vapi API key not configured")
        
        session_id = str(uuid.uuid4())
        
        # Vapi assistant configuration
        assistant_config = {
            "name": "Apple Support Agent",
            "model": {
                "provider": "openai",
                "model": "gpt-4",
                "temperature": 0.7,
                "systemPrompt": """You are an Apple Support AI Agent, designed to help users with questions about Apple products and services through voice interactions.

Your role is to:
1. Provide accurate, helpful information about Apple products, services, and troubleshooting
2. Be friendly, professional, and empathetic
3. Speak clearly and at a natural pace
4. Redirect users to official Apple support channels when appropriate
5. Never provide personal, legal, or financial advice
6. Detect and handle sensitive queries appropriately

When responding:
- Use the provided context from Apple's official support documentation
- If you don't have enough information, suggest contacting Apple Support directly
- Be concise but thorough
- Use a helpful, conversational tone
- Always mention the source of your information

Remember: You are not a replacement for official Apple Support, but a helpful assistant to guide users to the right information.""",
                "functions": [
                    {
                        "name": "schedule_meeting",
                        "description": "Schedule a meeting with Apple Support when a user requests it",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "user_name": {
                                    "type": "string",
                                    "description": "The user's name"
                                },
                                "user_email": {
                                    "type": "string",
                                    "description": "The user's email address"
                                },
                                "user_phone": {
                                    "type": "string",
                                    "description": "The user's phone number (optional)"
                                },
                                "meeting_type": {
                                    "type": "string",
                                    "enum": ["phone", "video", "in_person"],
                                    "description": "Type of meeting requested"
                                },
                                "topic": {
                                    "type": "string",
                                    "description": "Brief description of what the user needs help with"
                                },
                                "preferred_date": {
                                    "type": "string",
                                    "description": "Preferred date for the meeting (YYYY-MM-DD)"
                                },
                                "preferred_time": {
                                    "type": "string",
                                    "description": "Preferred time for the meeting (HH:MM)"
                                }
                            },
                            "required": ["user_name", "user_email", "topic", "preferred_date", "preferred_time"]
                        }
                    }
                ]
            },
            "voice": {
                "provider": "11labs",
                "voiceId": "pNInz6obpgDQGcFmaJgB"  # Adam voice
            },
            "firstMessage": "Hello! I'm your Apple Support assistant. How can I help you today?",
            "phoneNumberId": None,  # Will be set if phone call
            "metadata": {
                "session_id": session_id,
                "user_id": request.user_id,
                "context": request.context
            }
        }
        
        # Create Vapi assistant
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.vapi.ai/assistant",
                headers={
                    "Authorization": f"Bearer {settings.vapi_api_key}",
                    "Content-Type": "application/json"
                },
                json=assistant_config
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail=f"Failed to create Vapi assistant: {response.text}")
            
            assistant_data = response.json()
            assistant_id = assistant_data.get("id")
            
            # Create call if phone number provided
            call_id = None
            if request.phone_number:
                call_config = {
                    "assistantId": assistant_id,
                    "phoneNumberId": "your_phone_number_id",  # Replace with actual phone number ID
                    "customer": {
                        "number": request.phone_number
                    }
                }
                
                call_response = await client.post(
                    "https://api.vapi.ai/call",
                    headers={
                        "Authorization": f"Bearer {settings.vapi_api_key}",
                        "Content-Type": "application/json"
                    },
                    json=call_config
                )
                
                if call_response.status_code == 200:
                    call_data = call_response.json()
                    call_id = call_data.get("id")
        
        # Store session information
        voice_sessions[session_id] = {
            "session_id": session_id,
            "assistant_id": assistant_id,
            "call_id": call_id,
            "user_id": request.user_id,
            "phone_number": request.phone_number,
            "status": "active",
            "created_at": datetime.now(),
            "context": request.context
        }
        
        return VoiceSessionResponse(
            session_id=session_id,
            status="active",
            vapi_assistant_id=assistant_id,
            phone_number=request.phone_number,
            created_at=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting voice session: {str(e)}")

@router.post("/end", response_model=VoiceSessionEndResponse)
async def end_voice_session(request: VoiceSessionEndRequest):
    """End a voice session"""
    try:
        if request.session_id not in voice_sessions:
            raise HTTPException(status_code=404, detail="Voice session not found")
        
        session = voice_sessions[request.session_id]
        
        # End call if exists
        if session.get("call_id") and settings.vapi_api_key:
            async with httpx.AsyncClient() as client:
                await client.post(
                    f"https://api.vapi.ai/call/{session['call_id']}/end",
                    headers={
                        "Authorization": f"Bearer {settings.vapi_api_key}",
                        "Content-Type": "application/json"
                    }
                )
        
        # Update session status
        session["status"] = "ended"
        session["ended_at"] = datetime.now()
        session["end_reason"] = request.reason
        
        # Calculate duration
        duration = None
        if session.get("created_at") and session.get("ended_at"):
            duration = int((session["ended_at"] - session["created_at"]).total_seconds())
        
        return VoiceSessionEndResponse(
            session_id=request.session_id,
            status="ended",
            duration=duration,
            ended_at=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error ending voice session: {str(e)}")

@router.get("/sessions/{session_id}")
async def get_voice_session(session_id: str):
    """Get voice session information"""
    if session_id not in voice_sessions:
        raise HTTPException(status_code=404, detail="Voice session not found")
    
    return voice_sessions[session_id]

@router.get("/sessions")
async def list_voice_sessions(user_id: str = None, limit: int = 10):
    """List voice sessions"""
    sessions = list(voice_sessions.values())
    
    if user_id:
        sessions = [s for s in sessions if s.get("user_id") == user_id]
    
    return sessions[:limit]

@router.get("/webhook")
async def vapi_webhook():
    """Handle Vapi webhooks"""
    # This endpoint would handle webhooks from Vapi for call events
    # Implementation depends on specific webhook events you want to handle
    return {"status": "webhook received"}

@router.post("/webhook")
async def vapi_webhook_post():
    """Handle Vapi webhook POST requests"""
    # Handle webhook events from Vapi
    # This would include events like call started, call ended, speech detected, etc.
    return {"status": "webhook processed"} 