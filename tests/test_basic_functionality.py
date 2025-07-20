#!/usr/bin/env python3
"""
Автоматизированные тесты для ComfyUI Integration
Автор: AI Assistant
Версия: 1.0.0

Комплексное тестирование всех компонентов системы
"""

import unittest
import os
import sys
import json
import tempfile
from unittest.mock import patch, MagicMock
from typing import Dict, Any

# Добавление пути к модулям
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Импорт тестируемых модулей
try:
    from examples.comfyui_pipeline_builder import ComfyUIPipelineBuilder, PipelineTemplates
    from examples.pipeline_manager import PipelineManager
    from examples.s3_storage_manager import S3StorageManager
    from examples.openai_image_generator import OpenAIImageGenerator
    from config.settings import ComfyUISettings, AWSSettings, OpenAISettings, PipelineBuilderSettings
except ImportError as e:
    print(f"❌ Ошибка импорта модулей: {e}")
    sys.exit(1)


class TestPipelineBuilder(unittest.TestCase):
    """Тесты для Pipeline Builder"""
    
    def setUp(self):
        """Настройка тестов"""
        self.builder = ComfyUIPipelineBuilder()
    
    def test_create_basic_pipeline(self):
        """Тест создания базового пайплайна"""
        # Добавление узла
        node_id = self.builder.add_node(
            node_type="PreviewImage",
            inputs={},
            title="Test Preview",
            description="Тестовый узел предварительного просмотра"
        )
        
        self.assertEqual(node_id, 1)
        self.assertIn(node_id, self.builder.nodes)
        self.assertEqual(self.builder.nodes[node_id].node_type, "PreviewImage")
    
    def test_connect_nodes(self):
        """Тест соединения узлов"""
        # Создание двух узлов
        node1 = self.builder.add_node("PreviewImage", {})
        node2 = self.builder.add_node("PreviewImage", {})
        
        # Соединение узлов
        connection_id = self.builder.connect_nodes(node1, 0, node2, 0)
        
        self.assertEqual(len(self.builder.connections), 1)
        self.assertEqual(self.builder.connections[0].from_node, node1)
        self.assertEqual(self.builder.connections[0].to_node, node2)
    
    def test_build_workflow(self):
        """Тест сборки workflow"""
        # Создание простого пайплайна
        node_id = self.builder.add_node("PreviewImage", {})
        
        # Сборка workflow
        workflow = self.builder.build_workflow()
        
        self.assertIsInstance(workflow, dict)
        self.assertIn("nodes", workflow)
        self.assertIn("links", workflow)
        self.assertEqual(len(workflow["nodes"]), 1)
        self.assertEqual(workflow["last_node_id"], 1)
    
    def test_validate_workflow(self):
        """Тест валидации workflow"""
        # Создание валидного пайплайна
        node_id = self.builder.add_node("PreviewImage", {})
        
        # Валидация
        validation = self.builder.validate_workflow()
        
        self.assertIsInstance(validation, dict)
        self.assertIn("valid", validation)
        self.assertTrue(validation["valid"])
    
    def test_save_load_workflow(self):
        """Тест сохранения и загрузки workflow"""
        # Создание пайплайна
        node_id = self.builder.add_node("PreviewImage", {})
        
        # Сохранение
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            success = self.builder.save_workflow(temp_file)
            self.assertTrue(success)
            
            # Создание нового строителя и загрузка
            new_builder = ComfyUIPipelineBuilder()
            success = new_builder.load_workflow(temp_file)
            self.assertTrue(success)
            
            # Проверка загруженных данных
            self.assertEqual(len(new_builder.nodes), 1)
            self.assertEqual(new_builder.nodes[1].node_type, "PreviewImage")
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestPipelineTemplates(unittest.TestCase):
    """Тесты для шаблонов пайплайнов"""
    
    def test_openai_to_s3_template(self):
        """Тест шаблона OpenAI -> S3"""
        builder = PipelineTemplates.openai_to_s3_pipeline(
            prompt="Test prompt",
            bucket_name="test-bucket"
        )
        
        self.assertIsInstance(builder, ComfyUIPipelineBuilder)
        self.assertGreater(len(builder.nodes), 0)
        self.assertGreater(len(builder.connections), 0)
        
        # Проверка наличия нужных узлов
        node_types = [node.node_type for node in builder.nodes.values()]
        self.assertIn("OpenAIImageGenerator", node_types)
        self.assertIn("S3ImageUploader", node_types)
    
    def test_s3_to_preview_template(self):
        """Тест шаблона S3 -> Preview"""
        builder = PipelineTemplates.s3_to_preview_pipeline(
            s3_key="test/image.jpg",
            bucket_name="test-bucket"
        )
        
        self.assertIsInstance(builder, ComfyUIPipelineBuilder)
        self.assertGreater(len(builder.nodes), 0)
        self.assertGreater(len(builder.connections), 0)
        
        # Проверка наличия нужных узлов
        node_types = [node.node_type for node in builder.nodes.values()]
        self.assertIn("S3ImageDownloader", node_types)
        self.assertIn("PreviewImage", node_types)


