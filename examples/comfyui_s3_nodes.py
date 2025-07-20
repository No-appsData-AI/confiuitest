#!/usr/bin/env python3
"""
ComfyUI S3 Storage Nodes
Автор: AI Assistant
Версия: 1.0.0

Кастомные узлы ComfyUI для работы с AWS S3 хранилищем
"""

import os
import sys
import json
import tempfile
from typing import Dict, List, Optional, Tuple, Union
import logging

# Добавление пути к модулям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from s3_storage_manager import S3StorageManager
except ImportError:
    print("❌ Ошибка импорта S3StorageManager. Убедитесь, что файл s3_storage_manager.py находится в той же директории.")
    S3StorageManager = None

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class S3ImageUploader:
    """
    Узел для загрузки изображений в S3
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "bucket_name": ("STRING", {"default": "comfyui-images"}),
                "aws_access_key_id": ("STRING", {"default": "", "multiline": False}),
                "aws_secret_access_key": ("STRING", {"default": "", "multiline": False}),
                "region_name": ("STRING", {"default": "us-east-1"}),
                "s3_key": ("STRING", {"default": "", "multiline": False}),
                "metadata": ("STRING", {"default": "{}", "multiline": True}),
            },
            "optional": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "model": ("STRING", {"default": ""}),
                "workflow_name": ("STRING", {"default": ""}),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("s3_key", "s3_url", "status")
    FUNCTION = "upload_image"
    CATEGORY = "S3 Storage"
    
    def upload_image(self, 
                    image, 
                    bucket_name, 
                    aws_access_key_id, 
                    aws_secret_access_key, 
                    region_name, 
                    s3_key, 
                    metadata, 
                    prompt="", 
                    model="", 
                    workflow_name=""):
        """
        Загрузка изображения в S3
        """
        try:
            # Проверка доступности S3StorageManager
            if S3StorageManager is None:
                return "", "", "❌ S3StorageManager недоступен"
            
            # Получение учетных данных
            access_key = aws_access_key_id or os.getenv('AWS_ACCESS_KEY_ID')
            secret_key = aws_secret_access_key or os.getenv('AWS_SECRET_ACCESS_KEY')
            
            if not access_key or not secret_key:
                return "", "", "❌ AWS credentials не настроены"
            
            # Инициализация S3 менеджера
            s3_manager = S3StorageManager(
                bucket_name=bucket_name,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region_name
            )
            
            # Сохранение изображения во временный файл
            import numpy as np
            from PIL import Image
            
            # Конвертация numpy array в PIL Image
            if len(image.shape) == 4:
                image = image[0]  # Берем первый батч
            
            # Нормализация значений (0-1 -> 0-255)
            if image.max() <= 1.0:
                image = (image * 255).astype(np.uint8)
            
            pil_image = Image.fromarray(image)
            
            # Создание временного файла
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                temp_path = temp_file.name
                pil_image.save(temp_path, 'PNG')
            
            # Подготовка метаданных
            try:
                metadata_dict = json.loads(metadata) if metadata else {}
            except json.JSONDecodeError:
                metadata_dict = {}
            
            # Добавление дополнительных метаданных
            if prompt:
                metadata_dict['prompt'] = prompt
            if model:
                metadata_dict['model'] = model
            if workflow_name:
                metadata_dict['workflow_name'] = workflow_name
            
            # Загрузка в S3
            result = s3_manager.upload_image(
                image_path=temp_path,
                s3_key=s3_key if s3_key else None,
                metadata=metadata_dict
            )
            
            # Удаление временного файла
            os.unlink(temp_path)
            
            if result['success']:
                return result['s3_key'], result['url'], f"✅ {result['message']}"
            else:
                return "", "", f"❌ {result['error']}"
                
        except Exception as e:
            logger.error(f"❌ Ошибка загрузки изображения: {e}")
            return "", "", f"❌ Ошибка: {str(e)}"


class S3ImageDownloader:
    """
    Узел для скачивания изображений из S3
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "s3_key": ("STRING", {"default": "", "multiline": False}),
                "bucket_name": ("STRING", {"default": "comfyui-images"}),
                "aws_access_key_id": ("STRING", {"default": "", "multiline": False}),
                "aws_secret_access_key": ("STRING", {"default": "", "multiline": False}),
                "region_name": ("STRING", {"default": "us-east-1"}),
            }
        }
    
    RETURN_TYPES = ("IMAGE", "STRING", "STRING")
    RETURN_NAMES = ("image", "local_path", "status")
    FUNCTION = "download_image"
    CATEGORY = "S3 Storage"
    
    def download_image(self, 
                      s3_key, 
                      bucket_name, 
                      aws_access_key_id, 
                      aws_secret_access_key, 
                      region_name):
        """
        Скачивание изображения из S3
        """
        try:
            # Проверка доступности S3StorageManager
            if S3StorageManager is None:
                return None, "", "❌ S3StorageManager недоступен"
            
            # Получение учетных данных
            access_key = aws_access_key_id or os.getenv('AWS_ACCESS_KEY_ID')
            secret_key = aws_secret_access_key or os.getenv('AWS_SECRET_ACCESS_KEY')
            
            if not access_key or not secret_key:
                return None, "", "❌ AWS credentials не настроены"
            
            if not s3_key:
                return None, "", "❌ S3 ключ не указан"
            
            # Инициализация S3 менеджера
            s3_manager = S3StorageManager(
                bucket_name=bucket_name,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region_name
            )
            
            # Скачивание изображения
            result = s3_manager.download_image(s3_key=s3_key)
            
            if result['success']:
                # Загрузка изображения в ComfyUI
                from PIL import Image
                import numpy as np
                
                pil_image = Image.open(result['local_path'])
                image_array = np.array(pil_image).astype(np.float32) / 255.0
                
                # Добавление размерности батча
                if len(image_array.shape) == 3:
                    image_array = np.expand_dims(image_array, axis=0)
                
                return image_array, result['local_path'], f"✅ {result['message']}"
            else:
                return None, "", f"❌ {result['error']}"
                
        except Exception as e:
            logger.error(f"❌ Ошибка скачивания изображения: {e}")
            return None, "", f"❌ Ошибка: {str(e)}"


