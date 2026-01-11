from sqlmodel import SQLModel, Field
from .base import Base
from datetime import datetime, timezone
from typing import Optional
from argon2 import PasswordHasher
import uuid
from .gender import Gender
PH = PasswordHasher(
    time_cost=2,
    memory_cost=65536,
    parallelism=2,
    hash_len=32,
    salt_len=16
)

class User(SQLModel, table=True):

    __tablename__ = 'users'

    id: uuid.UUID = Field(
        default_factory=Base.generate_uuid,
        primary_key=True,
        description='unique users id'
    )

    email: str = Field(
        unique=True,
        index=True,
        nullable=False,
        max_length=70,
        description='Users Email(unique)'
    )

    username: str = Field(
        unique=True,
        nullable=False,
        max_length=20,
        description='username'
    )

    gender: Gender = Field(
        nullable=False,
        description='user gender'
    )
    
    password_hash: str = Field(
        nullable=False,
        description='pass hash'
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        description='created time'
    )

    def set_password(self, password: str) -> None:
        self.password_hash = PH.hash(password)
    
    def verify_password(self, password: str) -> bool:

        try:
            verified = PH.verify(self.password_hash, password)
            if verified and PH.check_needs_rehash(self.password_hash):
                self.password_hash = PH.hash(password)
            return verified
        except Exception:
            return False
