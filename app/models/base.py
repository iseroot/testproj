from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Uuid
import uuid
from uuid import uuid5

class Base(DeclarativeBase):
    """
    Базовый класс для всех моделей.
    
    Зачем он нужен:
    1. Все модели наследуются от одного класса → легко управлять
    2. Автоматическое создание таблиц при запуске
    3. Единая обработка типов данных (UUID вместо строк)
    
    Что НЕ делает:
    - Не содержит абстрактных методов (нам это не нужно)
    - Не реализует бизнес-логику (только структура данных)
    """ 
    type_annotation_map = {
        uuid.UUID: Uuid
    }

    @staticmethod
    def generate_uuid() -> uuid.UUID:
        namespace = uuid.UUID('12345678-1234-5678-1234-567812345678')
        name = str(uuid.uuid4())
        return uuid5(namespace, name)

