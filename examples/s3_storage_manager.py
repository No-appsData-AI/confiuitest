#!/usr/bin/env python3
"""
S3 Storage Manager для ComfyUI
Автор: AI Assistant
Версия: 1.0.0

Класс для взаимодействия с AWS S3 для чтения и сохранения изображений
"""

import os
import boto3
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union
from botocore.exceptions import ClientError, NoCredentialsError
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class S3StorageManager:
    """
    Менеджер для работы с AWS S3 хранилищем
    """
    
    def __init__(self, 
                 bucket_name: str,
                 aws_access_key_id: Optional[str] = None,
                 aws_secret_access_key: Optional[str] = None,
                 region_name: str = 'us-east-1',
                 endpoint_url: Optional[str] = None):
        """
        Инициализация S3 менеджера
        
        Args:
            bucket_name: Название S3 bucket
            aws_access_key_id: AWS Access Key ID
            aws_secret_access_key: AWS Secret Access Key
            region_name: AWS регион
            endpoint_url: URL эндпоинта (для совместимости с MinIO и др.)
        """
        self.bucket_name = bucket_name
        self.region_name = region_name
        
        # Получение учетных данных
        self.aws_access_key_id = aws_access_key_id or os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_access_key = aws_secret_access_key or os.getenv('AWS_SECRET_ACCESS_KEY')
        
        if not self.aws_access_key_id or not self.aws_secret_access_key:
            raise ValueError("AWS credentials not provided. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables.")
        
        # Инициализация S3 клиента
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name,
            endpoint_url=endpoint_url
        )
        
        # Проверка доступности bucket
        self._check_bucket_access()
        
        # Создание структуры папок
        self._create_folder_structure()
    
    def _check_bucket_access(self) -> bool:
        """Проверка доступа к bucket"""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            logger.info(f"✅ Доступ к bucket '{self.bucket_name}' подтвержден")
            return True
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                logger.error(f"❌ Bucket '{self.bucket_name}' не найден")
            elif error_code == '403':
                logger.error(f"❌ Нет доступа к bucket '{self.bucket_name}'")
            else:
                logger.error(f"❌ Ошибка доступа к bucket: {error_code}")
            raise
    
    def _create_folder_structure(self):
        """Создание структуры папок в S3"""
        folders = [
            'comfyui/images/',
            'comfyui/workflows/',
            'comfyui/metadata/',
            'comfyui/temp/',
            'comfyui/backups/'
        ]
        
        for folder in folders:
            try:
                self.s3_client.put_object(
                    Bucket=self.bucket_name,
                    Key=folder,
                    Body=''
                )
                logger.info(f"📁 Создана папка: {folder}")
            except ClientError as e:
                logger.warning(f"⚠️ Не удалось создать папку {folder}: {e}")
    
    def upload_image(self, 
                    image_path: str, 
                    s3_key: Optional[str] = None,
                    metadata: Optional[Dict] = None) -> Dict:
        """
        Загрузка изображения в S3
        
        Args:
            image_path: Путь к локальному файлу изображения
            s3_key: Ключ в S3 (если не указан, генерируется автоматически)
            metadata: Дополнительные метаданные
            
        Returns:
            Dict с информацией о загруженном файле
        """
        try:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Файл не найден: {image_path}")
            
            # Генерация ключа S3 если не указан
            if not s3_key:
                filename = os.path.basename(image_path)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                s3_key = f"comfyui/images/{timestamp}_{filename}"
            
            # Подготовка метаданных
            file_metadata = {
                'upload_time': datetime.now().isoformat(),
                'original_path': image_path,
                'file_size': os.path.getsize(image_path),
                'file_type': os.path.splitext(image_path)[1].lower()
            }
            
            if metadata:
                file_metadata.update(metadata)
            
            # Загрузка файла
            with open(image_path, 'rb') as file:
                self.s3_client.upload_fileobj(
                    file,
                    self.bucket_name,
                    s3_key,
                    ExtraArgs={'Metadata': file_metadata}
                )
            
            # Получение URL
            url = self.get_file_url(s3_key)
            
            result = {
                'success': True,
                's3_key': s3_key,
                'url': url,
                'metadata': file_metadata,
                'message': f"Изображение успешно загружено: {s3_key}"
            }
            
            logger.info(f"✅ Загружено изображение: {s3_key}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Ошибка загрузки изображения: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Ошибка загрузки изображения: {e}"
            }
    
    def download_image(self, 
                      s3_key: str, 
                      local_path: Optional[str] = None) -> Dict:
        """
        Скачивание изображения из S3
        
        Args:
            s3_key: Ключ файла в S3
            local_path: Локальный путь для сохранения (если не указан, генерируется)
            
        Returns:
            Dict с информацией о скачанном файле
        """
        try:
            # Генерация локального пути если не указан
            if not local_path:
                filename = os.path.basename(s3_key)
                local_path = f"/tmp/{filename}"
            
            # Создание директории если не существует
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            # Скачивание файла
            self.s3_client.download_file(self.bucket_name, s3_key, local_path)
            
            # Получение метаданных
            metadata = self.get_file_metadata(s3_key)
            
            result = {
                'success': True,
                'local_path': local_path,
                's3_key': s3_key,
                'metadata': metadata,
                'message': f"Изображение успешно скачано: {local_path}"
            }
            
            logger.info(f"✅ Скачано изображение: {s3_key} -> {local_path}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Ошибка скачивания изображения: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Ошибка скачивания изображения: {e}"
            }
    
    def list_images(self, 
                   prefix: str = 'comfyui/images/',
                   max_keys: int = 100) -> Dict:
        """
        Список изображений в S3
        
        Args:
            prefix: Префикс для поиска
            max_keys: Максимальное количество ключей
            
        Returns:
            Dict со списком файлов
        """
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix,
                MaxKeys=max_keys
            )
            
            files = []
            if 'Contents' in response:
                for obj in response['Contents']:
                    files.append({
                        'key': obj['Key'],
                        'size': obj['Size'],
                        'last_modified': obj['LastModified'].isoformat(),
                        'url': self.get_file_url(obj['Key'])
                    })
            
            result = {
                'success': True,
                'files': files,
                'count': len(files),
                'message': f"Найдено {len(files)} файлов"
            }
            
            logger.info(f"📋 Список изображений: {len(files)} файлов")
            return result
            
        except Exception as e:
            logger.error(f"❌ Ошибка получения списка файлов: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Ошибка получения списка файлов: {e}"
            }
    
    def delete_image(self, s3_key: str) -> Dict:
        """
        Удаление изображения из S3
        
        Args:
            s3_key: Ключ файла в S3
            
        Returns:
            Dict с результатом операции
        """
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=s3_key)
            
            result = {
                'success': True,
                's3_key': s3_key,
                'message': f"Изображение удалено: {s3_key}"
            }
            
            logger.info(f"🗑️ Удалено изображение: {s3_key}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Ошибка удаления изображения: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Ошибка удаления изображения: {e}"
            }
    
    def get_file_url(self, s3_key: str, expires_in: int = 3600) -> str:
        """
        Получение URL для доступа к файлу
        
        Args:
            s3_key: Ключ файла в S3
            expires_in: Время жизни URL в секундах
            
        Returns:
            URL для доступа к файлу
        """
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': s3_key},
                ExpiresIn=expires_in
            )
            return url
        except Exception as e:
            logger.error(f"❌ Ошибка генерации URL: {e}")
            return ""
    
    def get_file_metadata(self, s3_key: str) -> Dict:
        """
        Получение метаданных файла
        
        Args:
            s3_key: Ключ файла в S3
            
        Returns:
            Dict с метаданными
        """
        try:
            response = self.s3_client.head_object(Bucket=self.bucket_name, Key=s3_key)
            return response.get('Metadata', {})
        except Exception as e:
            logger.error(f"❌ Ошибка получения метаданных: {e}")
            return {}
    
    def save_workflow(self, 
                     workflow_data: Dict, 
                     workflow_name: Optional[str] = None) -> Dict:
        """
        Сохранение workflow в S3
        
        Args:
            workflow_data: Данные workflow
            workflow_name: Название workflow
            
        Returns:
            Dict с результатом операции
        """
        try:
            if not workflow_name:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                workflow_name = f"workflow_{timestamp}.json"
            
            s3_key = f"comfyui/workflows/{workflow_name}"
            
            # Сохранение workflow
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=json.dumps(workflow_data, indent=2),
                ContentType='application/json'
            )
            
            result = {
                'success': True,
                's3_key': s3_key,
                'workflow_name': workflow_name,
                'message': f"Workflow сохранен: {s3_key}"
            }
            
            logger.info(f"💾 Сохранен workflow: {s3_key}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Ошибка сохранения workflow: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Ошибка сохранения workflow: {e}"
            }
    
    def load_workflow(self, workflow_name: str) -> Dict:
        """
        Загрузка workflow из S3
        
        Args:
            workflow_name: Название workflow
            
        Returns:
            Dict с данными workflow
        """
        try:
            s3_key = f"comfyui/workflows/{workflow_name}"
            
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=s3_key)
            workflow_data = json.loads(response['Body'].read().decode('utf-8'))
            
            result = {
                'success': True,
                'workflow_data': workflow_data,
                's3_key': s3_key,
                'message': f"Workflow загружен: {s3_key}"
            }
            
            logger.info(f"📂 Загружен workflow: {s3_key}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Ошибка загрузки workflow: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Ошибка загрузки workflow: {e}"
            }
    
    def backup_images(self, backup_name: Optional[str] = None) -> Dict:
        """
        Создание резервной копии всех изображений
        
        Args:
            backup_name: Название резервной копии
            
        Returns:
            Dict с результатом операции
        """
        try:
            if not backup_name:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = f"backup_{timestamp}"
            
            # Получение списка всех изображений
            images_list = self.list_images()
            if not images_list['success']:
                return images_list
            
            backup_data = {
                'backup_name': backup_name,
                'created_at': datetime.now().isoformat(),
                'images_count': len(images_list['files']),
                'images': images_list['files']
            }
            
            # Сохранение резервной копии
            s3_key = f"comfyui/backups/{backup_name}.json"
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=json.dumps(backup_data, indent=2),
                ContentType='application/json'
            )
            
            result = {
                'success': True,
                'backup_name': backup_name,
                's3_key': s3_key,
                'images_count': len(images_list['files']),
                'message': f"Резервная копия создана: {backup_name}"
            }
            
            logger.info(f"💾 Создана резервная копия: {backup_name}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Ошибка создания резервной копии: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Ошибка создания резервной копии: {e}"
            }
    
    def get_storage_info(self) -> Dict:
        """
        Получение информации о хранилище
        
        Returns:
            Dict с информацией о хранилище
        """
        try:
            # Подсчет файлов по категориям
            categories = {
                'images': self.list_images('comfyui/images/'),
                'workflows': self.list_images('comfyui/workflows/'),
                'backups': self.list_images('comfyui/backups/')
            }
            
            total_files = sum(cat['count'] for cat in categories.values() if cat['success'])
            total_size = sum(
                sum(f['size'] for f in cat['files']) 
                for cat in categories.values() 
                if cat['success']
            )
            
            info = {
                'bucket_name': self.bucket_name,
                'region': self.region_name,
                'total_files': total_files,
                'total_size_bytes': total_size,
                'total_size_mb': round(total_size / (1024 * 1024), 2),
                'categories': {
                    name: {
                        'count': cat['count'] if cat['success'] else 0,
                        'files': cat['files'] if cat['success'] else []
                    }
                    for name, cat in categories.items()
                }
            }
            
            return {
                'success': True,
                'info': info,
                'message': f"Информация о хранилище получена"
            }
            
        except Exception as e:
            logger.error(f"❌ Ошибка получения информации о хранилище: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Ошибка получения информации о хранилище: {e}"
            }


# Пример использования
if __name__ == "__main__":
    # Инициализация менеджера
    s3_manager = S3StorageManager(
        bucket_name="your-comfyui-bucket",
        aws_access_key_id="your-access-key",
        aws_secret_access_key="your-secret-key",
        region_name="us-east-1"
    )
    
    # Пример загрузки изображения
    result = s3_manager.upload_image(
        image_path="/path/to/image.png",
        metadata={"prompt": "A beautiful sunset", "model": "dall-e-3"}
    )
    print(result)
    
    # Пример получения списка изображений
    images = s3_manager.list_images()
    print(f"Найдено изображений: {images['count']}")
    
    # Пример получения информации о хранилище
    info = s3_manager.get_storage_info()
    print(f"Общий размер: {info['info']['total_size_mb']} MB") 