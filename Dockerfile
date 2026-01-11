# 1. Базовый образ ВСЕГДА первый
FROM python:3.11-slim

# 2. Аргументы для настройки пользователя (должны быть после FROM)
ARG USER_ID=1000
ARG GROUP_ID=1000

# 3. Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# 4. Создание пользователя с правильными правами
RUN addgroup --gid $GROUP_ID vscode && \
    adduser --disabled-password --gecos "" --uid $USER_ID --gid $GROUP_ID vscode && \
    echo "vscode ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/vscode && \
    chmod 0440 /etc/sudoers.d/vscode

# 5. Рабочая директория
WORKDIR /app

# 6. Установка Python-зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 7. Переключение на пользователя vscode (безопасность!)
USER vscode

# 8. Копирование всего приложения
COPY . .

# 9. Экспозиция порта
EXPOSE 8000

# 10. Запуск приложения (последняя команда)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]