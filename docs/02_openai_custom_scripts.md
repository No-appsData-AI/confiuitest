# Создание кастомных скриптов для OpenAI API

## Обзор

Это руководство покажет, как создать кастомные скрипты для работы с OpenAI API и интегрировать их в ComfyUI как узлы.

## Структура проекта

```
openai_integration/
├── openai_image_generator.py      # Основной класс для работы с OpenAI
├── comfyui_openai_node.py         # Кастомные узлы для ComfyUI
├── __init__.py                    # Инициализация пакета
├── requirements.txt               # Зависимости
├── README.md                      # Документация
└── examples/                      # Примеры использования
    ├── basic_usage.py
    ├── batch_generation.py
    └── image_variations.py
```

## 1. Основной класс OpenAI генератора

### Создание базового класса

```python
#!/usr/bin/env python3
"""
OpenAI Image Generator
Автор: AI Assistant
Версия: 1.0.0
"""

import os
import json
import requests
import time
from typing import Optional, Dict, Any, List
from PIL import Image
import io

class OpenAIImageGenerator:
    """Класс для генерации изображений через OpenAI API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Инициализация генератора
        
        Args:
            api_key: OpenAI API ключ
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API ключ не найден")
        
        self.base_url = "https://api.openai.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_image(
        self,
        prompt: str,
        model: str = "dall-e-3",
        size: str = "1024x1024",
        quality: str = "standard",
        style: str = "vivid",
        n: int = 1
    ) -> Dict[str, Any]:
        """
        Генерация изображения
        
        Args:
            prompt: Описание изображения
            model: Модель (dall-e-2, dall-e-3)
            size: Размер изображения
            quality: Качество (standard, hd)
            style: Стиль (vivid, natural)
            n: Количество изображений
            
        Returns:
            Словарь с результатами
        """
        endpoint = f"{self.base_url}/images/generations"
        
        payload = {
            "model": model,
            "prompt": prompt,
            "size": size,
            "n": n
        }
        
        # Параметры только для DALL-E 3
        if model == "dall-e-3":
            payload["quality"] = quality
            payload["style"] = style
            payload["n"] = 1
        
        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            return {
                "success": True,
                "data": result,
                "images": result.get("data", []),
                "created": result.get("created"),
                "model": model
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "status_code": getattr(e.response, 'status_code', None)
            }
    
    def generate_variation(
        self,
        image_path: str,
        size: str = "1024x1024",
        n: int = 1
    ) -> Dict[str, Any]:
        """
        Генерация вариации изображения
        
        Args:
            image_path: Путь к изображению
            size: Размер вариации
            n: Количество вариаций
            
        Returns:
            Словарь с результатами
        """
        endpoint = f"{self.base_url}/images/variations"
        
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
        
        files = {"image": ("image.png", image_data, "image/png")}
        data = {"size": size, "n": n}
        
        try:
            response = requests.post(
                endpoint, 
                headers={"Authorization": f"Bearer {self.api_key}"}, 
                files=files, 
                data=data
            )
            response.raise_for_status()
            
            result = response.json()
            return {
                "success": True,
                "data": result,
                "images": result.get("data", []),
                "created": result.get("created")
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "status_code": getattr(e.response, 'status_code', None)
            }
    
    def download_image(self, url: str, save_path: str) -> bool:
        """
        Скачивание изображения
        
        Args:
            url: URL изображения
            save_path: Путь для сохранения
            
        Returns:
            True если успешно
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            return True
            
        except Exception as e:
            print(f"Ошибка скачивания: {e}")
            return False
    
    def save_images_from_result(
        self, 
        result: Dict[str, Any], 
        output_dir: str = "output"
    ) -> List[str]:
        """
        Сохранение изображений из результата
        
        Args:
            result: Результат генерации
            output_dir: Директория для сохранения
            
        Returns:
            Список путей к файлам
        """
        if not result.get("success"):
            print(f"Ошибка: {result.get('error')}")
            return []
        
        os.makedirs(output_dir, exist_ok=True)
        saved_paths = []
        
        for i, image_data in enumerate(result.get("images", [])):
            url = image_data.get("url")
            if url:
                timestamp = int(time.time())
                filename = f"openai_{timestamp}_{i}.png"
                filepath = os.path.join(output_dir, filename)
                
                if self.download_image(url, filepath):
                    saved_paths.append(filepath)
                    print(f"Сохранено: {filepath}")
        
        return saved_paths
```

