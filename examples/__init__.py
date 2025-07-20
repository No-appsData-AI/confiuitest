"""
ComfyUI Integration Examples Package
Автор: AI Assistant
Версия: 1.0.0

Пакет с примерами интеграции ComfyUI с внешними сервисами
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
    # Основные компоненты
    'ComfyUIPipelineBuilder',
    'PipelineTemplates',
    'PipelineManager',
    'S3StorageManager',
    'OpenAIImageGenerator',
    
    # S3 узлы
    'S3ImageUploader',
    'S3ImageDownloader',
    'S3ImageLister',
    'S3WorkflowSaver',
    'S3WorkflowLoader',
    'S3StorageInfo',
    
    # OpenAI узлы
    'OpenAIImageNode',
    'OpenAIImageVariationNode'
] 