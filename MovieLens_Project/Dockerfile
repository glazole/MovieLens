# Используем официальный Python-образ
FROM python:3.10-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы проекта
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Пробрасываем порт, на котором работает Dash
EXPOSE 8050

# Запускаем приложение
CMD ["python", "app.py"]
