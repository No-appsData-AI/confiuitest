#!/bin/bash

# Скрипт установки S3 Storage узлов на сервере ComfyUI
# Автор: AI Assistant

SERVER_IP="34.245.10.81"
COMFYUI_PATH="/home/ubuntu/ComfyUI"

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Установка S3 Storage узлов на сервере ComfyUI ===${NC}"

# Функция для выполнения команд на сервере
run_on_server() {
    ssh -i blackholetest.pem -o StrictHostKeyChecking=no ubuntu@${SERVER_IP} "$1"
}

# Проверка подключения к серверу
echo -e "${YELLOW}1. Проверка подключения к серверу...${NC}"
if ssh -i blackholetest.pem -o StrictHostKeyChecking=no -o ConnectTimeout=5 ubuntu@${SERVER_IP} "echo 'test'" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Сервер доступен${NC}"
else
    echo -e "${RED}✗ Сервер недоступен${NC}"
    exit 1
fi

# Остановка ComfyUI сервиса
echo -e "${YELLOW}2. Остановка ComfyUI сервиса...${NC}"
run_on_server "sudo systemctl stop comfyui.service"
echo -e "${GREEN}✓ Сервис остановлен${NC}"

# Установка зависимостей
echo -e "${YELLOW}3. Установка зависимостей...${NC}"
run_on_server "cd ${COMFYUI_PATH} && source venv/bin/activate && pip install boto3 botocore"
echo -e "${GREEN}✓ Зависимости установлены${NC}"

# Создание директории для S3 узлов
echo -e "${YELLOW}4. Создание директории для S3 узлов...${NC}"
run_on_server "mkdir -p ${COMFYUI_PATH}/custom_nodes/s3_storage"
echo -e "${GREEN}✓ Директория создана${NC}"

# Копирование файлов на сервер
echo -e "${YELLOW}5. Копирование файлов на сервер...${NC}"

# Копируем основной менеджер S3
scp -i blackholetest.pem examples/s3_storage_manager.py ubuntu@${SERVER_IP}:${COMFYUI_PATH}/custom_nodes/s3_storage/
echo -e "${GREEN}✓ s3_storage_manager.py скопирован${NC}"

# Копируем узлы ComfyUI
scp -i blackholetest.pem examples/comfyui_s3_nodes.py ubuntu@${SERVER_IP}:${COMFYUI_PATH}/custom_nodes/s3_storage/
echo -e "${GREEN}✓ comfyui_s3_nodes.py скопирован${NC}"

# Создание __init__.py файла
echo -e "${YELLOW}6. Создание __init__.py файла...${NC}"
run_on_server "cat > ${COMFYUI_PATH}/custom_nodes/s3_storage/__init__.py << 'EOF'
\"\"\"
S3 Storage для ComfyUI
Автор: AI Assistant
Версия: 1.0.0
\"\"\"

from .comfyui_s3_nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
EOF"
echo -e "${GREEN}✓ __init__.py создан${NC}"

# Создание requirements.txt
echo -e "${YELLOW}7. Создание requirements.txt...${NC}"
run_on_server "cat > ${COMFYUI_PATH}/custom_nodes/s3_storage/requirements.txt << 'EOF'
boto3>=1.26.0
botocore>=1.29.0
Pillow>=8.0.0
numpy>=1.19.0
EOF"
echo -e "${GREEN}✓ requirements.txt создан${NC}"

# Создание README.md
echo -e "${YELLOW}8. Создание README.md...${NC}"
run_on_server "cat > ${COMFYUI_PATH}/custom_nodes/s3_storage/README.md << 'EOF'
# S3 Storage для ComfyUI

Кастомные узлы для ComfyUI, которые позволяют работать с AWS S3 хранилищем.

## Возможности

- Загрузка изображений в S3
- Скачивание изображений из S3
- Получение списка изображений
- Сохранение и загрузка workflows
- Получение информации о хранилище
- Резервное копирование

## Установка

1. Установите зависимости:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

