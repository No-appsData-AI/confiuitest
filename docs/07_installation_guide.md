# Руководство по установке ComfyUI Integration

## Обзор

Это руководство поможет вам установить и настроить все компоненты ComfyUI Integration, включая Pipeline Builder, S3 Storage Integration и OpenAI Integration.

## Системные требования

### Минимальные требования
- **ОС**: Ubuntu 20.04+ / CentOS 8+ / macOS 10.15+
- **Python**: 3.8+
- **RAM**: 4GB+
- **Дисковое пространство**: 10GB+
- **Сеть**: Доступ к интернету

### Рекомендуемые требования
- **ОС**: Ubuntu 22.04 LTS
- **Python**: 3.10+
- **RAM**: 8GB+
- **Дисковое пространство**: 20GB+
- **GPU**: NVIDIA GPU с 8GB+ VRAM (опционально)

## Предварительная подготовка

### 1. Обновление системы

```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade -y

# CentOS/RHEL
sudo yum update -y

# macOS
brew update && brew upgrade
```

### 2. Установка базовых зависимостей

```bash
# Ubuntu/Debian
sudo apt install -y python3 python3-pip python3-venv git wget curl build-essential python3-dev

# CentOS/RHEL
sudo yum install -y python3 python3-pip git wget curl gcc python3-devel

# macOS
brew install python3 git wget curl
```

### 3. Установка ComfyUI

```bash
# Клонирование ComfyUI
cd /home/ubuntu
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI

# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate

# Установка PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Установка зависимостей ComfyUI
pip install -r requirements.txt
```

## Установка ComfyUI Integration

### Автоматическая установка (рекомендуется)

Используйте комплексный скрипт установки:

```bash
# Клонирование репозитория
git clone https://github.com/your-repo/confiuitest.git
cd confiuitest

# Установка на локальную машину
./scripts/install_all_components.sh /home/ubuntu/ComfyUI localhost

# Установка на удаленный сервер
./scripts/install_all_components.sh /home/ubuntu/ComfyUI 34.245.10.81
```

### Ручная установка

Если автоматическая установка не подходит, выполните установку вручную:

#### 1. Установка Pipeline Builder

```bash
# Запуск скрипта установки Pipeline Builder
./scripts/install_pipeline_builder_server.sh /home/ubuntu/ComfyUI
```

#### 2. Установка S3 Storage узлов

```bash
# Запуск скрипта установки S3 узлов
./scripts/install_s3_nodes_server.sh /home/ubuntu/ComfyUI
```

#### 3. Установка OpenAI узлов

```bash
# Запуск скрипта установки OpenAI узлов
./scripts/install_openai_node_server.sh /home/ubuntu/ComfyUI
```

## Настройка переменных окружения

### 1. Создание файла .env

```bash
cd /home/ubuntu/ComfyUI
nano .env
```

### 2. Настройка переменных

```bash
# ComfyUI Configuration
COMFYUI_URL=http://localhost:8188
COMFYUI_PORT=8188

# AWS S3 Configuration
AWS_ACCESS_KEY_ID=your-access-key-here
AWS_SECRET_ACCESS_KEY=your-secret-key-here
AWS_REGION=us-east-1
S3_BUCKET=comfyui-images

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here

# Pipeline Builder Configuration
PIPELINE_BUILDER_LOG_LEVEL=INFO
PIPELINE_BUILDER_TIMEOUT=300

# Development Configuration
DEBUG=false
LOG_LEVEL=INFO
```

### 3. Получение API ключей

