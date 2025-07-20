# Установка ComfyUI на сервере

## Требования к серверу

### Минимальные требования:
- **ОС**: Ubuntu 20.04+ или CentOS 8+
- **RAM**: 8 GB (рекомендуется 16 GB+)
- **CPU**: 4 ядра (рекомендуется 8+)
- **Диск**: 50 GB свободного места
- **GPU**: Опционально (для ускорения генерации)

### Рекомендуемые характеристики:
- **ОС**: Ubuntu 24.04 LTS
- **RAM**: 32 GB
- **CPU**: 16 ядер
- **Диск**: 100 GB SSD
- **GPU**: NVIDIA RTX 4090 или аналогичная

## Пошаговая установка

### 1. Подключение к серверу

```bash
# Подключение по SSH с ключом
ssh -i your-key.pem ubuntu@your-server-ip

# Проверка системы
uname -a
lsb_release -a
free -h
df -h
```

### 2. Обновление системы

```bash
# Обновление пакетов
sudo apt update && sudo apt upgrade -y

# Установка необходимых пакетов
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    wget \
    curl \
    unzip \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    nginx \
    supervisor \
    htop \
    nvtop \
    tree
```

### 3. Создание пользователя для ComfyUI

```bash
# Создание пользователя (если нужно)
sudo adduser comfyui
sudo usermod -aG sudo comfyui

# Переключение на пользователя
sudo su - comfyui
```

### 4. Установка Python и зависимостей

```bash
# Проверка версии Python
python3 --version

# Создание виртуального окружения
cd /home/ubuntu
python3 -m venv comfyui_env
source comfyui_env/bin/activate

# Обновление pip
pip install --upgrade pip setuptools wheel
```

### 5. Клонирование ComfyUI

```bash
# Клонирование репозитория
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI

# Установка зависимостей ComfyUI
pip install -r requirements.txt

# Установка дополнительных зависимостей
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install transformers diffusers accelerate
```

### 6. Установка моделей

```bash
# Создание директорий для моделей
mkdir -p models/checkpoints
mkdir -p models/loras
mkdir -p models/embeddings
mkdir -p models/vae
mkdir -p models/controlnet

# Скачивание базовой модели (пример)
cd models/checkpoints
wget https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned.safetensors

# Возврат в корневую директорию
cd /home/ubuntu/ComfyUI
```

### 7. Настройка конфигурации

```bash
# Создание конфигурационного файла
cat > extra_model_paths.yaml << 'EOF'
checkpoints: models/checkpoints
loras: models/loras
embeddings: models/embeddings
vae: models/vae
controlnet: models/controlnet
EOF

# Создание файла с переменными окружения
cat > .env << 'EOF'
PYTHONPATH=/home/ubuntu/ComfyUI
COMFYUI_PORT=8188
COMFYUI_HOST=0.0.0.0
COMFYUI_ENABLE_CORS=true
EOF
```

### 8. Создание systemd сервиса

```bash
# Создание сервисного файла
sudo tee /etc/systemd/system/comfyui.service > /dev/null << 'EOF'
[Unit]
Description=ComfyUI Service
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/ComfyUI
Environment=PATH=/home/ubuntu/comfyui_env/bin
ExecStart=/home/ubuntu/comfyui_env/bin/python main.py --listen 0.0.0.0 --port 8188 --enable-cors-header --cpu
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Перезагрузка systemd и включение сервиса
sudo systemctl daemon-reload
sudo systemctl enable comfyui.service
sudo systemctl start comfyui.service

# Проверка статуса
sudo systemctl status comfyui.service
```

### 9. Настройка Nginx (опционально)

```bash
# Создание конфигурации Nginx
sudo tee /etc/nginx/sites-available/comfyui << 'EOF'
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8188;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket поддержка
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
EOF

# Активация сайта
sudo ln -s /etc/nginx/sites-available/comfyui /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 10. Настройка файрвола

```bash
# Открытие портов
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8188/tcp