class TestPipelineManager(unittest.TestCase):
    """Тесты для Pipeline Manager"""
    
    def setUp(self):
        """Настройка тестов"""
        self.manager = PipelineManager()
    
    def test_create_openai_pipeline(self):
        """Тест создания OpenAI пайплайна"""
        builder = self.manager.create_openai_pipeline(
            prompt="Beautiful sunset",
            model="dall-e-3",
            size="1024x1024"
        )
        
        self.assertIsInstance(builder, ComfyUIPipelineBuilder)
        self.assertGreater(len(builder.nodes), 0)
        
        # Проверка настроек узла OpenAI
        openai_nodes = [node for node in builder.nodes.values() 
                       if node.node_type == "OpenAIImageGenerator"]
        self.assertGreater(len(openai_nodes), 0)
        
        openai_node = openai_nodes[0]
        self.assertEqual(openai_node.inputs["prompt"], "Beautiful sunset")
        self.assertEqual(openai_node.inputs["model"], "dall-e-3")
    
    def test_create_s3_pipeline(self):
        """Тест создания S3 пайплайна"""
        builder = self.manager.create_s3_upload_pipeline(
            bucket_name="test-bucket",
            region="us-east-1"
        )
        
        self.assertIsInstance(builder, ComfyUIPipelineBuilder)
        self.assertGreater(len(builder.nodes), 0)
        
        # Проверка настроек узла S3
        s3_nodes = [node for node in builder.nodes.values() 
                   if node.node_type == "S3ImageUploader"]
        self.assertGreater(len(s3_nodes), 0)
        
        s3_node = s3_nodes[0]
        self.assertEqual(s3_node.inputs["bucket_name"], "test-bucket")
        self.assertEqual(s3_node.inputs["region_name"], "us-east-1")
    
    def test_validate_pipeline(self):
        """Тест валидации пайплайна"""
        builder = self.manager.create_openai_pipeline("Test prompt")
        validation = self.manager.validate_pipeline(builder)
        
        self.assertIsInstance(validation, dict)
        self.assertIn("valid", validation)
        self.assertTrue(validation["valid"])


class TestSettings(unittest.TestCase):
    """Тесты для настроек"""
    
    def test_settings_initialization(self):
        """Тест инициализации настроек"""
        comfyui_settings = ComfyUISettings()
        aws_settings = AWSSettings()
        openai_settings = OpenAISettings()
        pipeline_settings = PipelineBuilderSettings()
        
        self.assertIsNotNone(comfyui_settings)
        self.assertIsNotNone(aws_settings)
        self.assertIsNotNone(openai_settings)
        self.assertIsNotNone(pipeline_settings)
    
    def test_settings_validation(self):
        """Тест валидации настроек"""
        # Тест с валидными настройками
        comfyui_settings = ComfyUISettings(url="http://localhost:8188")
        self.assertEqual(comfyui_settings.url, "http://localhost:8188")
        
        # Тест с невалидными настройками (должно использовать значения по умолчанию)
        aws_settings = AWSSettings(access_key_id="", secret_access_key="")
        self.assertEqual(aws_settings.access_key_id, "")
    
    def test_settings_to_dict(self):
        """Тест преобразования настроек в словарь"""
        comfyui_settings = ComfyUISettings(url="http://test:8188")
        settings_dict = comfyui_settings.to_dict()
        
        self.assertIsInstance(settings_dict, dict)
        self.assertEqual(settings_dict["url"], "http://test:8188")


