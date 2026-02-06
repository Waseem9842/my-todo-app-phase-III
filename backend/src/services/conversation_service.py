from typing import List, Optional
from sqlmodel import Session, select
from datetime import datetime
from fastapi import HTTPException, status
from src.models.conversation_model import Conversation, ConversationCreate, ConversationRead


class ConversationService:
    """
    Service class for handling CRUD operations on conversations with user isolation validation.
    """

    @staticmethod
    def create_conversation(conversation_data: ConversationCreate, db_session: Session) -> Conversation:
        """
        Create a new conversation with the given data.

        Args:
            conversation_data: ConversationCreate object containing conversation information
            db_session: Database session

        Returns:
            Created Conversation object
        """
        conversation = Conversation(
            user_id=conversation_data.user_id,
            status="active"
        )
        db_session.add(conversation)
        db_session.commit()
        db_session.refresh(conversation)
        return conversation

    @staticmethod
    def get_conversation_by_id(conversation_id: int, db_session: Session) -> Optional[Conversation]:
        """
        Get a specific conversation by its ID.

        Args:
            conversation_id: ID of the conversation to retrieve
            db_session: Database session

        Returns:
            Conversation object if found, None otherwise
        """
        statement = select(Conversation).where(Conversation.id == conversation_id)
        conversation = db_session.exec(statement).first()
        return conversation

    @staticmethod
    def get_conversations_by_user(user_id: str, db_session: Session) -> List[Conversation]:
        """
        Get all conversations for a specific user.

        Args:
            user_id: ID of the user whose conversations to retrieve
            db_session: Database session

        Returns:
            List of Conversation objects belonging to the user
        """
        statement = select(Conversation).where(Conversation.user_id == user_id)
        conversations = db_session.exec(statement).all()
        return conversations

    @staticmethod
    def update_conversation_status(conversation_id: int, new_status: str, db_session: Session) -> Optional[Conversation]:
        """
        Update the status of a conversation.

        Args:
            conversation_id: ID of the conversation to update
            new_status: New status for the conversation
            db_session: Database session

        Returns:
            Updated Conversation object if successful, None if not found
        """
        conversation = ConversationService.get_conversation_by_id(conversation_id, db_session)
        if not conversation:
            return None

        conversation.status = new_status
        conversation.updated_at = datetime.utcnow()
        db_session.add(conversation)
        db_session.commit()
        db_session.refresh(conversation)
        return conversation

    @staticmethod
    def get_active_conversation_for_user(user_id: str, db_session: Session) -> Optional[Conversation]:
        """
        Get the active conversation for a specific user.

        Args:
            user_id: ID of the user whose active conversation to retrieve
            db_session: Database session

        Returns:
            Active Conversation object if found, None otherwise
        """
        statement = select(Conversation).where(
            Conversation.user_id == user_id,
            Conversation.status == "active"
        )
        conversation = db_session.exec(statement).first()
        return conversation

    @staticmethod
    def create_new_or_get_active_conversation(user_id: str, db_session: Session) -> Conversation:
        """
        Create a new conversation for a user or return existing active conversation.

        Args:
            user_id: ID of the user requesting conversation
            db_session: Database session

        Returns:
            Active Conversation object (either new or existing)
        """
        # Check if user already has an active conversation
        active_conversation = ConversationService.get_active_conversation_for_user(user_id, db_session)

        if active_conversation:
            return active_conversation

        # Create a new conversation if no active one exists
        conversation_data = ConversationCreate(user_id=user_id)
        new_conversation = ConversationService.create_conversation(conversation_data, db_session)
        return new_conversation

    @staticmethod
    def validate_user_conversation_access(conversation_id: int, user_id: str, db_session: Session) -> bool:
        """
        Validate that a user has access to a specific conversation.

        Args:
            conversation_id: ID of the conversation to validate access to
            user_id: ID of the user requesting access
            db_session: Database session

        Returns:
            True if user has access, raises HTTPException otherwise
        """
        conversation = ConversationService.get_conversation_by_id(conversation_id, db_session)

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )

        if conversation.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You don't have permission to access this conversation"
            )

        return True