### Примеры использования основного класса

```python
# examples/basic_usage.py

from openai_image_generator import OpenAIImageGenerator
import os

def basic_generation_example():
    """Пример базовой генерации"""
    
    # Инициализация
    api_key = os.getenv('OPENAI_API_KEY')
    generator = OpenAIImageGenerator(api_key)
    
    # Генерация изображения
    result = generator.generate_image(
        prompt="A beautiful sunset over mountains, digital art style",
        model="dall-e-3",
        size="1024x1024",
        quality="standard",
        style="vivid"
    )
    
    if result["success"]:
        print("Изображение сгенерировано!")
        
        # Сохранение
        saved_paths = generator.save_images_from_result(result)
        print(f"Сохранено файлов: {len(saved_paths)}")
    else:
        print(f"Ошибка: {result['error']}")

def batch_generation_example():
    """Пример пакетной генерации"""
    
    api_key = os.getenv('OPENAI_API_KEY')
    generator = OpenAIImageGenerator(api_key)
    
    prompts = [
        "A cat sitting on a windowsill",
        "A futuristic city skyline at night",
        "A peaceful forest with sunlight filtering through trees"
    ]
    
    for i, prompt in enumerate(prompts):
        print(f"Генерация {i+1}/{len(prompts)}: {prompt}")
        
        result = generator.generate_image(
            prompt=prompt,
            model="dall-e-3",
            size="1024x1024"
        )
        
        if result["success"]:
            saved_paths = generator.save_images_from_result(
                result, 
                f"output/batch_{i+1}"
            )
            print(f"Сохранено: {len(saved_paths)} файлов")
        else:
            print(f"Ошибка: {result['error']}")
        
        # Пауза между запросами
        time.sleep(2)

if __name__ == "__main__":
    basic_generation_example()
    batch_generation_example()
```

## 2. Создание кастомных узлов для ComfyUI

### Структура узла ComfyUI

