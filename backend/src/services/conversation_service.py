from sqlmodel import Session, select
from datetime import datetime
from src.schema.models import Conversation, Message
from typing import List, Optional


class ConversationService:
    @staticmethod
    def create_conversation(session: Session, user_id: str) -> Conversation:
        """
        Initializes a new chat session for the user.

        Args:
            session: Database session
            user_id: ID of the user creating the conversation

        Returns:
            Conversation: The created conversation object
        """
        conversation = Conversation(
            user_id=user_id
        )
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation

    @staticmethod
    def add_message(session: Session, conversation_id: int, user_id: str, role: str, content: str) -> Message:
        """
        Saves a new message and updates the Conversation.updated_at timestamp.

        Args:
            session: Database session
            conversation_id: ID of the conversation
            user_id: ID of the user creating the message
            role: Role of the message sender ('user' or 'assistant')
            content: Content of the message

        Returns:
            Message: The created message object
        """
        # First, verify that the conversation belongs to the user
        conversation = session.get(Conversation, conversation_id)
        if not conversation or conversation.user_id != user_id:
            raise ValueError("Conversation not found or does not belong to the user")

        # Create the message
        message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
            content=content
        )
        session.add(message)

        # Update the conversation's updated_at timestamp
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)

        session.commit()
        session.refresh(message)
        return message

    @staticmethod
    def get_history(session: Session, conversation_id: int, user_id: str) -> List[Message]:
        """
        Retrieves all messages for a specific session, ensuring they belong to the user_id.

        Args:
            session: Database session
            conversation_id: ID of the conversation to retrieve
            user_id: ID of the user requesting the history

        Returns:
            List[Message]: List of messages in the conversation, ordered by creation time
        """
        # Verify that the conversation belongs to the user
        conversation = session.get(Conversation, conversation_id)
        if not conversation or conversation.user_id != user_id:
            raise ValueError("Conversation not found or does not belong to the user")

        # Retrieve all messages for the conversation, ordered by creation time
        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc())

        messages = session.exec(statement).all()
        return messages

    @staticmethod
    def list_conversations(session: Session, user_id: str) -> List[Conversation]:
        """
        Lists all chat sessions for a user, ordered by most recent.

        Args:
            session: Database session
            user_id: ID of the user whose conversations to list

        Returns:
            List[Conversation]: List of conversations for the user, ordered by most recent
        """
        statement = select(Conversation).where(
            Conversation.user_id == user_id
        ).order_by(Conversation.updated_at.desc())

        conversations = session.exec(statement).all()
        return conversations