2. Установите переменные окружения AWS:
   \`\`\`bash
   export AWS_ACCESS_KEY_ID=\"your-access-key\"
   export AWS_SECRET_ACCESS_KEY=\"your-secret-key\"
   \`\`\`

3. Создайте S3 bucket для ComfyUI

4. Перезапустите ComfyUI

## Узлы

### S3 Image Uploader
Загружает изображения в S3 хранилище.

**Входы:**
- image: Изображение для загрузки
- bucket_name: Название S3 bucket
- aws_access_key_id: AWS Access Key ID
- aws_secret_access_key: AWS Secret Access Key
- region_name: AWS регион
- s3_key: Ключ в S3 (опционально)
- metadata: Дополнительные метаданные (JSON)
- prompt: Промпт для генерации (опционально)
- model: Модель генерации (опционально)
- workflow_name: Название workflow (опционально)

**Выходы:**
- s3_key: Ключ загруженного файла в S3
- s3_url: URL для доступа к файлу
- status: Статус операции

### S3 Image Downloader
Скачивает изображения из S3 хранилища.

**Входы:**
- s3_key: Ключ файла в S3
- bucket_name: Название S3 bucket
- aws_access_key_id: AWS Access Key ID
- aws_secret_access_key: AWS Secret Access Key
- region_name: AWS регион

**Выходы:**
- image: Скачанное изображение
- local_path: Локальный путь к файлу
- status: Статус операции

### S3 Image Lister
Получает список изображений из S3.

**Входы:**
- bucket_name: Название S3 bucket
- aws_access_key_id: AWS Access Key ID
- aws_secret_access_key: AWS Secret Access Key
- region_name: AWS регион
- prefix: Префикс для поиска
- max_keys: Максимальное количество ключей

**Выходы:**
- images_list: JSON список изображений
- status: Статус операции

### S3 Workflow Saver
Сохраняет workflow в S3.

**Входы:**
- workflow_data: JSON данные workflow
- bucket_name: Название S3 bucket
- aws_access_key_id: AWS Access Key ID
- aws_secret_access_key: AWS Secret Access Key
- region_name: AWS регион
- workflow_name: Название workflow

**Выходы:**
- s3_key: Ключ сохраненного workflow
- status: Статус операции

### S3 Workflow Loader
Загружает workflow из S3.

**Входы:**
- workflow_name: Название workflow
- bucket_name: Название S3 bucket
- aws_access_key_id: AWS Access Key ID
- aws_secret_access_key: AWS Secret Access Key
- region_name: AWS регион

**Выходы:**
- workflow_data: JSON данные workflow
- status: Статус операции

### S3 Storage Info
Получает информацию о S3 хранилище.

**Входы:**
- bucket_name: Название S3 bucket
- aws_access_key_id: AWS Access Key ID
- aws_secret_access_key: AWS Secret Access Key
- region_name: AWS регион

**Выходы:**
- storage_info: JSON информация о хранилище
- status: Статус операции

## Структура S3

\`\`\`
your-bucket/
├── comfyui/
│   ├── images/          # Изображения
│   ├── workflows/       # Workflows
│   ├── metadata/        # Метаданные
│   ├── temp/           # Временные файлы
│   └── backups/        # Резервные копии
\`\`\`

## Примеры использования

### Загрузка изображения
1. Добавьте узел S3 Image Uploader
2. Подключите изображение к входу image
3. Укажите параметры AWS и bucket
4. Запустите workflow

### Скачивание изображения
1. Добавьте узел S3 Image Downloader
2. Укажите s3_key изображения
3. Настройте параметры AWS
4. Получите изображение на выходе

### Сохранение workflow
1. Добавьте узел S3 Workflow Saver
2. Подключите JSON данные workflow
3. Укажите название workflow
4. Сохраните в S3

## Безопасность

- Никогда не коммитьте AWS ключи в Git
- Используйте IAM роли с минимальными правами
- Настройте CORS для S3 bucket
- Используйте HTTPS для всех соединений

## Автор

AI Assistant
EOF"
echo -e "${GREEN}✓ README.md создан${NC}"

# Установка прав доступа
echo -e "${YELLOW}9. Установка прав доступа...${NC}"
run_on_server "chmod -R 755 ${COMFYUI_PATH}/custom_nodes/s3_storage"
echo -e "${GREEN}✓ Права доступа установлены${NC}"

# Запуск ComfyUI сервиса
echo -e "${YELLOW}10. Запуск ComfyUI сервиса...${NC}"
run_on_server "sudo systemctl start comfyui.service"
sleep 5

# Проверка статуса
echo -e "${YELLOW}11. Проверка статуса сервиса...${NC}"
run_on_server "sudo systemctl status comfyui.service --no-pager"

echo ""
echo -e "${BLUE}=== Установка завершена ===${NC}"
echo -e "${GREEN}✓ S3 Storage узлы установлены в ComfyUI${NC}"
echo -e "${YELLOW}Теперь вы можете использовать узлы S3 в ComfyUI:${NC}"
echo -e "${BLUE}  - S3 Image Uploader${NC}"
echo -e "${BLUE}  - S3 Image Downloader${NC}"
echo -e "${BLUE}  - S3 Image Lister${NC}"
echo -e "${BLUE}  - S3 Workflow Saver${NC}"
echo -e "${BLUE}  - S3 Workflow Loader${NC}"
echo -e "${BLUE}  - S3 Storage Info${NC}"
echo ""
echo -e "${YELLOW}Для использования настройте переменные окружения AWS:${NC}"
echo -e "${BLUE}  export AWS_ACCESS_KEY_ID=\"your-access-key\"${NC}"
echo -e "${BLUE}  export AWS_SECRET_ACCESS_KEY=\"your-secret-key\"${NC}"
echo ""
echo -e "${YELLOW}Или передавайте ключи напрямую в узлах${NC}"
echo ""
echo -e "${GREEN}ComfyUI доступен по адресу: http://${SERVER_IP}:8188${NC}" 