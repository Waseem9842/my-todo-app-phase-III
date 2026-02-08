from sqlmodel import Session, select
from src.models.user_model import User, UserCreate
from passlib.context import CryptContext
from typing import Optional

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    @staticmethod
    def get_user_by_id(session: Session, user_id: int) -> Optional[User]:
        """Get a user by their ID."""
        return session.exec(select(User).where(User.id == user_id)).first()

    @staticmethod
    def get_user_by_email(session: Session, email: str) -> Optional[User]:
        """Get a user by their email."""
        return session.exec(select(User).where(User.email == email)).first()

    @staticmethod
    def create_user(session: Session, user_create: UserCreate) -> User:
        """Create a new user with hashed password."""
        # Truncate password to 72 characters to comply with bcrypt limitations
        password = user_create.password
        
        # First check the byte length since bcrypt has a 72-byte limit
        if len(password.encode('utf-8')) > 72:
            # Truncate to 72 bytes while preserving multi-byte character integrity
            password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
        elif len(password) > 72:  # Then check the character length
            password = password[:72]

        # Hash the password
        hashed_password = pwd_context.hash(password)

        # Create user object
        db_user = User(
            email=user_create.email,
            name=user_create.name,
            hashed_password=hashed_password
        )

        # Add to session and commit
        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return db_user

    @staticmethod
    def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
        """Authenticate a user by email and password."""
        user = UserService.get_user_by_email(session, email)
        if not user:
            return None

        # Truncate password to 72 characters to comply with bcrypt limitations
        truncated_password = password
        
        # First check the byte length since bcrypt has a 72-byte limit
        if len(password.encode('utf-8')) > 72:
            # Truncate to 72 bytes while preserving multi-byte character integrity
            truncated_password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
        elif len(password) > 72:  # Then check the character length
            truncated_password = password[:72]

        # Verify password
        if not pwd_context.verify(truncated_password, user.hashed_password):
            return None

        return user

    @staticmethod
    def update_user(session: Session, user_id: int, user_update: dict) -> Optional[User]:
        """Update a user's information."""
        user = UserService.get_user_by_id(session, user_id)
        if not user:
            return None

        # Update user attributes
        for key, value in user_update.items():
            if hasattr(user, key):
                setattr(user, key, value)

        session.add(user)
        session.commit()
        session.refresh(user)

        return user

    @staticmethod
    def delete_user(session: Session, user_id: int) -> bool:
        """Delete a user by ID."""
        user = UserService.get_user_by_id(session, user_id)
        if not user:
            return False

        session.delete(user)
        session.commit()
        return True