```python
# comfyui_openai_node.py

import os
import sys
import json
import time
import requests
from PIL import Image
import io
import numpy as np
from typing import Dict, Any, List, Optional

# Импорт основного класса
from openai_image_generator import OpenAIImageGenerator

class OpenAIImageNode:
    """Кастомный узел ComfyUI для генерации изображений через OpenAI"""
    
    @classmethod
    def INPUT_TYPES(cls):
        """Определение входных параметров узла"""
        return {
            "required": {
                "prompt": ("STRING", {
                    "default": "A beautiful landscape", 
                    "multiline": True
                }),
                "api_key": ("STRING", {
                    "default": "", 
                    "password": True
                }),
                "model": (["dall-e-3", "dall-e-2"], {
                    "default": "dall-e-3"
                }),
                "size": (["1024x1024", "1792x1024", "1024x1792", "256x256", "512x512"], {
                    "default": "1024x1024"
                }),
                "quality": (["standard", "hd"], {
                    "default": "standard"
                }),
                "style": (["vivid", "natural"], {
                    "default": "vivid"
                }),
                "save_to_output": ("BOOLEAN", {
                    "default": True
                }),
            },
            "optional": {
                "seed": ("INT", {
                    "default": -1, 
                    "min": -1, 
                    "max": 0xffffffffffffffff
                }),
            }
        }
    
    # Определение выходных типов
    RETURN_TYPES = ("IMAGE", "STRING", "STRING")
    RETURN_NAMES = ("image", "filename", "metadata")
    FUNCTION = "generate_image"
    CATEGORY = "OpenAI"
    
    def generate_image(
        self, 
        prompt, 
        api_key, 
        model, 
        size, 
        quality, 
        style, 
        save_to_output, 
        seed=-1
    ):
        """
        Основная функция генерации
        
        Args:
            prompt: Описание изображения
            api_key: OpenAI API ключ
            model: Модель генерации
            size: Размер изображения
            quality: Качество изображения
            style: Стиль изображения
            save_to_output: Сохранять ли в output
            seed: Сид для генерации
            
        Returns:
            tuple: (image, filename, metadata)
        """
        try:
            # Получение API ключа
            api_key = api_key or os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OpenAI API ключ не указан")
            
            # Создание генератора
            generator = OpenAIImageGenerator(api_key)
            
            # Генерация изображения
            result = generator.generate_image(
                prompt=prompt,
                model=model,
                size=size,
                quality=quality,
                style=style
            )
            
            if not result.get("success"):
                error_msg = result.get("error", "Неизвестная ошибка")
                raise Exception(f"Ошибка генерации OpenAI: {error_msg}")
            
            # Получение URL изображения
            images = result.get("images", [])
            if not images:
                raise Exception("Не получено изображений от OpenAI")
            
            image_url = images[0].get("url")
            if not image_url:
                raise Exception("URL изображения не найден")
            
            # Скачивание изображения
            response = requests.get(image_url)
            response.raise_for_status()
            
            # Конвертация в PIL Image
            image = Image.open(io.BytesIO(response.content))
            
            # Конвертация в RGB
            if image.mode != "RGB":
                image = image.convert("RGB")
            
            # Создание имени файла
            timestamp = int(time.time())
            filename = f"openai_generated_{timestamp}.png"
            
            # Сохранение изображения
            if save_to_output:
                output_dir = "output"
                os.makedirs(output_dir, exist_ok=True)
                filepath = os.path.join(output_dir, filename)
                image.save(filepath)
            
            # Конвертация в формат ComfyUI
            image_array = np.array(image).astype(np.float32) / 255.0
            image_array = np.expand_dims(image_array, axis=0)
            
            # Создание метаданных
            metadata = {
                "prompt": prompt,
                "model": model,
                "size": size,
                "quality": quality,
                "style": style,
                "timestamp": timestamp,
                "generator": "OpenAI",
                "api_response": result.get("data", {})
            }
            
            return (image_array, filename, json.dumps(metadata, indent=2))
            
        except Exception as e:
            print(f"Ошибка в OpenAI узле: {e}")
            # Возврат пустого изображения при ошибке
            empty_image = np.zeros((1, 512, 512, 3), dtype=np.float32)
            return (empty_image, "error.png", json.dumps({"error": str(e)}))

class OpenAIImageVariationNode:
    """Кастомный узел ComfyUI для генерации вариаций изображений"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "api_key": ("STRING", {
                    "default": "", 
                    "password": True
                }),
                "size": (["1024x1024", "1792x1024", "1024x1792", "256x256", "512x512"], {
                    "default": "1024x1024"
                }),
                "save_to_output": ("BOOLEAN", {
                    "default": True
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE", "STRING", "STRING")
    RETURN_NAMES = ("image", "filename", "metadata")
    FUNCTION = "generate_variation"
    CATEGORY = "OpenAI"
    
    def generate_variation(self, image, api_key, size, save_to_output):
        """
        Генерация вариации изображения
        
        Args:
            image: Входное изображение
            api_key: OpenAI API ключ
            size: Размер вариации
            save_to_output: Сохранять ли в output
            
        Returns:
            tuple: (image, filename, metadata)
        """
        try:
            # Получение API ключа
            api_key = api_key or os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OpenAI API ключ не указан")
            
            # Конвертация изображения ComfyUI в PIL
            if len(image.shape) == 4:
                image_array = image[0]
            else:
                image_array = image
            
            image_array = (image_array * 255).astype(np.uint8)
            pil_image = Image.fromarray(image_array)
            
            # Сохранение временного файла
            temp_path = f"temp_variation_{int(time.time())}.png"
            pil_image.save(temp_path)
            
            try:
                # Создание генератора
                generator = OpenAIImageGenerator(api_key)
                
                # Генерация вариации
                result = generator.generate_variation(
                    image_path=temp_path,
                    size=size
                )
                
                if not result.get("success"):
                    error_msg = result.get("error", "Неизвестная ошибка")
                    raise Exception(f"Ошибка генерации вариации: {error_msg}")
                
                # Получение URL изображения
                images = result.get("images", [])
                if not images:
                    raise Exception("Не получено изображений от OpenAI")
                
                image_url = images[0].get("url")
                if not image_url:
                    raise Exception("URL изображения не найден")
                
                # Скачивание изображения
                response = requests.get(image_url)
                response.raise_for_status()
                
                # Конвертация в PIL Image
                new_image = Image.open(io.BytesIO(response.content))
                
                # Конвертация в RGB
                if new_image.mode != "RGB":
                    new_image = new_image.convert("RGB")
                
                # Создание имени файла
                timestamp = int(time.time())
                filename = f"openai_variation_{timestamp}.png"
                
                # Сохранение изображения
                if save_to_output:
                    output_dir = "output"
                    os.makedirs(output_dir, exist_ok=True)
                    filepath = os.path.join(output_dir, filename)
                    new_image.save(filepath)
                
                # Конвертация в формат ComfyUI
                new_image_array = np.array(new_image).astype(np.float32) / 255.0
                new_image_array = np.expand_dims(new_image_array, axis=0)
                
                # Создание метаданных
                metadata = {
                    "type": "variation",
                    "size": size,
                    "timestamp": timestamp,
                    "generator": "OpenAI",
                    "api_response": result.get("data", {})
                }
                
                return (new_image_array, filename, json.dumps(metadata, indent=2))
                
            finally:
                # Удаление временного файла
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            
        except Exception as e:
            print(f"Ошибка в OpenAI вариации узле: {e}")
            # Возврат пустого изображения при ошибке
            empty_image = np.zeros((1, 512, 512, 3), dtype=np.float32)
            return (empty_image, "error.png", json.dumps({"error": str(e)}))

# Регистрация узлов для ComfyUI
NODE_CLASS_MAPPINGS = {
    "OpenAIImageGenerator": OpenAIImageNode,
    "OpenAIImageVariation": OpenAIImageVariationNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OpenAIImageGenerator": "OpenAI Image Generator",
    "OpenAIImageVariation": "OpenAI Image Variation"
}

# Экспорт для ComfyUI
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
```

