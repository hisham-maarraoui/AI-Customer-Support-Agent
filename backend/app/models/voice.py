from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class VoiceSessionRequest(BaseModel):
    user_id: Optional[str] = None
    phone_number: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class VoiceSessionResponse(BaseModel):
    session_id: str
    status: str
    vapi_assistant_id: Optional[str] = None
    phone_number: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

class VoiceSessionEndRequest(BaseModel):
    session_id: str
    reason: Optional[str] = None

class VoiceSessionEndResponse(BaseModel):
    session_id: str
    status: str
    duration: Optional[int] = None  # in seconds
    ended_at: datetime = Field(default_factory=datetime.now) 