class S3ImageLister:
    """
    Узел для получения списка изображений из S3
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bucket_name": ("STRING", {"default": "comfyui-images"}),
                "aws_access_key_id": ("STRING", {"default": "", "multiline": False}),
                "aws_secret_access_key": ("STRING", {"default": "", "multiline": False}),
                "region_name": ("STRING", {"default": "us-east-1"}),
                "prefix": ("STRING", {"default": "comfyui/images/"}),
                "max_keys": ("INT", {"default": 50, "min": 1, "max": 1000}),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("images_list", "status")
    FUNCTION = "list_images"
    CATEGORY = "S3 Storage"
    
    def list_images(self, 
                   bucket_name, 
                   aws_access_key_id, 
                   aws_secret_access_key, 
                   region_name, 
                   prefix, 
                   max_keys):
        """
        Получение списка изображений из S3
        """
        try:
            # Проверка доступности S3StorageManager
            if S3StorageManager is None:
                return "", "❌ S3StorageManager недоступен"
            
            # Получение учетных данных
            access_key = aws_access_key_id or os.getenv('AWS_ACCESS_KEY_ID')
            secret_key = aws_secret_access_key or os.getenv('AWS_SECRET_ACCESS_KEY')
            
            if not access_key or not secret_key:
                return "", "❌ AWS credentials не настроены"
            
            # Инициализация S3 менеджера
            s3_manager = S3StorageManager(
                bucket_name=bucket_name,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region_name
            )
            
            # Получение списка изображений
            result = s3_manager.list_images(prefix=prefix, max_keys=max_keys)
            
            if result['success']:
                # Форматирование списка для вывода
                images_info = []
                for file_info in result['files']:
                    images_info.append({
                        'key': file_info['key'],
                        'size_mb': round(file_info['size'] / (1024 * 1024), 2),
                        'last_modified': file_info['last_modified'],
                        'url': file_info['url']
                    })
                
                images_json = json.dumps(images_info, indent=2, ensure_ascii=False)
                return images_json, f"✅ Найдено {result['count']} изображений"
            else:
                return "", f"❌ {result['error']}"
                
        except Exception as e:
            logger.error(f"❌ Ошибка получения списка изображений: {e}")
            return "", f"❌ Ошибка: {str(e)}"


class S3WorkflowSaver:
    """
    Узел для сохранения workflow в S3
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "workflow_data": ("STRING", {"default": "{}", "multiline": True}),
                "bucket_name": ("STRING", {"default": "comfyui-images"}),
                "aws_access_key_id": ("STRING", {"default": "", "multiline": False}),
                "aws_secret_access_key": ("STRING", {"default": "", "multiline": False}),
                "region_name": ("STRING", {"default": "us-east-1"}),
                "workflow_name": ("STRING", {"default": "", "multiline": False}),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("s3_key", "status")
    FUNCTION = "save_workflow"
    CATEGORY = "S3 Storage"
    
    def save_workflow(self, 
                     workflow_data, 
                     bucket_name, 
                     aws_access_key_id, 
                     aws_secret_access_key, 
                     region_name, 
                     workflow_name):
        """
        Сохранение workflow в S3
        """
        try:
            # Проверка доступности S3StorageManager
            if S3StorageManager is None:
                return "", "❌ S3StorageManager недоступен"
            
            # Получение учетных данных
            access_key = aws_access_key_id or os.getenv('AWS_ACCESS_KEY_ID')
            secret_key = aws_secret_access_key or os.getenv('AWS_SECRET_ACCESS_KEY')
            
            if not access_key or not secret_key:
                return "", "❌ AWS credentials не настроены"
            
            # Парсинг workflow данных
            try:
                workflow_dict = json.loads(workflow_data) if workflow_data else {}
            except json.JSONDecodeError:
                return "", "❌ Неверный формат JSON в workflow_data"
            
            # Инициализация S3 менеджера
            s3_manager = S3StorageManager(
                bucket_name=bucket_name,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region_name
            )
            
            # Сохранение workflow
            result = s3_manager.save_workflow(
                workflow_data=workflow_dict,
                workflow_name=workflow_name if workflow_name else None
            )
            
            if result['success']:
                return result['s3_key'], f"✅ {result['message']}"
            else:
                return "", f"❌ {result['error']}"
                
        except Exception as e:
            logger.error(f"❌ Ошибка сохранения workflow: {e}")
            return "", f"❌ Ошибка: {str(e)}"