# Включение файрвола
sudo ufw enable
sudo ufw status
```

### 11. Проверка установки

```bash
# Проверка работы сервиса
sudo systemctl status comfyui.service

# Проверка логов
sudo journalctl -u comfyui.service -f

# Проверка доступности веб-интерфейса
curl -I http://localhost:8188

# Проверка процессов
ps aux | grep python
netstat -tlnp | grep 8188
```

## Управление сервисом

### Основные команды:

```bash
# Запуск сервиса
sudo systemctl start comfyui.service

# Остановка сервиса
sudo systemctl stop comfyui.service

# Перезапуск сервиса
sudo systemctl restart comfyui.service

# Проверка статуса
sudo systemctl status comfyui.service

# Просмотр логов
sudo journalctl -u comfyui.service -f

# Включение автозапуска
sudo systemctl enable comfyui.service

# Отключение автозапуска
sudo systemctl disable comfyui.service
```

### Мониторинг ресурсов:

```bash
# Мониторинг CPU и RAM
htop

# Мониторинг GPU (если есть)
nvtop

# Мониторинг диска
df -h

# Мониторинг процессов ComfyUI
ps aux | grep python
```

## Устранение неполадок

### Проблема: Сервис не запускается

```bash
# Проверка логов
sudo journalctl -u comfyui.service -n 50

# Проверка прав доступа
ls -la /home/ubuntu/ComfyUI/
ls -la /home/ubuntu/comfyui_env/

# Проверка зависимостей
source /home/ubuntu/comfyui_env/bin/activate
python -c "import torch; print(torch.__version__)"
```

### Проблема: Недостаточно памяти

```bash
# Проверка использования памяти
free -h

# Очистка кэша
sudo sync && sudo sysctl -w vm.drop_caches=3

# Настройка swap (если нужно)
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Проблема: Медленная работа

```bash
# Проверка CPU
top

# Проверка диска
iostat -x 1

# Оптимизация для CPU
# Добавить в systemd сервис:
# Environment=OMP_NUM_THREADS=4
# Environment=MKL_NUM_THREADS=4
```

## Обновление ComfyUI

```bash
# Остановка сервиса
sudo systemctl stop comfyui.service

# Обновление кода
cd /home/ubuntu/ComfyUI
git pull origin main

# Обновление зависимостей
source /home/ubuntu/comfyui_env/bin/activate
pip install -r requirements.txt --upgrade

# Запуск сервиса
sudo systemctl start comfyui.service
```

## Резервное копирование

```bash
# Создание бэкапа конфигурации
tar -czf comfyui_config_backup_$(date +%Y%m%d).tar.gz \
    /home/ubuntu/ComfyUI/extra_model_paths.yaml \
    /home/ubuntu/ComfyUI/.env \
    /etc/systemd/system/comfyui.service

# Создание бэкапа моделей
tar -czf comfyui_models_backup_$(date +%Y%m%d).tar.gz \
    /home/ubuntu/ComfyUI/models/
```

## Дополнительные настройки

### Оптимизация производительности:

```bash
# Настройка переменных окружения для оптимизации
cat >> /home/ubuntu/ComfyUI/.env << 'EOF'
# Оптимизация PyTorch
OMP_NUM_THREADS=4
MKL_NUM_THREADS=4
TORCH_NUM_THREADS=4

# Оптимизация памяти
PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:128
EOF
```

### Настройка мониторинга:

```bash
# Установка Prometheus Node Exporter
wget https://github.com/prometheus/node_exporter/releases/download/v1.6.1/node_exporter-1.6.1.linux-amd64.tar.gz
tar xvf node_exporter-1.6.1.linux-amd64.tar.gz
sudo mv node_exporter-1.6.1.linux-amd64/node_exporter /usr/local/bin/
```

## Заключение

После выполнения всех шагов ComfyUI будет доступен по адресу:
- **Локально**: http://localhost:8188
- **По сети**: http://your-server-ip:8188
- **Через домен**: http://your-domain.com (если настроен Nginx)

Сервис будет автоматически запускаться при перезагрузке сервера и перезапускаться при сбоях. 