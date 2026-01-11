from app.database import SessionLocal, engine
from app.models.user import User
from app.repositories.user_repository import UserRepository
from sqlmodel import SQLModel
import time
from app.models.gender import Gender
from uuid import uuid4

# Создаем таблицы если нужно
SQLModel.metadata.create_all(engine)

# Создаем сессию
db = SessionLocal()
repo = UserRepository(db)


# Измеряем время поиска
print("Измеряем время поиска user999@example.com...")
start = time.time()
user = repo.get_by_email("user999@example.com")
elapsed = time.time() - start
print(f"⏱️  Время поиска: {elapsed:.6f} сек")

if user:
    print(f"✅ Пользователь найден: {user.email}, ID: {user.id}")
    print(f"   Username: {user.username}, Gender: {user.gender.value}")
else:
    print("❌ Пользователь не найден")

# ОЧИЩАЕМ ДАННЫЕ!
print("Очищаем тестовые данные...")
db.query(User).filter(User.email.like('user%@example.com')).delete()
db.commit()
print("✅ Тестовые данные удалены")

# Закрываем сессию
db.close()
print("✅ Тест завершен успешно")