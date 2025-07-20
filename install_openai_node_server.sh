#!/bin/bash

# Скрипт установки OpenAI узла на сервере ComfyUI
# Автор: AI Assistant

SERVER_IP="34.245.10.81"
COMFYUI_PATH="/home/ubuntu/ComfyUI"

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Установка OpenAI узла на сервере ComfyUI ===${NC}"

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
run_on_server "cd ${COMFYUI_PATH} && source venv/bin/activate && pip install requests Pillow numpy"
echo -e "${GREEN}✓ Зависимости установлены${NC}"

# Создание директории для кастомных узлов
echo -e "${YELLOW}4. Создание директории для кастомных узлов...${NC}"
run_on_server "mkdir -p ${COMFYUI_PATH}/custom_nodes/openai_image_generator"
echo -e "${GREEN}✓ Директория создана${NC}"

# Копирование файлов на сервер
echo -e "${YELLOW}5. Копирование файлов на сервер...${NC}"

# Копируем основной скрипт генератора
scp -i blackholetest.pem openai_image_generator.py ubuntu@${SERVER_IP}:${COMFYUI_PATH}/custom_nodes/openai_image_generator/
echo -e "${GREEN}✓ openai_image_generator.py скопирован${NC}"

# Копируем узел ComfyUI
scp -i blackholetest.pem comfyui_openai_node.py ubuntu@${SERVER_IP}:${COMFYUI_PATH}/custom_nodes/openai_image_generator/
echo -e "${GREEN}✓ comfyui_openai_node.py скопирован${NC}"

# Создание __init__.py файла
echo -e "${YELLOW}6. Создание __init__.py файла...${NC}"
run_on_server "cat > ${COMFYUI_PATH}/custom_nodes/openai_image_generator/__init__.py << 'EOF'
\"\"\"
OpenAI Image Generator для ComfyUI
Автор: AI Assistant
Версия: 1.0.0
\"\"\"

from .comfyui_openai_node import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
EOF"
echo -e "${GREEN}✓ __init__.py создан${NC}"

# Создание requirements.txt
echo -e "${YELLOW}7. Создание requirements.txt...${NC}"
run_on_server "cat > ${COMFYUI_PATH}/custom_nodes/openai_image_generator/requirements.txt << 'EOF'
requests>=2.25.0
Pillow>=8.0.0
numpy>=1.19.0
EOF"
echo -e "${GREEN}✓ requirements.txt создан${NC}"

# Создание README.md
echo -e "${YELLOW}8. Создание README.md...${NC}"
run_on_server "cat > ${COMFYUI_PATH}/custom_nodes/openai_image_generator/README.md << 'EOF'
# OpenAI Image Generator для ComfyUI

Кастомный узел для ComfyUI, который позволяет генерировать изображения через OpenAI API.

## Возможности

- Генерация изображений через DALL-E 2 и DALL-E 3
- Генерация вариаций изображений
- Интеграция в пайплайны ComfyUI
- Поддержка различных размеров и стилей

## Установка

1. Установите зависимости:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

2. Установите переменную окружения OPENAI_API_KEY:
   \`\`\`bash
   export OPENAI_API_KEY=\"your-api-key-here\"
   \`\`\`

3. Перезапустите ComfyUI

## Использование

### OpenAI Image Generator
- **prompt**: Описание изображения для генерации
- **api_key**: OpenAI API ключ (или используйте переменную окружения)
- **model**: Модель (dall-e-2, dall-e-3)
- **size**: Размер изображения
- **quality**: Качество (standard, hd) - только для DALL-E 3
- **style**: Стиль (vivid, natural) - только для DALL-E 3

### OpenAI Image Variation
- **image**: Входное изображение
- **api_key**: OpenAI API ключ
- **size**: Размер вариации

## Автор

AI Assistant
EOF"
echo -e "${GREEN}✓ README.md создан${NC}"

# Установка прав доступа
echo -e "${YELLOW}9. Установка прав доступа...${NC}"
run_on_server "chmod -R 755 ${COMFYUI_PATH}/custom_nodes/openai_image_generator"
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
echo -e "${GREEN}✓ OpenAI узел установлен в ComfyUI${NC}"
echo -e "${YELLOW}Теперь вы можете использовать узлы OpenAI в ComfyUI:${NC}"
echo -e "${BLUE}  - OpenAI Image Generator${NC}"
echo -e "${BLUE}  - OpenAI Image Variation${NC}"
echo ""
echo -e "${YELLOW}Для использования установите переменную окружения OPENAI_API_KEY:${NC}"
echo -e "${BLUE}  export OPENAI_API_KEY=\"your-api-key-here\"${NC}"
echo ""
echo -e "${GREEN}ComfyUI доступен по адресу: http://${SERVER_IP}:8188${NC}" 