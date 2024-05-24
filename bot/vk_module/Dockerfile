# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Добавляем текущую директорию в PYTHONPATH
ENV PYTHONPATH=/app

# Копируем файл зависимостей
COPY bot/vk_module/requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код бота
COPY bot/ /app/bot

# Команда для запуска бота
CMD ["python", "bot/vk_module/start_vk_bot.py"]