class S3WorkflowLoader:
    """
    Узел для загрузки workflow из S3
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "workflow_name": ("STRING", {"default": "", "multiline": False}),
                "bucket_name": ("STRING", {"default": "comfyui-images"}),
                "aws_access_key_id": ("STRING", {"default": "", "multiline": False}),
                "aws_secret_access_key": ("STRING", {"default": "", "multiline": False}),
                "region_name": ("STRING", {"default": "us-east-1"}),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("workflow_data", "status")
    FUNCTION = "load_workflow"
    CATEGORY = "S3 Storage"
    
    def load_workflow(self, 
                     workflow_name, 
                     bucket_name, 
                     aws_access_key_id, 
                     aws_secret_access_key, 
                     region_name):
        """
        Загрузка workflow из S3
        """
        try:
            # Проверка доступности S3StorageManager
            if S3StorageManager is None:
                return "", "❌ S3StorageManager недоступен"
            
            # Получение учетных данных
            access_key = aws_access_key_id or os.getenv('AWS_ACCESS_KEY_ID')
            secret_key = aws_secret_access_key or os.getenv('AWS_SECRET_ACCESS_KEY')
            
            if not access_key or not secret_key:
                return "", "❌ AWS credentials не настроены"
            
            if not workflow_name:
                return "", "❌ Название workflow не указано"
            
            # Инициализация S3 менеджера
            s3_manager = S3StorageManager(
                bucket_name=bucket_name,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region_name
            )
            
            # Загрузка workflow
            result = s3_manager.load_workflow(workflow_name=workflow_name)
            
            if result['success']:
                workflow_json = json.dumps(result['workflow_data'], indent=2, ensure_ascii=False)
                return workflow_json, f"✅ {result['message']}"
            else:
                return "", f"❌ {result['error']}"
                
        except Exception as e:
            logger.error(f"❌ Ошибка загрузки workflow: {e}")
            return "", f"❌ Ошибка: {str(e)}"


class S3StorageInfo:
    """
    Узел для получения информации о S3 хранилище
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bucket_name": ("STRING", {"default": "comfyui-images"}),
                "aws_access_key_id": ("STRING", {"default": "", "multiline": False}),
                "aws_secret_access_key": ("STRING", {"default": "", "multiline": False}),
                "region_name": ("STRING", {"default": "us-east-1"}),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("storage_info", "status")
    FUNCTION = "get_storage_info"
    CATEGORY = "S3 Storage"
    
    def get_storage_info(self, 
                        bucket_name, 
                        aws_access_key_id, 
                        aws_secret_access_key, 
                        region_name):
        """
        Получение информации о S3 хранилище
        """
        try:
            # Проверка доступности S3StorageManager
            if S3StorageManager is None:
                return "", "❌ S3StorageManager недоступен"
            
            # Получение учетных данных
            access_key = aws_access_key_id or os.getenv('AWS_ACCESS_KEY_ID')
            secret_key = aws_secret_access_key or os.getenv('AWS_SECRET_ACCESS_KEY')
            
            if not access_key or not secret_key:
                return "", "❌ AWS credentials не настроены"
            
            # Инициализация S3 менеджера
            s3_manager = S3StorageManager(
                bucket_name=bucket_name,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region_name
            )
            
            # Получение информации о хранилище
            result = s3_manager.get_storage_info()
            
            if result['success']:
                info_json = json.dumps(result['info'], indent=2, ensure_ascii=False)
                return info_json, f"✅ {result['message']}"
            else:
                return "", f"❌ {result['error']}"
                
        except Exception as e:
            logger.error(f"❌ Ошибка получения информации о хранилище: {e}")
            return "", f"❌ Ошибка: {str(e)}"


# Регистрация узлов для ComfyUI
NODE_CLASS_MAPPINGS = {
    "S3ImageUploader": S3ImageUploader,
    "S3ImageDownloader": S3ImageDownloader,
    "S3ImageLister": S3ImageLister,
    "S3WorkflowSaver": S3WorkflowSaver,
    "S3WorkflowLoader": S3WorkflowLoader,
    "S3StorageInfo": S3StorageInfo,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "S3ImageUploader": "S3 Image Uploader",
    "S3ImageDownloader": "S3 Image Downloader", 
    "S3ImageLister": "S3 Image Lister",
    "S3WorkflowSaver": "S3 Workflow Saver",
    "S3WorkflowLoader": "S3 Workflow Loader",
    "S3StorageInfo": "S3 Storage Info",
}

# Экспорт для ComfyUI
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS'] 