class TestS3StorageManager(unittest.TestCase):
    """Тесты для S3 Storage Manager"""
    
    @patch('boto3.client')
    def test_s3_manager_initialization(self, mock_boto3):
        """Тест инициализации S3 менеджера"""
        mock_s3 = MagicMock()
        mock_s3.head_bucket.return_value = {}
        mock_boto3.return_value = mock_s3
        
        s3_manager = S3StorageManager(
            bucket_name="test-bucket",
            aws_access_key_id="test-key",
            aws_secret_access_key="test-secret"
        )
        
        self.assertIsNotNone(s3_manager)
        mock_boto3.assert_called_once()
    
    @patch('boto3.client')
    def test_verify_bucket_access(self, mock_boto3):
        """Тест проверки доступа к bucket"""
        mock_s3 = MagicMock()
        mock_s3.head_bucket.return_value = {}
        mock_boto3.return_value = mock_s3
        
        s3_manager = S3StorageManager(
            bucket_name="test-bucket",
            aws_access_key_id="test-key",
            aws_secret_access_key="test-secret"
        )
        
        result = s3_manager._check_bucket_access()
        
        self.assertIsInstance(result, bool)
        self.assertTrue(result)


class TestOpenAIImageGenerator(unittest.TestCase):
    """Тесты для OpenAI Image Generator"""
    
    def test_generator_initialization(self):
        """Тест инициализации генератора"""
        generator = OpenAIImageGenerator("test-api-key")
        
        self.assertIsNotNone(generator)
        self.assertEqual(generator.api_key, "test-api-key")
    
    @patch('openai.OpenAI')
    def test_generate_image(self, mock_openai):
        """Тест генерации изображения"""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.data = [MagicMock(url="https://example.com/image.png")]
        mock_client.images.generate.return_value = mock_response
        mock_openai.return_value = mock_client
        
        generator = OpenAIImageGenerator("test-api-key")
        result = generator.generate_image("Test prompt")
        
        self.assertIsInstance(result, dict)
        self.assertIn("success", result)


