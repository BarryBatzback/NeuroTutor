# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Копируем зависимости
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Устанавливаем зависимости проекта
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт
EXPOSE 8000

# Запускаем сервер
CMD ["python", "backend/main.py"]