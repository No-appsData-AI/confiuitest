#!/usr/bin/env python3
"""
OpenAI Image Generator для ComfyUI
Автор: AI Assistant
Версия: 1.0.0

Этот скрипт предоставляет функциональность для генерации изображений через OpenAI API
и может использоваться как кастомный узел в ComfyUI.
"""

import os
import json
import base64
import requests
from PIL import Image
import io
import time
from typing import Optional, Dict, Any, List

class OpenAIImageGenerator:
    """Класс для генерации изображений через OpenAI API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Инициализация генератора изображений
        
        Args:
            api_key: OpenAI API ключ. Если не указан, берется из переменной окружения OPENAI_API_KEY
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API ключ не найден. Укажите его в параметре или установите переменную окружения OPENAI_API_KEY")
        
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
        Генерация изображения через OpenAI API
        
        Args:
            prompt: Описание изображения для генерации
            model: Модель для генерации (dall-e-2, dall-e-3)
            size: Размер изображения
            quality: Качество изображения (standard, hd)
            style: Стиль изображения (vivid, natural)
            n: Количество изображений (только для dall-e-2)
            
        Returns:
            Словарь с результатами генерации
        """
        endpoint = f"{self.base_url}/images/generations"
        
        payload = {
            "model": model,
            "prompt": prompt,
            "size": size,
            "n": n
        }
        
        # Добавляем параметры только для DALL-E 3
        if model == "dall-e-3":
            payload["quality"] = quality
            payload["style"] = style
            payload["n"] = 1  # DALL-E 3 поддерживает только 1 изображение за раз
        
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
    
    def generate_image_variation(
        self,
        image_path: str,
        size: str = "1024x1024",
        n: int = 1
    ) -> Dict[str, Any]:
        """
        Генерация вариации изображения
        
        Args:
            image_path: Путь к исходному изображению
            size: Размер изображения
            n: Количество вариаций
            
        Returns:
            Словарь с результатами генерации
        """
        endpoint = f"{self.base_url}/images/variations"
        
        # Подготавливаем изображение
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
        
        files = {"image": ("image.png", image_data, "image/png")}
        data = {"size": size, "n": n}
        
        try:
            response = requests.post(endpoint, headers={"Authorization": f"Bearer {self.api_key}"}, files=files, data=data)
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
        Скачивание изображения по URL
        
        Args:
            url: URL изображения
            save_path: Путь для сохранения
            
        Returns:
            True если успешно, False в противном случае
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            return True
            
        except Exception as e:
            print(f"Ошибка при скачивании изображения: {e}")
            return False
    
    def save_images_from_result(self, result: Dict[str, Any], output_dir: str = "output") -> List[str]:
        """
        Сохранение изображений из результата генерации
        
        Args:
            result: Результат генерации
            output_dir: Директория для сохранения
            
        Returns:
            Список путей к сохраненным изображениям
        """
        if not result.get("success"):
            print(f"Ошибка генерации: {result.get('error')}")
            return []
        
        os.makedirs(output_dir, exist_ok=True)
        saved_paths = []
        
        for i, image_data in enumerate(result.get("images", [])):
            url = image_data.get("url")
            if url:
                timestamp = int(time.time())
                filename = f"openai_generated_{timestamp}_{i}.png"
                filepath = os.path.join(output_dir, filename)
                
                if self.download_image(url, filepath):
                    saved_paths.append(filepath)
                    print(f"Изображение сохранено: {filepath}")
        
        return saved_paths

# Функции для использования в ComfyUI
def generate_openai_image(
    prompt: str,
    api_key: str,
    model: str = "dall-e-3",
    size: str = "1024x1024",
    quality: str = "standard",
    style: str = "vivid"
) -> Dict[str, Any]:
    """
    Функция для использования в ComfyUI
    
    Args:
        prompt: Описание изображения
        api_key: OpenAI API ключ
        model: Модель генерации
        size: Размер изображения
        quality: Качество изображения
        style: Стиль изображения
        
    Returns:
        Словарь с результатами
    """
    generator = OpenAIImageGenerator(api_key)
    return generator.generate_image(prompt, model, size, quality, style)

def save_openai_result(result: Dict[str, Any], output_dir: str = "output") -> List[str]:
    """
    Сохранение результатов генерации
    
    Args:
        result: Результат генерации
        output_dir: Директория для сохранения
        
    Returns:
        Список путей к файлам
    """
    generator = OpenAIImageGenerator()
    return generator.save_images_from_result(result, output_dir)

# Пример использования
if __name__ == "__main__":
    # Пример использования скрипта
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("Установите переменную окружения OPENAI_API_KEY")
        exit(1)
    
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
        print("Изображение успешно сгенерировано!")
        saved_paths = generator.save_images_from_result(result)
        print(f"Сохранено изображений: {len(saved_paths)}")
    else:
        print(f"Ошибка генерации: {result['error']}") 