#!/usr/bin/env python3
"""
Настройки приложения ComfyUI Integration
Автор: AI Assistant
Версия: 1.0.0
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ComfyUISettings:
    """Настройки ComfyUI"""
    url: str = "http://localhost:8188"
    timeout: int = 30
    retry_attempts: int = 3
    retry_delay: int = 5


@dataclass
class AWSSettings:
    """Настройки AWS"""
    access_key_id: Optional[str] = None
    secret_access_key: Optional[str] = None
    region_name: str = "us-east-1"
    default_bucket: str = "comfyui-images"
    
    def __post_init__(self):
        # Получение из переменных окружения если не указаны
        if not self.access_key_id:
            self.access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        if not self.secret_access_key:
            self.secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        if not self.region_name:
            self.region_name = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')


@dataclass
class OpenAISettings:
    """Настройки OpenAI"""
    api_key: Optional[str] = None
    default_model: str = "dall-e-3"
    default_size: str = "1024x1024"
    default_quality: str = "standard"
    default_style: str = "vivid"
    
    def __post_init__(self):
        if not self.api_key:
            self.api_key = os.getenv('OPENAI_API_KEY')


@dataclass
class PipelineSettings:
    """Настройки Pipeline Builder"""
    default_node_size: tuple = (300, 200)
    grid_spacing: tuple = (350, 250)
    nodes_per_row: int = 3
    auto_positioning: bool = True
    validation_enabled: bool = True


class Settings:
    """Основной класс настроек"""
    
    def __init__(self):
        self.comfyui = ComfyUISettings()
        self.aws = AWSSettings()
        self.openai = OpenAISettings()
        self.pipeline = PipelineSettings()
    
    def validate(self) -> Dict[str, Any]:
        """Валидация настроек"""
        errors = []
        warnings = []
        
        # Проверка ComfyUI
        if not self.comfyui.url:
            errors.append("URL ComfyUI не указан")
        
        # Проверка AWS
        if not self.aws.access_key_id:
            warnings.append("AWS Access Key ID не настроен")
        if not self.aws.secret_access_key:
            warnings.append("AWS Secret Access Key не настроен")
        
        # Проверка OpenAI
        if not self.openai.api_key:
            warnings.append("OpenAI API Key не настроен")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразование в словарь"""
        return {
            "comfyui": {
                "url": self.comfyui.url,
                "timeout": self.comfyui.timeout,
                "retry_attempts": self.comfyui.retry_attempts,
                "retry_delay": self.comfyui.retry_delay
            },
            "aws": {
                "access_key_id": self.aws.access_key_id,
                "secret_access_key": "***" if self.aws.secret_access_key else None,
                "region_name": self.aws.region_name,
                "default_bucket": self.aws.default_bucket
            },
            "openai": {
                "api_key": "***" if self.openai.api_key else None,
                "default_model": self.openai.default_model,
                "default_size": self.openai.default_size,
                "default_quality": self.openai.default_quality,
                "default_style": self.openai.default_style
            },
            "pipeline": {
                "default_node_size": self.pipeline.default_node_size,
                "grid_spacing": self.pipeline.grid_spacing,
                "nodes_per_row": self.pipeline.nodes_per_row,
                "auto_positioning": self.pipeline.auto_positioning,
                "validation_enabled": self.pipeline.validation_enabled
            }
        }


# Глобальный экземпляр настроек
settings = Settings()


def load_settings_from_env():
    """Загрузка настроек из переменных окружения"""
    # ComfyUI
    if os.getenv('COMFYUI_URL'):
        settings.comfyui.url = os.getenv('COMFYUI_URL')
    if os.getenv('COMFYUI_TIMEOUT'):
        settings.comfyui.timeout = int(os.getenv('COMFYUI_TIMEOUT'))
    
    # AWS
    if os.getenv('AWS_ACCESS_KEY_ID'):
        settings.aws.access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    if os.getenv('AWS_SECRET_ACCESS_KEY'):
        settings.aws.secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    if os.getenv('AWS_DEFAULT_REGION'):
        settings.aws.region_name = os.getenv('AWS_DEFAULT_REGION')
    if os.getenv('AWS_DEFAULT_BUCKET'):
        settings.aws.default_bucket = os.getenv('AWS_DEFAULT_BUCKET')
    
    # OpenAI
    if os.getenv('OPENAI_API_KEY'):
        settings.openai.api_key = os.getenv('OPENAI_API_KEY')
    if os.getenv('OPENAI_DEFAULT_MODEL'):
        settings.openai.default_model = os.getenv('OPENAI_DEFAULT_MODEL')
    if os.getenv('OPENAI_DEFAULT_SIZE'):
        settings.openai.default_size = os.getenv('OPENAI_DEFAULT_SIZE')


def print_settings():
    """Вывод текущих настроек"""
    print("🔧 Текущие настройки:")
    print("=" * 50)
    
    config_dict = settings.to_dict()
    
    for section, values in config_dict.items():
        print(f"\n📋 {section.upper()}:")
        for key, value in values.items():
            if key in ['secret_access_key', 'api_key']:
                print(f"  {key}: {'***' if value else 'Не настроен'}")
            else:
                print(f"  {key}: {value}")
    
    # Валидация
    validation = settings.validate()
    print(f"\n✅ Валидация:")
    print(f"  Валидны: {validation['valid']}")
    
    if validation['errors']:
        print("  Ошибки:")
        for error in validation['errors']:
            print(f"    ❌ {error}")
    
    if validation['warnings']:
        print("  Предупреждения:")
        for warning in validation['warnings']:
            print(f"    ⚠️ {warning}")


# Автоматическая загрузка настроек при импорте
load_settings_from_env() 