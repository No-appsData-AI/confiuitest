#!/usr/bin/env python3
"""
Примеры использования Pipeline Builder
Автор: AI Assistant
Версия: 1.0.0

Примеры создания различных пайплайнов ComfyUI
"""

import json
import os
from .comfyui_pipeline_builder import ComfyUIPipelineBuilder, PipelineTemplates
from .pipeline_manager import PipelineManager


def example_simple_openai_pipeline():
    """Пример простого пайплайна с OpenAI"""
    print("🎨 Создание простого OpenAI пайплайна...")
    
    # Создание строителя
    builder = ComfyUIPipelineBuilder("http://localhost:8188")
    
    # Добавление узла генерации OpenAI
    openai_node = builder.add_node(
        node_type="OpenAIImageGenerator",
        inputs={
            "prompt": "A beautiful sunset over mountains, digital art style",
            "api_key": "",
            "model": "dall-e-3",
            "size": "1024x1024",
            "quality": "standard",
            "style": "vivid"
        },
        title="Sunset Generator",
        description="Генерация красивого заката"
    )
    
    # Добавление узла предварительного просмотра
    preview_node = builder.add_node(
        node_type="PreviewImage",
        inputs={},
        title="Preview",
        description="Предварительный просмотр"
    )
    
    # Соединение узлов
    builder.connect_nodes(openai_node, 0, preview_node, 0)
    
    # Вывод информации
    builder.print_workflow_info()
    
    # Сохранение в файл
    builder.save_workflow("examples/simple_openai_pipeline.json")
    
    print("✅ Простой OpenAI пайплайн создан!")