## 3. Установка и настройка

### Создание файла requirements.txt

```txt
# requirements.txt
requests>=2.25.0
Pillow>=8.0.0
numpy>=1.19.0
torch>=1.9.0
torchvision>=0.10.0
```

### Создание __init__.py

```python
# __init__.py

"""
OpenAI Image Generator для ComfyUI
Автор: AI Assistant
Версия: 1.0.0
"""

from .comfyui_openai_node import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
```

### Скрипт установки

```python
# install_openai_node.py

#!/usr/bin/env python3
"""
Скрипт установки OpenAI узла для ComfyUI
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def install_dependencies():
    """Установка зависимостей"""
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
    
    # Создание директорий
    custom_nodes_dir = os.path.join(comfyui_path, "custom_nodes")
    os.makedirs(custom_nodes_dir, exist_ok=True)
    
    openai_node_dir = os.path.join(custom_nodes_dir, "openai_image_generator")
    os.makedirs(openai_node_dir, exist_ok=True)
    
    # Копирование файлов
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
    """Создание __init__.py файла"""
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

def main():
    """Основная функция установки"""
    print("=== Установка OpenAI узла для ComfyUI ===")
    
    # Определение пути к ComfyUI
    comfyui_path = input("Введите путь к ComfyUI: ").strip()
    
    if not os.path.exists(comfyui_path):
        print(f"Путь {comfyui_path} не существует")
        return
    
    # Установка зависимостей
    install_dependencies()
    
    # Копирование файлов
    copy_files_to_comfyui(comfyui_path)
    
    # Создание __init__.py
    create_init_file(comfyui_path)
    
    print("\n=== Установка завершена ===")
    print("Перезапустите ComfyUI для загрузки нового узла")

if __name__ == "__main__":
    main()
```

## 4. Тестирование

### Тестовый скрипт

