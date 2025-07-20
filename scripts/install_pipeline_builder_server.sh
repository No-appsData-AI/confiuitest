#!/bin/bash
# Скрипт установки Pipeline Builder на сервере ComfyUI
# Автор: AI Assistant
# Версия: 1.0.0

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функции логирования
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Проверка аргументов
if [ $# -eq 0 ]; then
    log_error "Использование: $0 <путь_к_comfyui>"
    log_info "Пример: $0 /home/ubuntu/ComfyUI"
    exit 1
fi

COMFYUI_PATH="$1"
PIPELINE_BUILDER_DIR="$COMFYUI_PATH/custom_nodes/pipeline_builder"

log_info "🚀 Установка Pipeline Builder на сервере ComfyUI"
log_info "Путь к ComfyUI: $COMFYUI_PATH"

# Проверка существования ComfyUI
if [ ! -d "$COMFYUI_PATH" ]; then
    log_error "ComfyUI не найден по пути: $COMFYUI_PATH"
    exit 1
fi

# Проверка виртуального окружения
if [ ! -d "$COMFYUI_PATH/venv" ]; then
    log_error "Виртуальное окружение ComfyUI не найдено"
    log_info "Сначала установите ComfyUI с виртуальным окружением"
    exit 1
fi

# Активация виртуального окружения
log_info "🔧 Активация виртуального окружения..."
source "$COMFYUI_PATH/venv/bin/activate"

# Создание директории для Pipeline Builder
log_info "📁 Создание директории Pipeline Builder..."
mkdir -p "$PIPELINE_BUILDER_DIR"

# Копирование файлов Pipeline Builder
log_info "📋 Копирование файлов..."

# Основные файлы
cp examples/comfyui_pipeline_builder.py "$PIPELINE_BUILDER_DIR/"
cp examples/pipeline_manager.py "$PIPELINE_BUILDER_DIR/"
cp examples/pipeline_examples.py "$PIPELINE_BUILDER_DIR/"

# S3 интеграция
cp examples/s3_storage_manager.py "$PIPELINE_BUILDER_DIR/"
cp examples/comfyui_s3_nodes.py "$PIPELINE_BUILDER_DIR/"

# OpenAI интеграция
cp examples/openai_image_generator.py "$PIPELINE_BUILDER_DIR/"
cp examples/comfyui_openai_node.py "$PIPELINE_BUILDER_DIR/"

# Конфигурация
cp config/settings.py "$PIPELINE_BUILDER_DIR/"

# Создание __init__.py
log_info "📦 Создание пакета..."
cat > "$PIPELINE_BUILDER_DIR/__init__.py" << 'EOF'
"""
Pipeline Builder для ComfyUI
Автор: AI Assistant
Версия: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "AI Assistant"

# Основные компоненты
from .comfyui_pipeline_builder import ComfyUIPipelineBuilder, PipelineTemplates
from .pipeline_manager import PipelineManager
from .s3_storage_manager import S3StorageManager
from .openai_image_generator import OpenAIImageGenerator

# ComfyUI узлы
from .comfyui_s3_nodes import (
    S3ImageUploader,
    S3ImageDownloader,
    S3ImageLister,
    S3WorkflowSaver,
    S3WorkflowLoader,
    S3StorageInfo
)

from .comfyui_openai_node import (
    OpenAIImageNode,
    OpenAIImageVariationNode
)

__all__ = [
    'ComfyUIPipelineBuilder',
    'PipelineTemplates',
    'PipelineManager',
    'S3StorageManager',
    'OpenAIImageGenerator',
    'S3ImageUploader',
    'S3ImageDownloader',
    'S3ImageLister',
    'S3WorkflowSaver',
    'S3WorkflowLoader',
    'S3StorageInfo',
    'OpenAIImageNode',
    'OpenAIImageVariationNode'
]
EOF

# Создание requirements.txt для Pipeline Builder
log_info "📋 Создание requirements.txt..."
cat > "$PIPELINE_BUILDER_DIR/requirements.txt" << 'EOF'
# Pipeline Builder Dependencies
requests>=2.28.0
boto3>=1.26.0
botocore>=1.29.0
Pillow>=8.0.0
numpy>=1.19.0
openai>=0.27.0
python-dotenv>=0.19.0
click>=8.0.0
colorama>=0.4.4
EOF

# Установка зависимостей
log_info "📦 Установка зависимостей..."
pip install -r "$PIPELINE_BUILDER_DIR/requirements.txt"

# Создание README.md
log_info "📖 Создание документации..."
cat > "$PIPELINE_BUILDER_DIR/README.md" << 'EOF'
# Pipeline Builder для ComfyUI

Инструмент для программного создания пайплайнов ComfyUI с интеграцией OpenAI и AWS S3.

## Возможности

- Программное создание пайплайнов ComfyUI
- Интеграция с OpenAI API для генерации изображений
- Интеграция с AWS S3 для хранения файлов
- Готовые шаблоны пайплайнов
- CLI интерфейс для управления

## Использование

```python
from pipeline_builder import ComfyUIPipelineBuilder

# Создание пайплайна
builder = ComfyUIPipelineBuilder("http://localhost:8188")
node_id = builder.add_node("OpenAIImageGenerator", {"prompt": "Beautiful sunset"})
builder.save_workflow("my_pipeline.json")
```

## Установка

Зависимости уже установлены. Для использования просто импортируйте модули.

## Документация

Подробная документация: https://github.com/your-repo/confiuitest
EOF

# Создание утилитарных скриптов
log_info "🔧 Создание утилитарных скриптов..."

# Скрипт для создания пайплайна
cat > "$PIPELINE_BUILDER_DIR/create_pipeline.py" << 'EOF'
#!/usr/bin/env python3
"""
Утилита для создания пайплайнов
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pipeline_manager import PipelineManager

def main():
    if len(sys.argv) < 2:
        print("Использование: python create_pipeline.py <тип> [параметры]")
        print("Типы: openai, s3, complex")
        return
    
    pipeline_type = sys.argv[1]
    manager = PipelineManager()
    
    if pipeline_type == "openai":
        prompt = sys.argv[2] if len(sys.argv) > 2 else "Beautiful landscape"
        builder = manager.create_openai_pipeline(prompt)
        builder.save_workflow("generated_openai_pipeline.json")
        print("✅ OpenAI пайплайн создан: generated_openai_pipeline.json")
    
    elif pipeline_type == "s3":
        bucket = sys.argv[2] if len(sys.argv) > 2 else "comfyui-images"
        builder = manager.create_s3_upload_pipeline(bucket)
        builder.save_workflow("generated_s3_pipeline.json")
        print("✅ S3 пайплайн создан: generated_s3_pipeline.json")
    
    elif pipeline_type == "complex":
        prompt = sys.argv[2] if len(sys.argv) > 2 else "Futuristic city"
        bucket = sys.argv[3] if len(sys.argv) > 3 else "comfyui-images"
        builder = manager.create_complex_pipeline(prompt, bucket)
        builder.save_workflow("generated_complex_pipeline.json")
        print("✅ Сложный пайплайн создан: generated_complex_pipeline.json")
    
    else:
        print(f"❌ Неизвестный тип пайплайна: {pipeline_type}")

if __name__ == "__main__":
    main()
EOF

# Скрипт для тестирования
cat > "$PIPELINE_BUILDER_DIR/test_pipeline.py" << 'EOF'
#!/usr/bin/env python3
"""
Утилита для тестирования пайплайнов
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from comfyui_pipeline_builder import ComfyUIPipelineBuilder

def main():
    if len(sys.argv) < 2:
        print("Использование: python test_pipeline.py <файл_пайплайна>")
        return
    
    pipeline_file = sys.argv[1]
    
    if not os.path.exists(pipeline_file):
        print(f"❌ Файл не найден: {pipeline_file}")
        return
    
    builder = ComfyUIPipelineBuilder()
    if builder.load_workflow(pipeline_file):
        validation = builder.validate_workflow()
        print(f"✅ Пайплайн загружен: {pipeline_file}")
        print(f"Валидность: {validation['valid']}")
        if validation['errors']:
            print("Ошибки:", validation['errors'])
        if validation['warnings']:
            print("Предупреждения:", validation['warnings'])
    else:
        print(f"❌ Ошибка загрузки пайплайна: {pipeline_file}")

if __name__ == "__main__":
    main()
EOF

# Установка прав на выполнение
chmod +x "$PIPELINE_BUILDER_DIR/create_pipeline.py"
chmod +x "$PIPELINE_BUILDER_DIR/test_pipeline.py"

# Создание конфигурационного файла
log_info "⚙️ Создание конфигурации..."
cat > "$PIPELINE_BUILDER_DIR/config.py" << 'EOF'
"""
Конфигурация Pipeline Builder
"""

import os

# ComfyUI настройки
COMFYUI_URL = os.getenv('COMFYUI_URL', 'http://localhost:8188')

# AWS S3 настройки
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
S3_BUCKET = os.getenv('S3_BUCKET', 'comfyui-images')

# OpenAI настройки
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

# Настройки логирования
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
EOF

# Тестирование установки
log_info "🧪 Тестирование установки..."
cd "$PIPELINE_BUILDER_DIR"

# Тест импорта
python3 -c "
try:
    from comfyui_pipeline_builder import ComfyUIPipelineBuilder
    from pipeline_manager import PipelineManager
    print('✅ Импорт модулей успешен')
except ImportError as e:
    print(f'❌ Ошибка импорта: {e}')
    exit(1)
"

# Тест создания простого пайплайна
python3 -c "
from comfyui_pipeline_builder import ComfyUIPipelineBuilder
builder = ComfyUIPipelineBuilder()
node_id = builder.add_node('PreviewImage', {})
workflow = builder.build_workflow()
print('✅ Создание пайплайна успешно')
print(f'Узлов в пайплайне: {len(workflow[\"nodes\"])}')
"

# Перезапуск ComfyUI для загрузки новых узлов
log_info "🔄 Перезапуск ComfyUI..."
if systemctl is-active --quiet comfyui.service; then
    sudo systemctl restart comfyui.service
    log_success "ComfyUI перезапущен"
else
    log_warning "ComfyUI сервис не запущен. Запустите вручную:"
    log_info "cd $COMFYUI_PATH && python main.py"
fi

log_success "🎉 Pipeline Builder успешно установлен!"
log_info "📁 Расположение: $PIPELINE_BUILDER_DIR"
log_info "🔧 Утилиты:"
log_info "  - python create_pipeline.py <тип> - создание пайплайнов"
log_info "  - python test_pipeline.py <файл> - тестирование пайплайнов"
log_info "🌐 ComfyUI доступен по адресу: http://localhost:8188"
log_info "📖 Документация: $PIPELINE_BUILDER_DIR/README.md" 