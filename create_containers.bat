@echo off
setlocal

REM Устанавливаем кодировку UTF-8 для поддержки русского языка
chcp 65001 >nul

REM Проверка, запущен ли Docker
docker info >nul 2>&1
if errorlevel 1 (
    echo Docker не установлен или не запущен. Пожалуйста, установите и запустите Docker.
    pause
    exit /b 1
)

REM Пересборка контейнеров
docker-compose build

REM Проверка, существует ли контейнер vk_bot
docker ps -a --format "{{.Names}}" | findstr /i "vk_bot" >nul
if errorlevel 1 (
    echo Контейнер vk_bot не найден. Создание контейнера...
    docker-compose up -d vk_bot
) else (
    echo Контейнер vk_bot уже существует. Пересборка...
    docker-compose up -d --build vk_bot
)

REM Проверка, существует ли контейнер tg_bot
docker ps -a --format "{{.Names}}" | findstr /i "tg_bot" >nul
if errorlevel 1 (
    echo Контейнер tg_bot не найден. Создание контейнера...
    docker-compose up -d tg_bot
) else (
    echo Контейнер tg_bot уже существует. Пересборка...
    docker-compose up -d --build tg_bot
)

echo Скрипт завершен. Закройте это окно, нажав любую клавишу.
pause