def run_basic_tests():
    """Запуск базовых тестов"""
    print("🧪 Запуск базовых тестов ComfyUI Integration")
    print("=" * 50)
    
    # Создание тестового набора
    test_suite = unittest.TestSuite()
    
    # Добавление тестов
    test_classes = [
        TestPipelineBuilder,
        TestPipelineTemplates,
        TestPipelineManager,
        TestSettings,
        TestS3StorageManager,
        TestOpenAIImageGenerator
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Запуск тестов
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Вывод результатов
    print("\n📊 Результаты тестирования:")
    print(f"  Тестов выполнено: {result.testsRun}")
    print(f"  Успешно: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"  Ошибок: {len(result.errors)}")
    print(f"  Провалов: {len(result.failures)}")
    
    if result.wasSuccessful():
        print("  ✅ Все тесты прошли успешно!")
        return True
    else:
        print("  ❌ Обнаружены проблемы в тестах")
        return False


def test_imports():
    """Тест импорта всех модулей"""
    print("📦 Тестирование импорта модулей...")
    
    modules_to_test = [
        "examples.comfyui_pipeline_builder",
        "examples.pipeline_manager",
        "examples.s3_storage_manager",
        "examples.openai_image_generator",
        "config.settings"
    ]
    
    failed_imports = []
    
    for module_name in modules_to_test:
        try:
            __import__(module_name)
            print(f"  ✅ {module_name}")
        except ImportError as e:
            print(f"  ❌ {module_name}: {e}")
            failed_imports.append(module_name)
    
    if failed_imports:
        print(f"\n⚠️ Проблемы с импортом: {len(failed_imports)} модулей")
        return False
    else:
        print("\n✅ Все модули импортированы успешно")
        return True


def test_dependencies():
    """Тест доступности зависимостей"""
    print("🔧 Тестирование зависимостей...")
    
    dependencies = [
        "requests",
        "boto3",
        "botocore",
        "PIL",
        "numpy",
        "openai",
        "dataclasses",
        "json",
        "logging"
    ]
    
    missing_deps = []
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"  ✅ {dep}")
        except ImportError:
            print(f"  ❌ {dep}")
            missing_deps.append(dep)
    
    if missing_deps:
        print(f"\n⚠️ Отсутствуют зависимости: {missing_deps}")
        print("Установите их командой: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ Все зависимости доступны")
        return True


def test_comfyui_integration():
    """Тест интеграции с ComfyUI"""
    print("🌐 Тестирование интеграции с ComfyUI...")
    
    try:
        import requests
        
        # Проверка доступности ComfyUI
        try:
            response = requests.get("http://localhost:8188/system_stats", timeout=5)
            if response.status_code == 200:
                print("  ✅ ComfyUI доступен")
                return True
            else:
                print("  ⚠️ ComfyUI отвечает, но с ошибкой")
                return False
        except requests.exceptions.RequestException:
            print("  ⚠️ ComfyUI недоступен (возможно, не запущен)")
            print("  💡 Запустите ComfyUI: python main.py --listen 0.0.0.0 --port 8188")
            return False
            
    except ImportError:
        print("  ❌ Модуль requests не установлен")
        return False


def test_external_services():
    """Тест внешних сервисов"""
    print("🔗 Тестирование внешних сервисов...")
    
    # Проверка AWS S3 (без реальных ключей)
    print("  ⚠️ AWS S3 - требует настройки ключей")
    
    # Проверка OpenAI (без реального ключа)
    print("  ⚠️ OpenAI API - требует настройки ключа")
    
    print("  💡 Настройте API ключи в переменных окружения для полного тестирования")
    return True


def main():
    """Основная функция тестирования"""
    print("🎯 Комплексное тестирование ComfyUI Integration")
    print("=" * 60)
    
    # Тест зависимостей
    deps_ok = test_dependencies()
    print()
    
    # Тест импортов
    imports_ok = test_imports()
    print()
    
    # Тест интеграции с ComfyUI
    comfyui_ok = test_comfyui_integration()
    print()
    
    # Тест внешних сервисов
    services_ok = test_external_services()
    print()
    
    # Базовые тесты (только если импорты прошли успешно)
    if imports_ok:
        tests_ok = run_basic_tests()
    else:
        tests_ok = False
        print("⏭️ Пропуск базовых тестов из-за проблем с импортом")
    
    # Итоговый результат
    print("\n" + "=" * 60)
    print("📋 ИТОГОВЫЙ РЕЗУЛЬТАТ:")
    
    if deps_ok and imports_ok and tests_ok:
        print("🎉 Все тесты прошли успешно!")
        print("✅ Система готова к использованию")
        
        if comfyui_ok:
            print("🌐 ComfyUI доступен и готов к работе")
        else:
            print("⚠️ ComfyUI недоступен - запустите сервис для полной функциональности")
            
        return 0
    else:
        print("❌ Обнаружены проблемы:")
        if not deps_ok:
            print("  - Проблемы с зависимостями")
        if not imports_ok:
            print("  - Проблемы с импортом модулей")
        if not tests_ok:
            print("  - Проблемы в функциональных тестах")
        if not comfyui_ok:
            print("  - ComfyUI недоступен")
        print("\n🔧 Рекомендации:")
        print("  1. Установите зависимости: pip install -r requirements.txt")
        print("  2. Проверьте структуру проекта")
        print("  3. Убедитесь в корректности кода")
        print("  4. Запустите ComfyUI для полной функциональности")
        return 1


if __name__ == "__main__":
    exit(main()) 