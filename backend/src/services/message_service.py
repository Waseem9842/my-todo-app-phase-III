from typing import List, Optional, Dict, Any
from sqlmodel import Session, select
from datetime import datetime
from fastapi import HTTPException, status
from src.models.message_model import Message, MessageCreate, MessageRead


class MessageService:
    """
    Service class for handling CRUD operations on messages with conversation validation.
    """

    @staticmethod
    def create_message(message_data: MessageCreate, db_session: Session) -> Message:
        """
        Create a new message with the given data.

        Args:
            message_data: MessageCreate object containing message information
            db_session: Database session

        Returns:
            Created Message object
        """
        message = Message(
            conversation_id=message_data.conversation_id,
            role=message_data.role,
            content=message_data.content
        )
        db_session.add(message)
        db_session.commit()
        db_session.refresh(message)
        return message

    @staticmethod
    def get_message_by_id(message_id: int, db_session: Session) -> Optional[Message]:
        """
        Get a specific message by its ID.

        Args:
            message_id: ID of the message to retrieve
            db_session: Database session

        Returns:
            Message object if found, None otherwise
        """
        statement = select(Message).where(Message.id == message_id)
        message = db_session.exec(statement).first()
        return message

    @staticmethod
    def get_messages_by_conversation(conversation_id: int, db_session: Session) -> List[Message]:
        """
        Get all messages for a specific conversation.

        Args:
            conversation_id: ID of the conversation whose messages to retrieve
            db_session: Database session

        Returns:
            List of Message objects belonging to the conversation
        """
        statement = select(Message).where(Message.conversation_id == conversation_id)
        messages = db_session.exec(statement).all()
        return messages

    @staticmethod
    def get_messages_by_conversation_ordered(conversation_id: int, db_session: Session) -> List[Message]:
        """
        Get all messages for a specific conversation ordered by timestamp.

        Args:
            conversation_id: ID of the conversation whose messages to retrieve
            db_session: Database session

        Returns:
            List of Message objects belonging to the conversation, ordered by timestamp
        """
        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.timestamp.asc())
        messages = db_session.exec(statement).all()
        return messages

    @staticmethod
    def update_message_content(message_id: int, new_content: str, db_session: Session) -> Optional[Message]:
        """
        Update the content of a message.

        Args:
            message_id: ID of the message to update
            new_content: New content for the message
            db_session: Database session

        Returns:
            Updated Message object if successful, None if not found
        """
        message = MessageService.get_message_by_id(message_id, db_session)
        if not message:
            return None

        message.content = new_content
        message.timestamp = datetime.utcnow()
        db_session.add(message)
        db_session.commit()
        db_session.refresh(message)
        return message

    @staticmethod
    def create_user_message(content: str, conversation_id: int, db_session: Session) -> Message:
        """
        Create a new user message in a conversation.

        Args:
            content: Content of the message
            conversation_id: ID of the conversation to add message to
            db_session: Database session

        Returns:
            Created Message object
        """
        message_data = MessageCreate(
            conversation_id=conversation_id,
            role="user",
            content=content
        )
        return MessageService.create_message(message_data, db_session)

    @staticmethod
    def create_assistant_message(content: str, conversation_id: int, db_session: Session, tool_calls: Optional[Dict[str, Any]] = None) -> Message:
        """
        Create a new assistant message in a conversation.

        Args:
            content: Content of the message
            conversation_id: ID of the conversation to add message to
            db_session: Database session
            tool_calls: Optional tool calls made by the assistant

        Returns:
            Created Message object
        """
        message_data = MessageCreate(
            conversation_id=conversation_id,
            role="assistant",
            content=content
        )

        # Create the message first
        message = MessageService.create_message(message_data, db_session)

        # If there are tool calls, update the message to include them
        if tool_calls:
            message.tool_calls = tool_calls
            db_session.add(message)
            db_session.commit()
            db_session.refresh(message)

        return message

    @staticmethod
    def validate_user_message_access(message_id: int, user_id: str, db_session: Session) -> bool:
        """
        Validate that a user has access to a specific message.

        Args:
            message_id: ID of the message to validate access to
            user_id: ID of the user requesting access
            db_session: Database session

        Returns:
            True if user has access, raises HTTPException otherwise
        """
        message = MessageService.get_message_by_id(message_id, db_session)

        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found"
            )

        # Get the conversation this message belongs to
        from src.services.conversation_service import ConversationService
        conversation = ConversationService.get_conversation_by_id(message.conversation_id, db_session)

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation for message not found"
            )

        if conversation.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You don't have permission to access this message"
            )

        return True