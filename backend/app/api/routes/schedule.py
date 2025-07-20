from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import uuid
from datetime import datetime, date, time
from app.models.schedule import (
    ScheduleMeetingRequest, 
    ScheduleMeetingResponse, 
    MeetingSlot, 
    AvailableSlotsResponse,
    MeetingType,
    MeetingStatus
)

router = APIRouter()

# In-memory storage for meetings (use database in production)
meetings = {}

# Mock available time slots (in production, this would come from a calendar system)
AVAILABLE_SLOTS = {
    "monday": ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00"],
    "tuesday": ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00"],
    "wednesday": ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00"],
    "thursday": ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00"],
    "friday": ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00"]
}

@router.post("/meeting", response_model=ScheduleMeetingResponse)
async def schedule_meeting(request: ScheduleMeetingRequest):
    """Schedule a meeting with Apple Support"""
    try:
        meeting_id = str(uuid.uuid4())
        
        # Validate date and time
        if request.preferred_date < date.today():
            raise HTTPException(status_code=400, detail="Cannot schedule meetings in the past")
        
        # Check if slot is available
        day_name = request.preferred_date.strftime("%A").lower()
        if day_name not in AVAILABLE_SLOTS:
            raise HTTPException(status_code=400, detail="No available slots for this day")
        
        time_str = request.preferred_time.strftime("%H:%M")
        if time_str not in AVAILABLE_SLOTS[day_name]:
            raise HTTPException(status_code=400, detail="Requested time slot is not available")
        
        # Create meeting
        meeting = {
            "meeting_id": meeting_id,
            "user_id": request.user_id,
            "user_name": request.user_name,
            "user_email": request.user_email,
            "user_phone": request.user_phone,
            "meeting_type": request.meeting_type,
            "preferred_date": request.preferred_date,
            "preferred_time": request.preferred_time,
            "scheduled_date": datetime.combine(request.preferred_date, request.preferred_time),
            "duration_minutes": request.duration_minutes,
            "topic": request.topic,
            "notes": request.notes,
            "status": MeetingStatus.SCHEDULED,
            "confirmation_code": f"APPLE{meeting_id[:8].upper()}",
            "meeting_link": None,  # Would be generated for video meetings
            "created_at": datetime.now()
        }
        
        # Generate meeting link for video meetings
        if request.meeting_type == MeetingType.VIDEO:
            meeting["meeting_link"] = f"https://meet.apple.com/{meeting_id}"
        
        # Store meeting
        meetings[meeting_id] = meeting
        
        # In production, you would:
        # 1. Send confirmation email
        # 2. Add to calendar system
        # 3. Send notifications
        # 4. Update availability
        
        return ScheduleMeetingResponse(
            meeting_id=meeting_id,
            status=MeetingStatus.SCHEDULED,
            scheduled_date=meeting["scheduled_date"],
            meeting_type=request.meeting_type,
            duration_minutes=request.duration_minutes,
            confirmation_code=meeting["confirmation_code"],
            meeting_link=meeting["meeting_link"],
            created_at=datetime.now()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scheduling meeting: {str(e)}")

@router.get("/meetings/{meeting_id}", response_model=Dict[str, Any])
async def get_meeting(meeting_id: str):
    """Get meeting details"""
    if meeting_id not in meetings:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    return meetings[meeting_id]

@router.get("/meetings", response_model=List[Dict[str, Any]])
async def list_meetings(user_id: str = None, status: MeetingStatus = None):
    """List meetings, optionally filtered by user_id and status"""
    meeting_list = list(meetings.values())
    
    if user_id:
        meeting_list = [m for m in meeting_list if m.get("user_id") == user_id]
    
    if status:
        meeting_list = [m for m in meeting_list if m.get("status") == status]
    
    return meeting_list

@router.put("/meetings/{meeting_id}/cancel")
async def cancel_meeting(meeting_id: str):
    """Cancel a meeting"""
    if meeting_id not in meetings:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    meeting = meetings[meeting_id]
    
    # Check if meeting can be cancelled (e.g., not too close to meeting time)
    time_until_meeting = meeting["scheduled_date"] - datetime.now()
    if time_until_meeting.total_seconds() < 3600:  # Less than 1 hour
        raise HTTPException(status_code=400, detail="Cannot cancel meetings less than 1 hour before start time")
    
    meeting["status"] = MeetingStatus.CANCELLED
    meeting["cancelled_at"] = datetime.now()
    
    # In production, you would:
    # 1. Send cancellation email
    # 2. Update calendar
    # 3. Free up the time slot
    
    return {"message": "Meeting cancelled successfully", "meeting_id": meeting_id}

@router.put("/meetings/{meeting_id}/reschedule")
async def reschedule_meeting(
    meeting_id: str,
    new_date: date,
    new_time: time
):
    """Reschedule a meeting"""
    if meeting_id not in meetings:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    meeting = meetings[meeting_id]
    
    # Validate new date and time
    if new_date < date.today():
        raise HTTPException(status_code=400, detail="Cannot reschedule to a past date")
    
    # Check if new slot is available
    day_name = new_date.strftime("%A").lower()
    if day_name not in AVAILABLE_SLOTS:
        raise HTTPException(status_code=400, detail="No available slots for this day")
    
    time_str = new_time.strftime("%H:%M")
    if time_str not in AVAILABLE_SLOTS[day_name]:
        raise HTTPException(status_code=400, detail="Requested time slot is not available")
    
    # Update meeting
    old_date = meeting["scheduled_date"]
    meeting["preferred_date"] = new_date
    meeting["preferred_time"] = new_time
    meeting["scheduled_date"] = datetime.combine(new_date, new_time)
    meeting["rescheduled_at"] = datetime.now()
    
    # In production, you would:
    # 1. Send reschedule notification
    # 2. Update calendar
    # 3. Free up old slot
    
    return {
        "message": "Meeting rescheduled successfully",
        "meeting_id": meeting_id,
        "old_date": old_date,
        "new_date": meeting["scheduled_date"]
    }

@router.get("/availability/{meeting_date}", response_model=AvailableSlotsResponse)
async def get_available_slots(meeting_date: date):
    """Get available time slots for a specific date"""
    try:
        day_name = meeting_date.strftime("%A").lower()
        
        if day_name not in AVAILABLE_SLOTS:
            return AvailableSlotsResponse(
                date=meeting_date,
                slots=[]
            )
        
        # Convert time strings to time objects
        slots = []
        for time_str in AVAILABLE_SLOTS[day_name]:
            time_obj = datetime.strptime(time_str, "%H:%M").time()
            slots.append(MeetingSlot(
                date=meeting_date,
                time=time_obj,
                available=True
            ))
        
        return AvailableSlotsResponse(
            date=meeting_date,
            slots=slots
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting available slots: {str(e)}")

@router.get("/availability", response_model=Dict[str, Any])
async def get_availability_range(start_date: date, end_date: date):
    """Get availability for a date range"""
    try:
        availability = {}
        current_date = start_date
        
        while current_date <= end_date:
            day_name = current_date.strftime("%A").lower()
            
            if day_name in AVAILABLE_SLOTS:
                slots = []
                for time_str in AVAILABLE_SLOTS[day_name]:
                    time_obj = datetime.strptime(time_str, "%H:%M").time()
                    slots.append({
                        "time": time_str,
                        "available": True
                    })
                
                availability[current_date.isoformat()] = slots
            else:
                availability[current_date.isoformat()] = []
            
            current_date = current_date.replace(day=current_date.day + 1)
        
        return {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "availability": availability
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting availability range: {str(e)}") 