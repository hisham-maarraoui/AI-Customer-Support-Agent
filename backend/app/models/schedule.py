from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date, time
from enum import Enum

class MeetingType(str, Enum):
    PHONE = "phone"
    VIDEO = "video"
    IN_PERSON = "in_person"

class MeetingStatus(str, Enum):
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class ScheduleMeetingRequest(BaseModel):
    user_id: str
    user_name: str
    user_email: str
    user_phone: Optional[str] = None
    meeting_type: MeetingType = MeetingType.PHONE
    preferred_date: date
    preferred_time: time
    duration_minutes: int = Field(default=30, ge=15, le=120)
    topic: str
    notes: Optional[str] = None

class ScheduleMeetingResponse(BaseModel):
    meeting_id: str
    status: MeetingStatus
    scheduled_date: datetime
    meeting_type: MeetingType
    duration_minutes: int
    confirmation_code: Optional[str] = None
    meeting_link: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

class MeetingSlot(BaseModel):
    date: date
    time: time
    available: bool = True
    meeting_id: Optional[str] = None

class AvailableSlotsResponse(BaseModel):
    date: date
    slots: List[MeetingSlot] 