from sqlmodel import Session, select
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User
from typing import Optional
import uuid
from app.models.gender import Gender

class UserRepository:
    """
    Репозиторий для работы с пользователями (CRUD операции).
    
    Использует совместимый синтаксис для разных версий SQLModel.
    """
    
    def __init__(self, session: Session):
        self.session = session
    
    def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """Получить пользователя по ID."""
        return self.session.get(User, user_id)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Получить пользователя по email."""
        statement = select(User).where(User.email == email)
        
        # Совместимый синтаксис для разных версий SQLModel
        try:
            # Попробуем новый синтаксис (SQLModel 0.0.8+)
            return self.session.exec(statement).first()
        except AttributeError:
            # Используем старый синтаксис (SQLAlchemy 1.4+)
            result = self.session.execute(statement)
            return result.scalars().first()
    
    def create(self, user_create: UserCreate) -> User:
        """
        Создать нового пользователя.
        
        Упрощенная версия для теста (без валидации).
        """
        # Проверяем уникальность email
        if self.get_by_email(user_create.email):
            raise ValueError("Пользователь с таким email уже существует")
        
        # Создаем объект пользователя
        user = User(
            email=user_create.email.lower(),
            username=user_create.username,
            gender=user_create.gender
        )
        
        # Хешируем пароль
        user.set_password(user_create.password)
        
        # Сохраняем в БД
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        
        return user
    
    def update(self, user_id: uuid.UUID, user_update: dict) -> User:
        
        db_user = self.get_by_id(user_id)
        if not db_user:
            return None
        
        if 'email' in user_update and user_update['email'].lower() != db_user.email:
            new_email = user_update['email'].lower()
            if self.get_by_email(new_email):
                raise ValueError(f'Error {new_email} uncorrect')
        
        for k, v in user_update.items():
            if k == 'password' and v:
                db_user.set_password(v)
            elif k == 'email' and v:
                setattr(db_user, k, v.lower())
            elif hasattr(db_user, k):
                setattr(db_user, k, v)
        
        self.session.commit()
        self.session.refresh(db_user)

        return db_user