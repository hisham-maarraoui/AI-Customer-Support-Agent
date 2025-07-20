from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
import uuid
from datetime import datetime

from app.models.chat import ChatRequest, ChatResponse, Message, MessageRole, Conversation
from app.services.ai_agent import ai_agent
from app.services.guardrails import guardrails

router = APIRouter()

# In-memory storage for conversations (use database in production)
conversations = {}

@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    """Chat with the AI agent"""
    try:
        # Generate conversation ID if not provided
        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        # Get or create conversation
        if conversation_id not in conversations:
            conversations[conversation_id] = Conversation(
                id=conversation_id,
                user_id=request.user_id,
                messages=[],
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        
        conversation = conversations[conversation_id]
        
        # Add user message to conversation
        user_message = Message(
            role=MessageRole.USER,
            content=request.message,
            timestamp=datetime.now()
        )
        conversation.messages.append(user_message)
        
        # Prepare conversation history for AI
        conversation_history = []
        for msg in conversation.messages[-10:]:  # Last 10 messages
            conversation_history.append({
                'role': msg.role.value,
                'content': msg.content
            })
        
        # Generate AI response
        ai_response = ai_agent.generate_response(
            user_message=request.message,
            conversation_history=conversation_history,
            context=request.context
        )
        
        # Add AI response to conversation
        assistant_message = Message(
            role=MessageRole.ASSISTANT,
            content=ai_response['message'],
            timestamp=datetime.now(),
            metadata={
                'confidence': ai_response.get('confidence', 0.0),
                'sources': ai_response.get('sources', []),
                'guardrail_triggered': ai_response.get('guardrail_triggered', False)
            }
        )
        conversation.messages.append(assistant_message)
        
        # Update conversation timestamp
        conversation.updated_at = datetime.now()
        
        # Log guardrail violations if any
        if ai_response.get('guardrail_triggered'):
            guardrails.log_violation(
                user_id=request.user_id or 'anonymous',
                violation_type=ai_response.get('guardrail_type', 'unknown'),
                details={'message': request.message}
            )
        
        return ChatResponse(
            message=ai_response['message'],
            conversation_id=conversation_id,
            sources=ai_response.get('sources', []),
            confidence=ai_response.get('confidence', 0.0),
            metadata={
                'guardrail_triggered': ai_response.get('guardrail_triggered', False),
                'guardrail_type': ai_response.get('guardrail_type'),
                'tool_used': ai_response.get('tool_used'),
                'meeting_id': ai_response.get('meeting_id')
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")

@router.get("/conversations/{conversation_id}", response_model=Conversation)
async def get_conversation(conversation_id: str):
    """Get a specific conversation"""
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return conversations[conversation_id]

@router.get("/conversations", response_model=List[Conversation])
async def list_conversations(user_id: Optional[str] = None, limit: int = 10):
    """List conversations, optionally filtered by user_id"""
    if user_id:
        user_conversations = [
            conv for conv in conversations.values()
            if conv.user_id == user_id
        ]
        return user_conversations[:limit]
    else:
        return list(conversations.values())[:limit]

@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a conversation"""
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    del conversations[conversation_id]
    return {"message": "Conversation deleted successfully"}

@router.post("/conversations/{conversation_id}/clear")
async def clear_conversation(conversation_id: str):
    """Clear messages from a conversation"""
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    conversations[conversation_id].messages = []
    conversations[conversation_id].updated_at = datetime.now()
    
    return {"message": "Conversation cleared successfully"}

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "conversations_count": len(conversations)} 