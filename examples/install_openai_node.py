#!/usr/bin/env python3
"""
Скрипт установки OpenAI узла для ComfyUI
Автор: AI Assistant
Версия: 1.0.0

Этот скрипт устанавливает кастомный узел OpenAI в ComfyUI
и настраивает необходимые зависимости.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def install_dependencies():
    """Установка необходимых зависимостей"""
    print("Установка зависимостей...")
    
    dependencies = [
        "requests",
        "Pillow",
        "numpy"
    ]
    
    for dep in dependencies:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✓ {dep} установлен")
        except subprocess.CalledProcessError:
            print(f"✗ Ошибка установки {dep}")

def copy_files_to_comfyui(comfyui_path):
    """Копирование файлов в ComfyUI"""
    print(f"Копирование файлов в ComfyUI: {comfyui_path}")
    
    # Создаем директорию для кастомных узлов
    custom_nodes_dir = os.path.join(comfyui_path, "custom_nodes")
    os.makedirs(custom_nodes_dir, exist_ok=True)
    
    # Создаем директорию для нашего узла
    openai_node_dir = os.path.join(custom_nodes_dir, "openai_image_generator")
    os.makedirs(openai_node_dir, exist_ok=True)
    
    # Копируем файлы
    files_to_copy = [
        "openai_image_generator.py",
        "comfyui_openai_node.py"
    ]
    
    for file in files_to_copy:
        if os.path.exists(file):
            dest_path = os.path.join(openai_node_dir, file)
            shutil.copy2(file, dest_path)
            print(f"✓ Скопирован {file}")
        else:
            print(f"✗ Файл {file} не найден")

def create_init_file(comfyui_path):
    """Создание __init__.py файла для кастомного узла"""
    openai_node_dir = os.path.join(comfyui_path, "custom_nodes", "openai_image_generator")
    init_file = os.path.join(openai_node_dir, "__init__.py")
    
    init_content = '''"""
OpenAI Image Generator для ComfyUI
Автор: AI Assistant
Версия: 1.0.0
"""

from .comfyui_openai_node import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
'''
    
    with open(init_file, 'w', encoding='utf-8') as f:
        f.write(init_content)
    
    print("✓ Создан __init__.py файл")

def create_requirements_file(comfyui_path):
    """Создание requirements.txt файла"""
    openai_node_dir = os.path.join(comfyui_path, "custom_nodes", "openai_image_generator")
    requirements_file = os.path.join(openai_node_dir, "requirements.txt")
    
    requirements_content = '''requests>=2.25.0
Pillow>=8.0.0
numpy>=1.19.0
'''
    
    with open(requirements_file, 'w', encoding='utf-8') as f:
        f.write(requirements_content)
    
    print("✓ Создан requirements.txt файл")

def create_readme_file(comfyui_path):
    """Создание README.md файла с инструкциями"""
    openai_node_dir = os.path.join(comfyui_path, "custom_nodes", "openai_image_generator")
    readme_file = os.path.join(openai_node_dir, "README.md")
    
    readme_content = '''# OpenAI Image Generator для ComfyUI

Кастомный узел для ComfyUI, который позволяет генерировать изображения через OpenAI API.

## Возможности

- Генерация изображений через DALL-E 2 и DALL-E 3
- Генерация вариаций изображений
- Интеграция в пайплайны ComfyUI
- Поддержка различных размеров и стилей

## Установка

1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

2. Установите переменную окружения OPENAI_API_KEY:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

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

## Примеры

1. Генерация пейзажа:
   ```
   prompt: "A beautiful sunset over mountains, digital art style"
   model: dall-e-3
   size: 1024x1024
   ```

2. Генерация портрета:
   ```
   prompt: "A professional portrait of a woman, studio lighting"
   model: dall-e-3
   size: 1024x1024
   quality: hd
   style: natural
   ```

## Примечания

- DALL-E 3 поддерживает только 1 изображение за раз
- DALL-E 2 поддерживает до 10 изображений за раз
- Для использования HD качества требуется DALL-E 3
- API ключ можно указать в узле или через переменную окружения

## Автор

AI Assistant
'''
    
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✓ Создан README.md файл")

def main():
    """Основная функция установки"""
    print("=== Установка OpenAI узла для ComfyUI ===")
    
    # Определяем путь к ComfyUI
    comfyui_path = input("Введите путь к ComfyUI (или нажмите Enter для поиска): ").strip()
    
    if not comfyui_path:
        # Ищем ComfyUI в стандартных местах
        possible_paths = [
            "/home/ubuntu/ComfyUI",
            "./ComfyUI",
            "../ComfyUI",
            os.path.expanduser("~/ComfyUI")
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                comfyui_path = path
                print(f"Найден ComfyUI: {comfyui_path}")
                break
        else:
            print("ComfyUI не найден. Укажите путь вручную.")
            return
    
    if not os.path.exists(comfyui_path):
        print(f"Путь {comfyui_path} не существует")
        return
    
    # Устанавливаем зависимости
    install_dependencies()
    
    # Копируем файлы
    copy_files_to_comfyui(comfyui_path)
    
    # Создаем дополнительные файлы
    create_init_file(comfyui_path)
    create_requirements_file(comfyui_path)
    create_readme_file(comfyui_path)
    
    print("\n=== Установка завершена ===")
    print("Теперь перезапустите ComfyUI для загрузки нового узла")
    print("Узел будет доступен в категории 'OpenAI'")

if __name__ == "__main__":
    main() 