def example_s3_integration_pipeline():
    """Пример пайплайна с интеграцией S3"""
    print("☁️ Создание пайплайна с интеграцией S3...")
    
    # Создание строителя
    builder = ComfyUIPipelineBuilder("http://localhost:8188")
    
    # Узел генерации OpenAI
    openai_node = builder.add_node(
        node_type="OpenAIImageGenerator",
        inputs={
            "prompt": "A futuristic city with flying cars, neon lights",
            "api_key": "",
            "model": "dall-e-3",
            "size": "1024x1024",
            "quality": "hd",
            "style": "vivid"
        },
        title="Futuristic City Generator",
        description="Генерация футуристического города"
    )
    
    # Узел загрузки в S3
    s3_upload_node = builder.add_node(
        node_type="S3ImageUploader",
        inputs={
            "bucket_name": "comfyui-images",
            "aws_access_key_id": "",
            "aws_secret_access_key": "",
            "region_name": "us-east-1",
            "metadata": json.dumps({
                "prompt": "A futuristic city with flying cars, neon lights",
                "model": "dall-e-3",
                "category": "futuristic"
            })
        },
        title="S3 Uploader",
        description="Загрузка в облачное хранилище"
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
    
    # Вывод информации
    builder.print_workflow_info()
    
    # Сохранение в файл
    builder.save_workflow("examples/s3_integration_pipeline.json")
    
    print("✅ Пайплайн с интеграцией S3 создан!")


def example_workflow_management_pipeline():
    """Пример пайплайна для управления workflows"""
    print("📋 Создание пайплайна для управления workflows...")
    
    # Создание строителя
    builder = ComfyUIPipelineBuilder("http://localhost:8188")
    
    # Узел сохранения workflow
    save_node = builder.add_node(
        node_type="S3WorkflowSaver",
        inputs={
            "workflow_data": json.dumps({
                "name": "Example Workflow",
                "version": "1.0.0",
                "description": "Пример workflow для демонстрации",
                "author": "AI Assistant",
                "created_at": "2024-12-01T12:00:00Z"
            }),
            "bucket_name": "comfyui-images",
            "aws_access_key_id": "",
            "aws_secret_access_key": "",
            "region_name": "us-east-1",
            "workflow_name": "example_workflow.json"
        },
        title="Workflow Saver",
        description="Сохранение workflow в S3"
    )
    
    # Узел загрузки workflow
    load_node = builder.add_node(
        node_type="S3WorkflowLoader",
        inputs={
            "workflow_name": "example_workflow.json",
            "bucket_name": "comfyui-images",
            "aws_access_key_id": "",
            "aws_secret_access_key": "",
            "region_name": "us-east-1"
        },
        title="Workflow Loader",
        description="Загрузка workflow из S3"
    )
    
    # Узел информации о хранилище
    info_node = builder.add_node(
        node_type="S3StorageInfo",
        inputs={
            "bucket_name": "comfyui-images",
            "aws_access_key_id": "",
            "aws_secret_access_key": "",
            "region_name": "us-east-1"
        },
        title="Storage Info",
        description="Информация о хранилище"
    )
    
    # Вывод информации
    builder.print_workflow_info()
    
    # Сохранение в файл
    builder.save_workflow("examples/workflow_management_pipeline.json")
    
    print("✅ Пайплайн для управления workflows создан!")


def example_batch_processing_pipeline():
    """Пример пайплайна для пакетной обработки"""
    print("🔄 Создание пайплайна для пакетной обработки...")
    
    # Создание строителя
    builder = ComfyUIPipelineBuilder("http://localhost:8188")
    
    # Узел списка изображений
    lister_node = builder.add_node(
        node_type="S3ImageLister",
        inputs={
            "bucket_name": "comfyui-images",
            "aws_access_key_id": "",
            "aws_secret_access_key": "",
            "region_name": "us-east-1",
            "prefix": "comfyui/images/",
            "max_keys": 10
        },
        title="Image Lister",
        description="Получение списка изображений"
    )
    
    # Узел скачивания изображения
    download_node = builder.add_node(
        node_type="S3ImageDownloader",
        inputs={
            "s3_key": "comfyui/images/20241201_120000_image.png",
            "bucket_name": "comfyui-images",
            "aws_access_key_id": "",
            "aws_secret_access_key": "",
            "region_name": "us-east-1"
        },
        title="Image Downloader",
        description="Скачивание изображения"
    )
    
    # Узел предварительного просмотра
    preview_node = builder.add_node(
        node_type="PreviewImage",
        inputs={},
        title="Preview",
        description="Предварительный просмотр"
    )
    
    # Узел загрузки обработанного изображения
    upload_node = builder.add_node(
        node_type="S3ImageUploader",
        inputs={
            "bucket_name": "comfyui-images",
            "aws_access_key_id": "",
            "aws_secret_access_key": "",
            "region_name": "us-east-1",
            "metadata": json.dumps({"processed": True, "batch": "example"})
        },
        title="Processed Uploader",
        description="Загрузка обработанного изображения"
    )
    
    # Соединения
    builder.connect_nodes(download_node, 0, preview_node, 0)
    builder.connect_nodes(download_node, 0, upload_node, 0)
    
    # Вывод информации
    builder.print_workflow_info()
    
    # Сохранение в файл
    builder.save_workflow("examples/batch_processing_pipeline.json")
    
    print("✅ Пайплайн для пакетной обработки создан!")


def example_using_pipeline_manager():
    """Пример использования Pipeline Manager"""
    print("🛠️ Использование Pipeline Manager...")
    
    # Создание менеджера
    manager = PipelineManager("http://localhost:8188")
    
    # Создание OpenAI пайплайна
    print("Создание OpenAI пайплайна...")
    openai_builder = manager.create_openai_pipeline(
        prompt="A magical forest with glowing mushrooms and fairy lights",
        model="dall-e-3",
        size="1024x1024"
    )
    
    # Сохранение пайплайна
    manager.save_pipeline_to_file(openai_builder, "examples/magical_forest_pipeline.json")
    
    # Валидация пайплайна
    validation = manager.validate_pipeline(openai_builder)
    print(f"Валидация: {validation}")
    
    # Создание сложного пайплайна
    print("Создание сложного пайплайна...")
    complex_builder = manager.create_complex_pipeline(
        prompt="A steampunk airship flying over Victorian London",
        bucket_name="comfyui-images",
        aws_access_key_id="",
        aws_secret_access_key=""
    )
    
    # Сохранение сложного пайплайна
    manager.save_pipeline_to_file(complex_builder, "examples/steampunk_airship_pipeline.json")
    
    print("✅ Примеры с Pipeline Manager созданы!")


def example_using_templates():
    """Пример использования шаблонов"""
    print("📝 Использование шаблонов пайплайнов...")
    
    # Шаблон OpenAI -> S3
    print("Создание шаблона OpenAI -> S3...")
    template_builder = PipelineTemplates.openai_to_s3_pipeline(
        prompt="A cyberpunk street scene with neon signs and rain",
        bucket_name="comfyui-images",
        aws_access_key_id="",
        aws_secret_access_key=""
    )
    
    # Сохранение шаблона
    template_builder.save_workflow("examples/cyberpunk_template.json")
    
    # Шаблон S3 -> Preview
    print("Создание шаблона S3 -> Preview...")
    download_template = PipelineTemplates.s3_to_preview_pipeline(
        s3_key="comfyui/images/cyberpunk_street.png",
        bucket_name="comfyui-images",
        aws_access_key_id="",
        aws_secret_access_key=""
    )
    
    # Сохранение шаблона
    download_template.save_workflow("examples/download_template.json")
    
    print("✅ Шаблоны пайплайнов созданы!")


def example_advanced_pipeline():
    """Пример продвинутого пайплайна с множественными узлами"""
    print("🚀 Создание продвинутого пайплайна...")
    
    # Создание строителя
    builder = ComfyUIPipelineBuilder("http://localhost:8188")
    
    # Узел генерации OpenAI
    openai_node = builder.add_node(
        node_type="OpenAIImageGenerator",
        inputs={
            "prompt": "A majestic dragon flying over a medieval castle at sunset",
            "api_key": "",
            "model": "dall-e-3",
            "size": "1024x1024",
            "quality": "hd",
            "style": "vivid"
        },
        title="Dragon Generator",
        description="Генерация дракона над замком"
    )
    
    # Узел загрузки в S3
    s3_upload_node = builder.add_node(
        node_type="S3ImageUploader",
        inputs={
            "bucket_name": "comfyui-images",
            "aws_access_key_id": "",
            "aws_secret_access_key": "",
            "region_name": "us-east-1",
            "metadata": json.dumps({
                "prompt": "A majestic dragon flying over a medieval castle at sunset",
                "model": "dall-e-3",
                "category": "fantasy",
                "quality": "hd"
            })
        },
        title="S3 Uploader",
        description="Загрузка в облачное хранилище"
    )
    
    # Узел предварительного просмотра
    preview_node = builder.add_node(
        node_type="PreviewImage",
        inputs={},
        title="Preview",
        description="Предварительный просмотр"
    )
    
    # Узел информации о хранилище
    info_node = builder.add_node(
        node_type="S3StorageInfo",
        inputs={
            "bucket_name": "comfyui-images",
            "aws_access_key_id": "",
            "aws_secret_access_key": "",
            "region_name": "us-east-1"
        },
        title="Storage Info",
        description="Информация о хранилище"
    )
    
    # Узел сохранения workflow
    workflow_save_node = builder.add_node(
        node_type="S3WorkflowSaver",
        inputs={
            "workflow_data": json.dumps({
                "name": "Dragon Castle Workflow",
                "version": "1.0.0",
                "description": "Пайплайн для генерации дракона над замком",
                "author": "AI Assistant",
                "created_at": "2024-12-01T12:00:00Z"
            }),
            "bucket_name": "comfyui-images",
            "aws_access_key_id": "",
            "aws_secret_access_key": "",
            "region_name": "us-east-1",
            "workflow_name": "dragon_castle_workflow.json"
        },
        title="Workflow Saver",
        description="Сохранение workflow"
    )
    
    # Соединения
    builder.connect_nodes(openai_node, 0, s3_upload_node, 0)
    builder.connect_nodes(openai_node, 0, preview_node, 0)
    
    # Вывод информации
    builder.print_workflow_info()
    
    # Сохранение в файл
    builder.save_workflow("examples/advanced_dragon_pipeline.json")
    
    print("✅ Продвинутый пайплайн создан!")


def main():
    """Основная функция для запуска примеров"""
    print("🎯 Запуск примеров Pipeline Builder")
    print("=" * 50)
    
    # Создание директории для примеров
    os.makedirs("examples", exist_ok=True)
    
    try:
        # Запуск всех примеров
        example_simple_openai_pipeline()
        print()
        
        example_s3_integration_pipeline()
        print()
        
        example_workflow_management_pipeline()
        print()
        
        example_batch_processing_pipeline()
        print()
        
        example_using_pipeline_manager()
        print()
        
        example_using_templates()
        print()
        
        example_advanced_pipeline()
        print()
        
        print("🎉 Все примеры успешно созданы!")
        print("\n📁 Созданные файлы:")
        
        # Вывод списка созданных файлов
        example_files = [
            "simple_openai_pipeline.json",
            "s3_integration_pipeline.json",
            "workflow_management_pipeline.json",
            "batch_processing_pipeline.json",
            "magical_forest_pipeline.json",
            "steampunk_airship_pipeline.json",
            "cyberpunk_template.json",
            "download_template.json",
            "advanced_dragon_pipeline.json"
        ]
        
        for file in example_files:
            filepath = f"examples/{file}"
            if os.path.exists(filepath):
                print(f"  ✅ {filepath}")
            else:
                print(f"  ❌ {filepath} (не найден)")
        
        print("\n🚀 Для использования пайплайнов:")
        print("1. Загрузите файлы в ComfyUI через веб-интерфейс")
        print("2. Или используйте Pipeline Manager для автоматической загрузки")
        print("3. Настройте API ключи и параметры в узлах")
        
    except Exception as e:
        print(f"❌ Ошибка при создании примеров: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main()) 