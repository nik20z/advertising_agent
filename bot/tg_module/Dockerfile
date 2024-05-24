# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Добавляем текущую директорию в PYTHONPATH
ENV PYTHONPATH=/app

# Копируем файл зависимостей
COPY bot/tg_module/requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код бота
COPY bot/ /app/bot

# Команда для запуска бота
CMD ["python", "bot/tg_module/start_telegram_bot.py"]
