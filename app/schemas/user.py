from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from datetime import datetime
from typing import Optional
from enum import Enum
import re
from uuid import UUID
class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class UserBase(BaseModel):
    email: EmailStr = Field(
        description="Электронная почта в формате user@domain.com",
        examples=["user@example.com"]
    )
    gender: Gender = Field(
        default=Gender.OTHER,
        description="Пол пользователя: male, female, other"
    )
    
    @field_validator('email')
    @classmethod
    def validate_email_domain(cls, v: str) -> str:
        allowed_domains = ["example.com", "test.com", "localhost"]
        domain = v.split('@')[-1]
        if domain not in allowed_domains:
            raise ValueError(
                f"Домен {domain} не разрешен. "
                f"Разрешены: {', '.join(allowed_domains)}"
            )
        return v.lower()

class UserCreate(UserBase):
    username: str = Field(
        min_length=3,
        max_length=15
    )

    password: str = Field(
        min_length=8,
        description="Пароль (минимум 8 символов, включая заглавные буквы, цифры и спецсимволы)",
        examples=["SecurePass123!"]
    )
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not re.search(r'[A-Z]', v):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву")
        if not re.search(r'[a-z]', v):
            raise ValueError("Пароль должен содержать хотя бы одну строчную букву")
        if not re.search(r'[0-9]', v):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError("Пароль должен содержать хотя бы один спецсимвол")
        return v

class UserRead(UserBase):
    username: str = Field(
        description='name'
    )
    id: UUID = Field(
        description="Уникальный ID пользователя (UUID)"
    )
    created_at: datetime = Field(
        description="Время создания в формате ISO 8601"
    )
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "2d3a8c4c-5ab7-5a3b-9e1d-3c4a6b8d9e0f",
                "email": "user@example.com",
                "gender": "male",
                "created_at": "2025-12-26T15:30:45.123456+00:00"
            }
        }
    )

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    gender: Optional[Gender] = None
    password: Optional[str] = None
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        if not re.search(r'[A-Z]', v):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву")
        if not re.search(r'[a-z]', v):
            raise ValueError("Пароль должен содержать хотя бы одну строчную букву")
        if not re.search(r'[0-9]', v):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError("Пароль должен содержать хотя бы один спецсимвол")
        return v
    
    # ИСПРАВЛЕНО: правильный синтаксис для примера в Pydantic v2
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "new@example.com",
                "gender": "female",
                "password": "NewSecurePass123!"
            }
        }
    )





