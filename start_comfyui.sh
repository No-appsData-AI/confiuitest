#!/bin/bash

# Скрипт для запуска ComfyUI на сервере
# Автор: AI Assistant
# Дата: $(date)

# Переходим в директорию ComfyUI
cd /home/ubuntu/ComfyUI

# Активируем виртуальное окружение
source venv/bin/activate

# Запускаем ComfyUI с параметрами для сервера
# --listen 0.0.0.0 - слушаем на всех интерфейсах
# --port 8188 - порт по умолчанию
# --enable-cors-header - разрешаем CORS для веб-интерфейса
# --cpu - используем CPU (так как нет GPU)
python main.py --listen 0.0.0.0 --port 8188 --enable-cors-header --cpu 