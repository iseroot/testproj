from sqlmodel import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Выбираем файл окружения вручную, чтобы переключаться между local и docker.
env_file = os.getenv("ENV_FILE")
app_env = os.getenv("APP_ENV", "").lower()

if not env_file:
    if app_env == "docker":
        env_file = ".env.docker"
    elif app_env == "local":
        env_file = ".env.local"
    else:
        env_file = ".env"

load_dotenv(env_file)

# 1. ПРАВИЛЬНЫЙ URL для psycopg3 (без "2" в конце!)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://user:password@db:5432/appdb"  # ← psycopg вместо psycopg2
)

# 2. Создаем движок
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    connect_args={
        'keepalives': 1,
        'keepalives_idle': 30,
        'keepalives_interval': 10,
        'keepalives_count': 5,
    }
)

# 3. Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Dependency для FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