```python
# test_openai_node.py

#!/usr/bin/env python3
"""
Тестирование OpenAI узла
"""

import os
import sys
from openai_image_generator import OpenAIImageGenerator

def test_basic_generation():
    """Тест базовой генерации"""
    print("Тестирование базовой генерации...")
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Ошибка: OPENAI_API_KEY не установлен")
        return False
    
    generator = OpenAIImageGenerator(api_key)
    
    result = generator.generate_image(
        prompt="A simple red circle on white background",
        model="dall-e-3",
        size="1024x1024"
    )
    
    if result["success"]:
        print("✓ Генерация успешна")
        
        # Сохранение тестового изображения
        saved_paths = generator.save_images_from_result(result, "test_output")
        print(f"✓ Сохранено {len(saved_paths)} файлов")
        return True
    else:
        print(f"✗ Ошибка генерации: {result['error']}")
        return False

def test_variation_generation():
    """Тест генерации вариаций"""
    print("Тестирование генерации вариаций...")
    
    # Создание тестового изображения
    from PIL import Image, ImageDraw
    
    test_image = Image.new('RGB', (1024, 1024), color='white')
    draw = ImageDraw.Draw(test_image)
    draw.ellipse([400, 400, 624, 624], fill='red')
    
    test_path = "test_image.png"
    test_image.save(test_path)
    
    try:
        api_key = os.getenv('OPENAI_API_KEY')
        generator = OpenAIImageGenerator(api_key)
        
        result = generator.generate_variation(
            image_path=test_path,
            size="1024x1024"
        )
        
        if result["success"]:
            print("✓ Генерация вариации успешна")
            saved_paths = generator.save_images_from_result(result, "test_output")
            print(f"✓ Сохранено {len(saved_paths)} вариаций")
            return True
        else:
            print(f"✗ Ошибка генерации вариации: {result['error']}")
            return False
    
    finally:
        # Удаление тестового изображения
        if os.path.exists(test_path):
            os.remove(test_path)

def main():
    """Основная функция тестирования"""
    print("=== Тестирование OpenAI узла ===")
    
    # Проверка API ключа
    if not os.getenv('OPENAI_API_KEY'):
        print("Установите переменную окружения OPENAI_API_KEY")
        return
    
    # Создание директории для тестовых файлов
    os.makedirs("test_output", exist_ok=True)
    
    # Запуск тестов
    test1_passed = test_basic_generation()
    test2_passed = test_variation_generation()
    
    print("\n=== Результаты тестирования ===")
    print(f"Базовая генерация: {'✓' if test1_passed else '✗'}")
    print(f"Генерация вариаций: {'✓' if test2_passed else '✗'}")
    
    if test1_passed and test2_passed:
        print("Все тесты пройдены успешно!")
    else:
        print("Некоторые тесты не пройдены")

if __name__ == "__main__":
    main()
```

## 5. Использование в ComfyUI

### Загрузка узлов

После установки узлы будут доступны в ComfyUI в категории "OpenAI":

1. **OpenAI Image Generator** - для генерации новых изображений
2. **OpenAI Image Variation** - для создания вариаций существующих изображений

### Параметры узлов

#### OpenAI Image Generator:
- **prompt**: Описание изображения (обязательно)
- **api_key**: OpenAI API ключ (или переменная окружения)
- **model**: dall-e-2 или dall-e-3
- **size**: Размер изображения
- **quality**: standard или hd (только для DALL-E 3)
- **style**: vivid или natural (только для DALL-E 3)
- **save_to_output**: Сохранять ли файл

#### OpenAI Image Variation:
- **image**: Входное изображение (обязательно)
- **api_key**: OpenAI API ключ
- **size**: Размер вариации
- **save_to_output**: Сохранять ли файл

### Пример workflow

```json
{
  "nodes": [
    {
      "id": 1,
      "type": "OpenAIImageGenerator",
      "inputs": {
        "prompt": "A beautiful sunset over mountains",
        "model": "dall-e-3",
        "size": "1024x1024",
        "quality": "standard",
        "style": "vivid"
      }
    },
    {
      "id": 2,
      "type": "SaveImage",
      "inputs": {
        "images": ["1", 0],
        "filename_prefix": "openai_generated"
      }
    }
  ],
  "links": [[1, 1, 0, 2, 0]]
}
```

## 6. Устранение неполадок

### Частые проблемы:

1. **Ошибка API ключа**:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

2. **Ошибка импорта**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Узел не появляется в ComfyUI**:
   - Перезапустите ComfyUI
   - Проверьте логи на ошибки
   - Убедитесь, что файлы скопированы в правильную директорию

4. **Ошибка генерации**:
   - Проверьте баланс OpenAI аккаунта
   - Убедитесь в правильности API ключа
   - Проверьте ограничения модели

### Логирование

Добавьте логирование для отладки:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# В функциях узлов
logger.debug(f"Генерация изображения: {prompt}")
logger.error(f"Ошибка: {e}")
```

## Заключение

Этот подход позволяет создать полнофункциональную интеграцию с OpenAI API в ComfyUI. Основные преимущества:

- ✅ Модульная архитектура
- ✅ Легкое расширение функциональности
- ✅ Полная интеграция с ComfyUI
- ✅ Обработка ошибок
- ✅ Поддержка различных моделей
- ✅ Автоматическое сохранение результатов 