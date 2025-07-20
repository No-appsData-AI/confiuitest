"""
OpenAI Image Generator Node для ComfyUI
Автор: AI Assistant
Версия: 1.0.0

Кастомный узел для ComfyUI, который позволяет генерировать изображения через OpenAI API
и интегрировать их в пайплайны ComfyUI.
"""

import os
import sys
import json
import time
import requests
from PIL import Image
import io
import base64
from typing import Dict, Any, List, Optional

# Добавляем путь к нашему скрипту
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

try:
    from openai_image_generator import OpenAIImageGenerator
except ImportError:
    print("Ошибка импорта openai_image_generator.py")

class OpenAIImageNode:
    """Кастомный узел ComfyUI для генерации изображений через OpenAI"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "A beautiful landscape", "multiline": True}),
                "api_key": ("STRING", {"default": "", "password": True}),
                "model": (["dall-e-3", "dall-e-2"], {"default": "dall-e-3"}),
                "size": (["1024x1024", "1792x1024", "1024x1792", "256x256", "512x512"], {"default": "1024x1024"}),
                "quality": (["standard", "hd"], {"default": "standard"}),
                "style": (["vivid", "natural"], {"default": "vivid"}),
                "save_to_output": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "seed": ("INT", {"default": -1, "min": -1, "max": 0xffffffffffffffff}),
            }
        }
    
    RETURN_TYPES = ("IMAGE", "STRING", "STRING")
    RETURN_NAMES = ("image", "filename", "metadata")
    FUNCTION = "generate_image"
    CATEGORY = "OpenAI"
    
    def generate_image(self, prompt, api_key, model, size, quality, style, save_to_output, seed=-1):
        """
        Генерация изображения через OpenAI API
        
        Args:
            prompt: Описание изображения
            api_key: OpenAI API ключ
            model: Модель генерации
            size: Размер изображения
            quality: Качество изображения
            style: Стиль изображения
            save_to_output: Сохранять ли в output
            seed: Сид для генерации (не используется в OpenAI)
            
        Returns:
            tuple: (image, filename, metadata)
        """
        try:
            # Используем API ключ из параметра или переменной окружения
            api_key = api_key or os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OpenAI API ключ не указан")
            
            # Создаем генератор
            generator = OpenAIImageGenerator(api_key)
            
            # Генерируем изображение
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
            
            # Получаем URL изображения
            images = result.get("images", [])
            if not images:
                raise Exception("Не получено изображений от OpenAI")
            
            image_url = images[0].get("url")
            if not image_url:
                raise Exception("URL изображения не найден")
            
            # Скачиваем изображение
            response = requests.get(image_url)
            response.raise_for_status()
            
            # Конвертируем в PIL Image
            image = Image.open(io.BytesIO(response.content))
            
            # Конвертируем в формат ComfyUI (RGB)
            if image.mode != "RGB":
                image = image.convert("RGB")
            
            # Создаем имя файла
            timestamp = int(time.time())
            filename = f"openai_generated_{timestamp}.png"
            
            # Сохраняем изображение если нужно
            if save_to_output:
                output_dir = "output"
                os.makedirs(output_dir, exist_ok=True)
                filepath = os.path.join(output_dir, filename)
                image.save(filepath)
            
            # Конвертируем в формат ComfyUI (numpy array)
            import numpy as np
            image_array = np.array(image).astype(np.float32) / 255.0
            image_array = np.expand_dims(image_array, axis=0)  # Добавляем batch dimension
            
            # Создаем метаданные
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
            # Возвращаем пустое изображение в случае ошибки
            import numpy as np
            empty_image = np.zeros((1, 512, 512, 3), dtype=np.float32)
            return (empty_image, "error.png", json.dumps({"error": str(e)}))

class OpenAIImageVariationNode:
    """Кастомный узел ComfyUI для генерации вариаций изображений через OpenAI"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "api_key": ("STRING", {"default": "", "password": True}),
                "size": (["1024x1024", "1792x1024", "1024x1792", "256x256", "512x512"], {"default": "1024x1024"}),
                "save_to_output": ("BOOLEAN", {"default": True}),
            }
        }
    
    RETURN_TYPES = ("IMAGE", "STRING", "STRING")
    RETURN_NAMES = ("image", "filename", "metadata")
    FUNCTION = "generate_variation"
    CATEGORY = "OpenAI"
    
    def generate_variation(self, image, api_key, size, save_to_output):
        """
        Генерация вариации изображения через OpenAI API
        
        Args:
            image: Входное изображение
            api_key: OpenAI API ключ
            size: Размер изображения
            save_to_output: Сохранять ли в output
            
        Returns:
            tuple: (image, filename, metadata)
        """
        try:
            # Используем API ключ из параметра или переменной окружения
            api_key = api_key or os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OpenAI API ключ не указан")
            
            # Конвертируем изображение ComfyUI в PIL Image
            import numpy as np
            if len(image.shape) == 4:
                image_array = image[0]  # Берем первый batch
            else:
                image_array = image
            
            # Конвертируем из [0,1] в [0,255]
            image_array = (image_array * 255).astype(np.uint8)
            pil_image = Image.fromarray(image_array)
            
            # Сохраняем временный файл
            temp_path = f"temp_variation_{int(time.time())}.png"
            pil_image.save(temp_path)
            
            try:
                # Создаем генератор
                generator = OpenAIImageGenerator(api_key)
                
                # Генерируем вариацию
                result = generator.generate_image_variation(
                    image_path=temp_path,
                    size=size
                )
                
                if not result.get("success"):
                    error_msg = result.get("error", "Неизвестная ошибка")
                    raise Exception(f"Ошибка генерации вариации OpenAI: {error_msg}")
                
                # Получаем URL изображения
                images = result.get("images", [])
                if not images:
                    raise Exception("Не получено изображений от OpenAI")
                
                image_url = images[0].get("url")
                if not image_url:
                    raise Exception("URL изображения не найден")
                
                # Скачиваем изображение
                response = requests.get(image_url)
                response.raise_for_status()
                
                # Конвертируем в PIL Image
                new_image = Image.open(io.BytesIO(response.content))
                
                # Конвертируем в формат ComfyUI (RGB)
                if new_image.mode != "RGB":
                    new_image = new_image.convert("RGB")
                
                # Создаем имя файла
                timestamp = int(time.time())
                filename = f"openai_variation_{timestamp}.png"
                
                # Сохраняем изображение если нужно
                if save_to_output:
                    output_dir = "output"
                    os.makedirs(output_dir, exist_ok=True)
                    filepath = os.path.join(output_dir, filename)
                    new_image.save(filepath)
                
                # Конвертируем в формат ComfyUI (numpy array)
                new_image_array = np.array(new_image).astype(np.float32) / 255.0
                new_image_array = np.expand_dims(new_image_array, axis=0)
                
                # Создаем метаданные
                metadata = {
                    "type": "variation",
                    "size": size,
                    "timestamp": timestamp,
                    "generator": "OpenAI",
                    "api_response": result.get("data", {})
                }
                
                return (new_image_array, filename, json.dumps(metadata, indent=2))
                
            finally:
                # Удаляем временный файл
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            
        except Exception as e:
            print(f"Ошибка в OpenAI вариации узле: {e}")
            # Возвращаем пустое изображение в случае ошибки
            import numpy as np
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