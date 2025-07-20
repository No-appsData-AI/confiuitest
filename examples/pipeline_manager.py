#!/usr/bin/env python3
"""
Pipeline Manager для ComfyUI
Автор: AI Assistant
Версия: 1.0.0

Утилита для управления пайплайнами ComfyUI
"""

import os
import json
import argparse
from typing import Dict, List, Optional, Any
from .comfyui_pipeline_builder import ComfyUIPipelineBuilder, PipelineTemplates
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PipelineManager:
    """
    Менеджер пайплайнов ComfyUI
    """
    
    def __init__(self, comfyui_url: str = "http://localhost:8188"):
        """
        Инициализация менеджера пайплайнов
        
        Args:
            comfyui_url: URL ComfyUI сервера
        """
        self.comfyui_url = comfyui_url
        self.builder = ComfyUIPipelineBuilder(comfyui_url)
    
    def create_openai_pipeline(self, 
                              prompt: str,
                              model: str = "dall-e-3",
                              size: str = "1024x1024",
                              quality: str = "standard",
                              style: str = "vivid") -> ComfyUIPipelineBuilder:
        """
        Создание пайплайна с OpenAI генерацией
        
        Args:
            prompt: Промпт для генерации
            model: Модель OpenAI
            size: Размер изображения
            quality: Качество изображения
            style: Стиль изображения
            
        Returns:
            Строитель пайплайна
        """
        builder = ComfyUIPipelineBuilder(self.comfyui_url)
        
        # Узел генерации OpenAI
        openai_node = builder.add_node(
            node_type="OpenAIImageGenerator",
            inputs={
                "prompt": prompt,
                "api_key": "",
                "model": model,
                "size": size,
                "quality": quality,
                "style": style
            },
            title="OpenAI Generator",
            description=f"Генерация: {prompt[:50]}..."
        )
        
        # Узел предварительного просмотра
        preview_node = builder.add_node(
            node_type="PreviewImage",
            inputs={},
            title="Preview",
            description="Предварительный просмотр"
        )
        
        # Соединение
        builder.connect_nodes(openai_node, 0, preview_node, 0)
        
        return builder
    
    def create_s3_upload_pipeline(self,
                                 bucket_name: str,
                                 aws_access_key_id: str = "",
                                 aws_secret_access_key: str = "",
                                 region: str = "us-east-1") -> ComfyUIPipelineBuilder:
        """
        Создание пайплайна для загрузки в S3
        
        Args:
            bucket_name: Название S3 bucket
            aws_access_key_id: AWS Access Key ID
            aws_secret_access_key: AWS Secret Access Key
            region: AWS регион
            
        Returns:
            Строитель пайплайна
        """
        builder = ComfyUIPipelineBuilder(self.comfyui_url)
        
        # Узел загрузки изображения
        load_node = builder.add_node(
            node_type="LoadImage",
            inputs={},
            title="Load Image",
            description="Загрузка изображения"
        )
        
        # Узел загрузки в S3
        s3_node = builder.add_node(
            node_type="S3ImageUploader",
            inputs={
                "bucket_name": bucket_name,
                "aws_access_key_id": aws_access_key_id,
                "aws_secret_access_key": aws_secret_access_key,
                "region_name": region,
                "metadata": "{\"source\": \"pipeline_manager\"}"
            },
            title="S3 Uploader",
            description="Загрузка в S3"
        )
        
        # Соединение
        builder.connect_nodes(load_node, 0, s3_node, 0)
        
        return builder
    
    def create_s3_download_pipeline(self,
                                   s3_key: str,
                                   bucket_name: str,
                                   aws_access_key_id: str = "",
                                   aws_secret_access_key: str = "",
                                   region: str = "us-east-1") -> ComfyUIPipelineBuilder:
        """
        Создание пайплайна для скачивания из S3
        
        Args:
            s3_key: Ключ файла в S3
            bucket_name: Название S3 bucket
            aws_access_key_id: AWS Access Key ID
            aws_secret_access_key: AWS Secret Access Key
            region: AWS регион
            
        Returns:
            Строитель пайплайна
        """
        builder = ComfyUIPipelineBuilder(self.comfyui_url)
        
        # Узел скачивания из S3
        s3_node = builder.add_node(
            node_type="S3ImageDownloader",
            inputs={
                "s3_key": s3_key,
                "bucket_name": bucket_name,
                "aws_access_key_id": aws_access_key_id,
                "aws_secret_access_key": aws_secret_access_key,
                "region_name": region
            },
            title="S3 Downloader",
            description=f"Скачивание: {s3_key}"
        )
        
        # Узел предварительного просмотра
        preview_node = builder.add_node(
            node_type="PreviewImage",
            inputs={},
            title="Preview",
            description="Предварительный просмотр"
        )
        
        # Соединение
        builder.connect_nodes(s3_node, 0, preview_node, 0)
        
        return builder
    
    def create_workflow_save_pipeline(self,
                                    workflow_data: Dict[str, Any],
                                    bucket_name: str,
                                    workflow_name: str,
                                    aws_access_key_id: str = "",
                                    aws_secret_access_key: str = "",
                                    region: str = "us-east-1") -> ComfyUIPipelineBuilder:
        """
        Создание пайплайна для сохранения workflow в S3
        
        Args:
            workflow_data: Данные workflow
            bucket_name: Название S3 bucket
            workflow_name: Название workflow
            aws_access_key_id: AWS Access Key ID
            aws_secret_access_key: AWS Secret Access Key
            region: AWS регион
            
        Returns:
            Строитель пайплайна
        """
        return PipelineTemplates.workflow_save_pipeline(
            workflow_data=workflow_data,
            bucket_name=bucket_name,
            workflow_name=workflow_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
    
    def create_complex_pipeline(self,
                               prompt: str,
                               bucket_name: str,
                               aws_access_key_id: str = "",
                               aws_secret_access_key: str = "",
                               region: str = "us-east-1") -> ComfyUIPipelineBuilder:
        """
        Создание сложного пайплайна: OpenAI -> S3 -> Preview
        
        Args:
            prompt: Промпт для генерации
            bucket_name: Название S3 bucket
            aws_access_key_id: AWS Access Key ID
            aws_secret_access_key: AWS Secret Access Key
            region: AWS регион
            
        Returns:
            Строитель пайплайна
        """
        builder = ComfyUIPipelineBuilder(self.comfyui_url)
        
        # Узел генерации OpenAI
        openai_node = builder.add_node(
            node_type="OpenAIImageGenerator",
            inputs={
                "prompt": prompt,
                "api_key": "",
                "model": "dall-e-3",
                "size": "1024x1024",
                "quality": "standard",
                "style": "vivid"
            },
            title="OpenAI Generator",
            description=f"Генерация: {prompt[:50]}..."
        )
        
        # Узел загрузки в S3
        s3_upload_node = builder.add_node(
            node_type="S3ImageUploader",
            inputs={
                "bucket_name": bucket_name,
                "aws_access_key_id": aws_access_key_id,
                "aws_secret_access_key": aws_secret_access_key,
                "region_name": region,
                "metadata": json.dumps({"prompt": prompt, "source": "openai"})
            },
            title="S3 Uploader",
            description="Загрузка в S3"
        )
        
        # Узел предварительного просмотра
        preview_node = builder.add_node(
            node_type="PreviewImage",
            inputs={},
            title="Preview",
            description="Предварительный просмотр"
        )
        
        # Соединения
        builder.connect_nodes(openai_node, 0, s3_upload_node, 0)
        builder.connect_nodes(openai_node, 0, preview_node, 0)
        
        return builder
    
    def load_pipeline_from_file(self, filepath: str) -> ComfyUIPipelineBuilder:
        """
        Загрузка пайплайна из файла
        
        Args:
            filepath: Путь к файлу пайплайна
            
        Returns:
            Строитель пайплайна
        """
        builder = ComfyUIPipelineBuilder(self.comfyui_url)
        
        if builder.load_workflow(filepath):
            logger.info(f"✅ Пайплайн загружен из {filepath}")
            return builder
        else:
            raise ValueError(f"Не удалось загрузить пайплайн из {filepath}")
    
    def save_pipeline_to_file(self, builder: ComfyUIPipelineBuilder, filepath: str) -> bool:
        """
        Сохранение пайплайна в файл
        
        Args:
            builder: Строитель пайплайна
            filepath: Путь к файлу для сохранения
            
        Returns:
            True если сохранение успешно
        """
        return builder.save_workflow(filepath)
    
    def upload_pipeline(self, builder: ComfyUIPipelineBuilder, name: str = None) -> Dict[str, Any]:
        """
        Загрузка пайплайна в ComfyUI
        
        Args:
            builder: Строитель пайплайна
            name: Название пайплайна
            
        Returns:
            Результат загрузки
        """
        return builder.upload_to_comfyui(name)
    
    def execute_pipeline(self, 
                        builder: ComfyUIPipelineBuilder,
                        name: str = None,
                        wait: bool = True,
                        timeout: int = 300) -> Dict[str, Any]:
        """
        Выполнение пайплайна
        
        Args:
            builder: Строитель пайплайна
            name: Название пайплайна
            wait: Ожидать завершения
            timeout: Таймаут ожидания
            
        Returns:
            Результат выполнения
        """
        return builder.execute_workflow(name, wait, timeout)
    
    def validate_pipeline(self, builder: ComfyUIPipelineBuilder) -> Dict[str, Any]:
        """
        Валидация пайплайна
        
        Args:
            builder: Строитель пайплайна
            
        Returns:
            Результат валидации
        """
        return builder.validate_workflow()
    
    def list_available_nodes(self) -> Dict[str, Any]:
        """
        Получение списка доступных узлов
        
        Returns:
            Список доступных узлов
        """
        return self.builder.get_available_nodes()


def main():
    """Основная функция для работы с командной строкой"""
    parser = argparse.ArgumentParser(description="Pipeline Manager для ComfyUI")
    parser.add_argument("--url", default="http://localhost:8188", help="URL ComfyUI сервера")
    
    subparsers = parser.add_subparsers(dest="command", help="Доступные команды")
    
    # Команда создания OpenAI пайплайна
    openai_parser = subparsers.add_parser("create-openai", help="Создать OpenAI пайплайн")
    openai_parser.add_argument("--prompt", required=True, help="Промпт для генерации")
    openai_parser.add_argument("--model", default="dall-e-3", help="Модель OpenAI")
    openai_parser.add_argument("--size", default="1024x1024", help="Размер изображения")
    openai_parser.add_argument("--output", help="Файл для сохранения пайплайна")
    openai_parser.add_argument("--upload", action="store_true", help="Загрузить в ComfyUI")
    openai_parser.add_argument("--execute", action="store_true", help="Выполнить пайплайн")
    
    # Команда создания S3 пайплайна
    s3_parser = subparsers.add_parser("create-s3", help="Создать S3 пайплайн")
    s3_parser.add_argument("--type", choices=["upload", "download"], required=True, help="Тип S3 пайплайна")
    s3_parser.add_argument("--bucket", required=True, help="Название S3 bucket")
    s3_parser.add_argument("--s3-key", help="Ключ файла в S3 (для download)")
    s3_parser.add_argument("--aws-key", help="AWS Access Key ID")
    s3_parser.add_argument("--aws-secret", help="AWS Secret Access Key")
    s3_parser.add_argument("--region", default="us-east-1", help="AWS регион")
    s3_parser.add_argument("--output", help="Файл для сохранения пайплайна")
    s3_parser.add_argument("--upload", action="store_true", help="Загрузить в ComfyUI")
    
    # Команда создания сложного пайплайна
    complex_parser = subparsers.add_parser("create-complex", help="Создать сложный пайплайн")
    complex_parser.add_argument("--prompt", required=True, help="Промпт для генерации")
    complex_parser.add_argument("--bucket", required=True, help="Название S3 bucket")
    complex_parser.add_argument("--aws-key", help="AWS Access Key ID")
    complex_parser.add_argument("--aws-secret", help="AWS Secret Access Key")
    complex_parser.add_argument("--region", default="us-east-1", help="AWS регион")
    complex_parser.add_argument("--output", help="Файл для сохранения пайплайна")
    complex_parser.add_argument("--upload", action="store_true", help="Загрузить в ComfyUI")
    complex_parser.add_argument("--execute", action="store_true", help="Выполнить пайплайн")
    
    # Команда загрузки пайплайна
    load_parser = subparsers.add_parser("load", help="Загрузить пайплайн из файла")
    load_parser.add_argument("--file", required=True, help="Файл пайплайна")
    load_parser.add_argument("--upload", action="store_true", help="Загрузить в ComfyUI")
    load_parser.add_argument("--execute", action="store_true", help="Выполнить пайплайн")
    load_parser.add_argument("--validate", action="store_true", help="Валидировать пайплайн")
    
    # Команда получения списка узлов
    nodes_parser = subparsers.add_parser("nodes", help="Получить список доступных узлов")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Инициализация менеджера
    manager = PipelineManager(args.url)
    
    try:
        if args.command == "create-openai":
            # Создание OpenAI пайплайна
            builder = manager.create_openai_pipeline(
                prompt=args.prompt,
                model=args.model,
                size=args.size
            )
            
            if args.output:
                manager.save_pipeline_to_file(builder, args.output)
                print(f"✅ Пайплайн сохранен в {args.output}")
            
            if args.upload:
                result = manager.upload_pipeline(builder, f"OpenAI Pipeline: {args.prompt[:30]}")
                print(f"📤 Результат загрузки: {result}")
            
            if args.execute:
                result = manager.execute_pipeline(builder, f"OpenAI Pipeline: {args.prompt[:30]}")
                print(f"🚀 Результат выполнения: {result}")
        
        elif args.command == "create-s3":
            if args.type == "upload":
                # Создание S3 upload пайплайна
                builder = manager.create_s3_upload_pipeline(
                    bucket_name=args.bucket,
                    aws_access_key_id=args.aws_key or "",
                    aws_secret_access_key=args.aws_secret or "",
                    region=args.region
                )
            else:
                # Создание S3 download пайплайна
                if not args.s3_key:
                    print("❌ Для download пайплайна требуется --s3-key")
                    return
                
                builder = manager.create_s3_download_pipeline(
                    s3_key=args.s3_key,
                    bucket_name=args.bucket,
                    aws_access_key_id=args.aws_key or "",
                    aws_secret_access_key=args.aws_secret or "",
                    region=args.region
                )
            
            if args.output:
                manager.save_pipeline_to_file(builder, args.output)
                print(f"✅ Пайплайн сохранен в {args.output}")
            
            if args.upload:
                result = manager.upload_pipeline(builder, f"S3 {args.type} Pipeline")
                print(f"📤 Результат загрузки: {result}")
        
        elif args.command == "create-complex":
            # Создание сложного пайплайна
            builder = manager.create_complex_pipeline(
                prompt=args.prompt,
                bucket_name=args.bucket,
                aws_access_key_id=args.aws_key or "",
                aws_secret_access_key=args.aws_secret or "",
                region=args.region
            )
            
            if args.output:
                manager.save_pipeline_to_file(builder, args.output)
                print(f"✅ Пайплайн сохранен в {args.output}")
            
            if args.upload:
                result = manager.upload_pipeline(builder, f"Complex Pipeline: {args.prompt[:30]}")
                print(f"📤 Результат загрузки: {result}")
            
            if args.execute:
                result = manager.execute_pipeline(builder, f"Complex Pipeline: {args.prompt[:30]}")
                print(f"🚀 Результат выполнения: {result}")
        
        elif args.command == "load":
            # Загрузка пайплайна из файла
            builder = manager.load_pipeline_from_file(args.file)
            
            if args.validate:
                validation = manager.validate_pipeline(builder)
                print(f"✅ Валидация: {validation}")
            
            if args.upload:
                result = manager.upload_pipeline(builder, f"Loaded Pipeline")
                print(f"📤 Результат загрузки: {result}")
            
            if args.execute:
                result = manager.execute_pipeline(builder, f"Loaded Pipeline")
                print(f"🚀 Результат выполнения: {result}")
        
        elif args.command == "nodes":
            # Получение списка узлов
            result = manager.list_available_nodes()
            if result["success"]:
                nodes = result["nodes"]
                print(f"📋 Доступно узлов: {len(nodes)}")
                for node_type in sorted(nodes.keys()):
                    print(f"  - {node_type}")
            else:
                print(f"❌ Ошибка получения узлов: {result['error']}")
    
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main()) 