from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, Optional
from sqlmodel import Session
from pydantic import BaseModel
from src.auth.jwt_auth import get_current_user, validate_user_access
from src.database.database import get_session
from src.services.conversation_service import ConversationService
from src.services.message_service import MessageService
from src.services.ai_agent_service import AIAgentService
from src.models.message_model import Message
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api", tags=["chat"])

# Global agent service instance
agent_service = AIAgentService()

# Define request model for chat endpoint
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None

@router.post("/{user_id}/chat")
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,  # Accept the request body as a Pydantic model
    current_user_id: str = Depends(get_current_user),
    db_session: Session = Depends(get_session)
) -> Dict[str, Any]:
    """
    Chat endpoint that accepts natural language requests and returns AI agent responses
    with tool call information.

    Args:
        user_id: ID of the user making the request (from path)
        request: ChatRequest containing the message and optional conversation_id
        current_user_id: ID of the user from JWT token (dependency)
        db_session: Database session (dependency)

    Returns:
        Dictionary with AI response, tool calls, and conversation information
    """
    try:
        # Validate that the user_id in the path matches the user_id from the token
        validate_user_access(user_id, current_user_id)

        # Extract message and conversation_id from the request body
        message = request.message
        conversation_id = request.conversation_id

        # Get or create conversation
        if conversation_id:
            # Verify the conversation belongs to the user
            conversation = ConversationService.get_conversation_by_id(conversation_id, db_session)
            if not conversation or conversation.user_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied: Invalid conversation ID"
                )
        else:
            # Create new conversation or get existing active one
            conversation = ConversationService.create_new_or_get_active_conversation(user_id, db_session)

        # Create user message in the conversation
        user_message = MessageService.create_user_message(message, conversation.id, db_session)

        # Get recent conversation history for context
        conversation_messages = MessageService.get_messages_by_conversation_ordered(conversation.id, db_session)

        # Format the conversation history for the AI agent
        formatted_history = agent_service.format_conversation_history(conversation_messages)

        # Process the message with the AI agent using conversation context
        result = await agent_service.enhance_with_conversation_context(
            user_message=message,
            conversation_id=conversation.id,
            user_id=user_id,
            db_session=db_session
        )

        # Create assistant message with the response
        assistant_message = MessageService.create_assistant_message(
            content=result.get("response", ""),
            conversation_id=conversation.id,
            db_session=db_session,
            tool_calls=result.get("tool_calls")
        )

        # Prepare the response
        response = {
            "success": True,
            "response": result.get("response", ""),
            "tool_calls": result.get("tool_calls", []),
            "conversation_id": conversation.id,
            "message_id": assistant_message.id
        }

        # Add tool results if they exist
        if "tool_results" in result:
            response["tool_results"] = result["tool_results"]

        return response

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/{user_id}/conversations/{conversation_id}")
async def get_conversation_endpoint(
    user_id: str,
    conversation_id: int,
    current_user_id: str = Depends(get_current_user),
    db_session: Session = Depends(get_session)
) -> Dict[str, Any]:
    """
    Get a specific conversation by ID for the authenticated user.

    Args:
        user_id: ID of the user making the request (from path)
        conversation_id: ID of the conversation to retrieve
        current_user_id: ID of the user from JWT token (dependency)
        db_session: Database session (dependency)

    Returns:
        Dictionary with conversation details
    """
    try:
        # Validate that the user_id in the path matches the user_id from the token
        validate_user_access(user_id, current_user_id)

        # Get the conversation
        conversation = ConversationService.get_conversation_by_id(conversation_id, db_session)

        if not conversation or str(conversation.user_id) != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found or does not belong to user"
            )

        # Get messages for this conversation
        conversation_messages = MessageService.get_messages_by_conversation_ordered(conversation_id, db_session)

        # Prepare response
        response = {
            "success": True,
            "conversation": {
                "id": conversation.id,
                "user_id": conversation.user_id,
                "messages": [
                    {
                        "id": msg.id,
                        "content": msg.content,
                        "role": msg.role,
                        "timestamp": msg.timestamp.isoformat() if msg.timestamp else None
                    }
                    for msg in conversation_messages
                ],
                "created_at": conversation.started_at.isoformat() if conversation.started_at else None,
                "updated_at": conversation.updated_at.isoformat() if conversation.updated_at else None,
                "status": getattr(conversation, 'status', 'active')
            }
        }

        return response

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error in get conversation endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
    """
    Chat endpoint that accepts natural language requests and returns AI agent responses
    with tool call information.

    Args:
        user_id: ID of the user making the request (from path)
        request: ChatRequest containing the message and optional conversation_id
        current_user_id: ID of the user from JWT token (dependency)
        db_session: Database session (dependency)

    Returns:
        Dictionary with AI response, tool calls, and conversation information
    """
    try:
        # Validate that the user_id in the path matches the user_id from the token
        validate_user_access(user_id, current_user_id)

        # Extract message and conversation_id from the request body
        message = request.message
        conversation_id = request.conversation_id

        # Get or create conversation
        if conversation_id:
            # Verify the conversation belongs to the user
            conversation = ConversationService.get_conversation_by_id(conversation_id, db_session)
            if not conversation or conversation.user_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied: Invalid conversation ID"
                )
        else:
            # Create new conversation or get existing active one
            conversation = ConversationService.create_new_or_get_active_conversation(user_id, db_session)

        # Create user message in the conversation
        user_message = MessageService.create_user_message(message, conversation.id, db_session)

        # Get recent conversation history for context
        conversation_messages = MessageService.get_messages_by_conversation_ordered(conversation.id, db_session)

        # Format the conversation history for the AI agent
        formatted_history = agent_service.format_conversation_history(conversation_messages)

        # Process the message with the AI agent using conversation context
        result = await agent_service.enhance_with_conversation_context(
            user_message=message,
            conversation_id=conversation.id,
            user_id=user_id,
            db_session=db_session
        )

        # Create assistant message with the response
        assistant_message = MessageService.create_assistant_message(
            content=result.get("response", ""),
            conversation_id=conversation.id,
            db_session=db_session,
            tool_calls=result.get("tool_calls")
        )

        # Prepare the response
        response = {
            "success": True,
            "response": result.get("response", ""),
            "tool_calls": result.get("tool_calls", []),
            "conversation_id": conversation.id,
            "message_id": assistant_message.id
        }

        # Add tool results if they exist
        if "tool_results" in result:
            response["tool_results"] = result["tool_results"]

        return response

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


