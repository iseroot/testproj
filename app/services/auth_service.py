from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserRead
from fastapi import HTTPException

class AuthService:

    def __init__(self, user_repo: UserRepository):

        self.user_repo = user_repo

    def register_user(self, user_create: UserCreate) -> UserRead:
        try:
            user = self.user_repo.create(user_create)
            user_data = {
            "id": str(user.id),
            "email": user.email,
            "username": user.username,
            "gender": user.gender,
            "created_at": user.created_at
        }
            return UserRead(**user_data)
        except Exception as e:
            print(f'Ошибка: {str(e)}')
            raise HTTPException(
                status_code=500
            )
        