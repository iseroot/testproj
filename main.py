from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session
from app.database import get_db, engine
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from uuid import UUID

User.metadata.create_all(bind=engine)

app = FastAPI(
    title='M P Api',
    description='REST API'
)

@app.get("/", include_in_schema=False)
def root():
    return {
        "message": "API работает!",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "openapi_url": "/openapi.json"
    }

@app.post(
    "/users/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary='Регистрация нового пользователя'
)
def register_user(
    user_create: UserCreate,
    db: Session = Depends(get_db)
):
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)

    try:
        return auth_service.register_user(user_create)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
@app.get(
    "/users/{user_id}",
    response_model=UserRead,
    summary="Получение пользователя по ID",
    responses={404: {"description": "Пользователь не найден"}}
)
def get_user(
    user_id: UUID, # <--------------------ТУТ ПОСМОТРЕТЬ 
    db: Session = Depends(get_db)
):
    user_repo = UserRepository(db)
    user = user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    return user

@app.post('/login',
          response_model=UserRead,
          summary='Аутентификация пользователя',
          description='Проверяет email и пароль, возвращает данные пользователя',
          responses={
              401: {"description": "Неверный email или пароль"},
              404: {"description": "Пользователь не найден"}
          })
def login(
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    user_repo = UserRepository(db)
    user = user_repo.get_by_email(email.lower())

    if not user or not user.verify_password(password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверный пороль или емаил',
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user

@app.patch(
    "/users/{user_id}",
    response_model=UserRead,  # ← Безопасно! Без пароля в ответе
    summary="Частичное обновление пользователя",
    description="Обновляет указанные поля пользователя. Пароль хешируется автоматически.",
    responses={
        404: {"description": "Пользователь не найден"},
        400: {"description": "Неверные данные (дубликат email, слабый пароль)"}
    }
)
def update_user(
    user_id: UUID,
    user_update: UserUpdate,  # ← Pydantic автоматически валидирует
    db: Session = Depends(get_db)
):
    repo = UserRepository(db)

    up_data = {k: v for k, v in user_update.model_dump().items() if v is not None}

    try:
        up_user = repo.update(user_id, up_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    if not up_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='user not found'
        )