#### AWS S3
1. Войдите в [AWS Console](https://console.aws.amazon.com/)
2. Перейдите в IAM → Users → Create User
3. Привяжите политику `AmazonS3FullAccess`
4. Создайте Access Key и Secret Access Key
5. Создайте S3 bucket для хранения изображений

#### OpenAI
1. Войдите в [OpenAI Platform](https://platform.openai.com/)
2. Перейдите в API Keys
3. Создайте новый API ключ
4. Скопируйте ключ в переменную `OPENAI_API_KEY`

## Настройка systemd сервиса

### 1. Создание сервисного файла

```bash
sudo nano /etc/systemd/system/comfyui.service
```

### 2. Содержимое файла

```ini
[Unit]
Description=ComfyUI Service
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/ComfyUI
Environment=PATH=/home/ubuntu/ComfyUI/venv/bin
ExecStart=/home/ubuntu/ComfyUI/venv/bin/python main.py --listen 0.0.0.0 --port 8188
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 3. Активация сервиса

```bash
sudo systemctl daemon-reload
sudo systemctl enable comfyui.service
sudo systemctl start comfyui.service
```

## Проверка установки

### 1. Запуск тестов

```bash
cd /home/ubuntu/ComfyUI
./manage_comfyui.sh test
```

### 2. Проверка состояния системы

```bash
./manage_comfyui.sh health
```

### 3. Проверка статуса сервиса

```bash
./manage_comfyui.sh status
```

### 4. Просмотр логов

```bash
./manage_comfyui.sh logs
```

## Управление системой

### Основные команды

```bash
# Управление ComfyUI
./manage_comfyui.sh start      # Запуск
./manage_comfyui.sh stop       # Остановка
./manage_comfyui.sh restart    # Перезапуск
./manage_comfyui.sh status     # Статус
./manage_comfyui.sh logs       # Логи

# Проверка состояния
./manage_comfyui.sh health     # Проверка здоровья
./manage_comfyui.sh test       # Запуск тестов

# Управление пайплайнами
./manage_comfyui.sh pipeline create openai "Beautiful sunset"
./manage_comfyui.sh pipeline test my_pipeline.json
./manage_comfyui.sh pipeline list

# Документация и конфигурация
./manage_comfyui.sh docs       # Открыть документацию
./manage_comfyui.sh config     # Редактировать конфигурацию
```

### Справка

```bash
./manage_comfyui.sh help
```

## Использование Pipeline Builder

### 1. Создание простого пайплайна

```python
from examples.comfyui_pipeline_builder import ComfyUIPipelineBuilder

# Создание строителя
builder = ComfyUIPipelineBuilder("http://localhost:8188")

# Добавление узла OpenAI
openai_node = builder.add_node(
    node_type="OpenAIImageGenerator",
    inputs={
        "prompt": "A beautiful sunset over mountains",
        "model": "dall-e-3",
        "size": "1024x1024"
    }
)

# Добавление узла предварительного просмотра
preview_node = builder.add_node(
    node_type="PreviewImage",
    inputs={}
)

# Соединение узлов
builder.connect_nodes(openai_node, 0, preview_node, 0)

# Сохранение пайплайна
builder.save_workflow("sunset_pipeline.json")
```

### 2. Использование шаблонов

```python
from examples.comfyui_pipeline_builder import PipelineTemplates

# Создание пайплайна OpenAI -> S3
builder = PipelineTemplates.openai_to_s3_pipeline(
    prompt="Futuristic city",
    bucket_name="my-images"
)

# Сохранение
builder.save_workflow("futuristic_city_pipeline.json")
```

### 3. Использование Pipeline Manager

```python
from examples.pipeline_manager import PipelineManager

# Создание менеджера
manager = PipelineManager("http://localhost:8188")

# Создание сложного пайплайна
pipeline = manager.create_complex_pipeline(
    prompt="Dragon over castle",
    bucket_name="my-images"
)

# Валидация и выполнение
validation = manager.validate_pipeline(pipeline)
if validation["valid"]:
    result = manager.execute_pipeline(pipeline, "Dragon Pipeline")
    print(f"Результат: {result}")
```

## CLI интерфейс

### Создание пайплайнов

```bash
# OpenAI пайплайн
./manage_comfyui.sh pipeline create openai "Beautiful landscape"

# S3 пайплайн
./manage_comfyui.sh pipeline create s3 my-bucket

# Сложный пайплайн
./manage_comfyui.sh pipeline create complex "Futuristic city" my-bucket
```

### Тестирование пайплайнов

```bash
# Тест пайплайна
./manage_comfyui.sh pipeline test my_pipeline.json

# Список доступных узлов
./manage_comfyui.sh pipeline list
```

## Мониторинг и обслуживание

### 1. Мониторинг ресурсов

```bash
# Использование CPU и RAM
htop

# Использование диска
df -h

# Использование сети
iftop
```

### 2. Просмотр логов

```bash
# Логи ComfyUI
sudo journalctl -u comfyui.service -f

# Логи системы
sudo journalctl -f

# Логи приложения
tail -f /home/ubuntu/ComfyUI/logs/app.log
```

### 3. Резервное копирование

```bash
# Создание резервной копии
tar -czf comfyui_backup_$(date +%Y%m%d).tar.gz /home/ubuntu/ComfyUI

# Восстановление из резервной копии
tar -xzf comfyui_backup_20241201.tar.gz -C /
```

## Устранение неполадок

### Проблемы с установкой

#### Ошибка импорта модулей
```bash
# Проверка зависимостей
pip list | grep -E "(requests|boto3|openai)"

# Переустановка зависимостей
pip install -r requirements.txt --force-reinstall
```

#### Ошибка доступа к файлам
```bash
# Установка прав доступа
sudo chown -R ubuntu:ubuntu /home/ubuntu/ComfyUI
sudo chmod -R 755 /home/ubuntu/ComfyUI
```

### Проблемы с ComfyUI

#### Сервис не запускается
```bash
# Проверка статуса
sudo systemctl status comfyui.service

# Просмотр логов
sudo journalctl -u comfyui.service -n 50

# Проверка конфигурации
sudo systemctl cat comfyui.service
```

#### Проблемы с доступом
```bash
# Проверка порта
netstat -tlnp | grep 8188

# Проверка firewall
sudo ufw status

# Открытие порта
sudo ufw allow 8188
```

### Проблемы с внешними сервисами

#### AWS S3
```bash
# Проверка ключей
aws s3 ls s3://your-bucket --profile default

# Тест подключения
python3 -c "
import boto3
s3 = boto3.client('s3')
s3.list_buckets()
"
```

#### OpenAI API
```bash
# Тест API ключа
python3 -c "
import openai
client = openai.OpenAI(api_key='your-key')
response = client.models.list()
print('API ключ работает')
"
```

## Обновление системы

### 1. Обновление ComfyUI

```bash
cd /home/ubuntu/ComfyUI
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart comfyui.service
```

### 2. Обновление ComfyUI Integration

```bash
cd /path/to/confiuitest
git pull origin main
./scripts/install_all_components.sh /home/ubuntu/ComfyUI
sudo systemctl restart comfyui.service
```

### 3. Обновление зависимостей

```bash
cd /home/ubuntu/ComfyUI
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt --upgrade
```

## Безопасность

### 1. Настройка firewall

```bash
# Установка UFW
sudo apt install ufw

# Настройка правил
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 8188

# Активация
sudo ufw enable
```

### 2. Настройка SSL/TLS

```bash
# Установка Certbot
sudo apt install certbot

# Получение сертификата
sudo certbot certonly --standalone -d your-domain.com

# Настройка Nginx (опционально)
sudo apt install nginx
```

### 3. Регулярные обновления

```bash
# Автоматические обновления безопасности
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

## Производительность

### 1. Оптимизация Python

```bash
# Установка оптимизированных версий
pip install --upgrade pip setuptools wheel
pip install numpy --upgrade
```

### 2. Настройка виртуальной памяти

```bash
# Увеличение swap
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### 3. Мониторинг производительности

```bash
# Установка инструментов мониторинга
sudo apt install htop iotop nethogs

# Мониторинг в реальном времени
htop
```

## Поддержка

### Полезные ресурсы

- **Документация ComfyUI**: https://github.com/comfyanonymous/ComfyUI
- **Документация AWS S3**: https://docs.aws.amazon.com/s3/
- **Документация OpenAI**: https://platform.openai.com/docs
- **Issues и поддержка**: https://github.com/your-repo/confiuitest/issues

### Логи и отладка

```bash
# Включение отладочного режима
export DEBUG=true
export LOG_LEVEL=DEBUG

# Перезапуск с отладкой
sudo systemctl restart comfyui.service
sudo journalctl -u comfyui.service -f
```

### Контакты

При возникновении проблем:
1. Проверьте логи: `./manage_comfyui.sh logs`
2. Запустите тесты: `./manage_comfyui.sh test`
3. Проверьте состояние: `./manage_comfyui.sh health`
4. Обратитесь к документации: `./manage_comfyui.sh docs`
5. Создайте issue в репозитории проекта

## Заключение

После завершения установки у вас будет полностью функциональная система ComfyUI Integration с:

- ✅ Pipeline Builder для программного создания пайплайнов
- ✅ S3 Storage Integration для работы с облачным хранилищем
- ✅ OpenAI Integration для генерации изображений
- ✅ Автоматизированные тесты и мониторинг
- ✅ CLI интерфейс для управления
- ✅ Подробная документация

Система готова к использованию! Начните с создания первого пайплайна:

```bash
./manage_comfyui.sh pipeline create openai "Beautiful sunset over mountains"
``` 