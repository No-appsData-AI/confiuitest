#!/usr/bin/env python3
"""
ComfyUI Pipeline Builder
Автор: AI Assistant
Версия: 1.0.0

Класс для программного создания пайплайнов ComfyUI
"""

import json
import requests
import time
from typing import Dict, List, Optional, Tuple, Union, Any
from dataclasses import dataclass, asdict
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class NodeConfig:
    """Конфигурация узла ComfyUI"""
    node_type: str
    inputs: Dict[str, Any]
    position: Tuple[int, int] = (0, 0)
    size: Tuple[int, int] = (300, 200)
    title: Optional[str] = None
    description: Optional[str] = None


@dataclass
class Connection:
    """Соединение между узлами"""
    from_node: int
    from_output: int
    to_node: int
    to_input: int


class ComfyUIPipelineBuilder:
    """
    Строитель пайплайнов ComfyUI
    """
    
    def __init__(self, comfyui_url: str = "http://localhost:8188"):
        """
        Инициализация строителя пайплайнов
        
        Args:
            comfyui_url: URL ComfyUI сервера
        """
        self.comfyui_url = comfyui_url.rstrip('/')
        self.nodes: Dict[int, NodeConfig] = {}
        self.connections: List[Connection] = []
        self.next_node_id = 1
        self.next_link_id = 1
        
    def add_node(self, 
                 node_type: str, 
                 inputs: Dict[str, Any],
                 position: Tuple[int, int] = None,
                 size: Tuple[int, int] = None,
                 title: Optional[str] = None,
                 description: Optional[str] = None) -> int:
        """
        Добавление узла в пайплайн
        
        Args:
            node_type: Тип узла
            inputs: Входные параметры узла
            position: Позиция узла (x, y)
            size: Размер узла (width, height)
            title: Заголовок узла
            description: Описание узла
            
        Returns:
            ID добавленного узла
        """
        node_id = self.next_node_id
        self.next_node_id += 1
        
        # Автоматическое позиционирование если не указано
        if position is None:
            position = self._calculate_position(node_id)
        
        if size is None:
            size = self._get_default_size(node_type)
        
        node_config = NodeConfig(
            node_type=node_type,
            inputs=inputs,
            position=position,
            size=size,
            title=title,
            description=description
        )
        
        self.nodes[node_id] = node_config
        logger.info(f"✅ Добавлен узел {node_type} с ID {node_id}")
        
        return node_id
    
    def connect_nodes(self, 
                     from_node: int, 
                     from_output: int,
                     to_node: int, 
                     to_input: int) -> int:
        """
        Соединение узлов
        
        Args:
            from_node: ID исходного узла
            from_output: Номер выхода исходного узла
            to_node: ID целевого узла
            to_input: Номер входа целевого узла
            
        Returns:
            ID соединения
        """
        if from_node not in self.nodes:
            raise ValueError(f"Узел {from_node} не найден")
        if to_node not in self.nodes:
            raise ValueError(f"Узел {to_node} не найден")
        
        connection = Connection(
            from_node=from_node,
            from_output=from_output,
            to_node=to_node,
            to_input=to_input
        )
        
        self.connections.append(connection)
        link_id = self.next_link_id
        self.next_link_id += 1
        
        logger.info(f"🔗 Соединен узел {from_node}:{from_output} -> {to_node}:{to_input}")
        
        return link_id
    
    def _calculate_position(self, node_id: int) -> Tuple[int, int]:
        """Вычисление позиции для нового узла"""
        if not self.nodes:
            return (100, 100)
        
        # Простая стратегия: размещаем узлы в сетке
        nodes_per_row = 3
        row = (node_id - 1) // nodes_per_row
        col = (node_id - 1) % nodes_per_row
        
        x = 100 + col * 350
        y = 100 + row * 250
        
        return (x, y)
    
    def _get_default_size(self, node_type: str) -> Tuple[int, int]:
        """Получение размера по умолчанию для типа узла"""
        default_sizes = {
            "OpenAIImageGenerator": (300, 200),
            "S3ImageUploader": (300, 250),
            "S3ImageDownloader": (300, 200),
            "PreviewImage": (300, 200),
            "LoadImage": (300, 150),
            "SaveImage": (300, 150),
            "KSampler": (300, 200),
            "CheckpointLoaderSimple": (300, 150),
            "CLIPTextEncode": (300, 150),
            "VAEDecode": (300, 150),
            "VAEEncode": (300, 150),
            "LoraLoader": (300, 200),
            "ControlNetLoader": (300, 200),
        }
        
        return default_sizes.get(node_type, (300, 200))
    
    def build_workflow(self) -> Dict[str, Any]:
        """
        Сборка workflow в формате ComfyUI
        
        Returns:
            Словарь с workflow
        """
        workflow = {
            "last_node_id": self.next_node_id - 1,
            "last_link_id": self.next_link_id - 1,
            "nodes": [],
            "links": []
        }
        
        # Добавление узлов
        for node_id, node_config in self.nodes.items():
            node_data = {
                "id": node_id,
                "type": node_config.node_type,
                "pos": list(node_config.position),
                "size": {"0": node_config.size[0], "1": node_config.size[1]},
                "flags": {},
                "order": node_id - 1,
                "mode": 0,
                "inputs": node_config.inputs
            }
            
            if node_config.title:
                node_data["title"] = node_config.title
            if node_config.description:
                node_data["description"] = node_config.description
            
            workflow["nodes"].append(node_data)
        
        # Добавление соединений
        for i, connection in enumerate(self.connections):
            link_data = [
                i + 1,  # link_id
                connection.from_node,
                connection.from_output,
                connection.to_node,
                connection.to_input
            ]
            workflow["links"].append(link_data)
        
        return workflow
    
    def save_workflow(self, filepath: str) -> bool:
        """
        Сохранение workflow в файл
        
        Args:
            filepath: Путь к файлу для сохранения
            
        Returns:
            True если сохранение успешно
        """
        try:
            workflow = self.build_workflow()
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(workflow, f, indent=2, ensure_ascii=False)
            
            logger.info(f"💾 Workflow сохранен в {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка сохранения workflow: {e}")
            return False
    
    def load_workflow(self, filepath: str) -> bool:
        """
        Загрузка workflow из файла
        
        Args:
            filepath: Путь к файлу workflow
            
        Returns:
            True если загрузка успешна
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                workflow = json.load(f)
            
            # Очистка текущего состояния
            self.nodes.clear()
            self.connections.clear()
            
            # Загрузка узлов
            for node_data in workflow.get("nodes", []):
                node_config = NodeConfig(
                    node_type=node_data["type"],
                    inputs=node_data.get("inputs", {}),
                    position=tuple(node_data["pos"]),
                    size=(node_data["size"]["0"], node_data["size"]["1"]),
                    title=node_data.get("title"),
                    description=node_data.get("description")
                )
                
                self.nodes[node_data["id"]] = node_config
                self.next_node_id = max(self.next_node_id, node_data["id"] + 1)
            
            # Загрузка соединений
            for link_data in workflow.get("links", []):
                connection = Connection(
                    from_node=link_data[1],
                    from_output=link_data[2],
                    to_node=link_data[3],
                    to_input=link_data[4]
                )
                
                self.connections.append(connection)
                self.next_link_id = max(self.next_link_id, link_data[0] + 1)
            
            logger.info(f"📂 Workflow загружен из {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка загрузки workflow: {e}")
            return False
    
    def upload_to_comfyui(self, workflow_name: str = None) -> Dict[str, Any]:
        """
        Загрузка workflow в ComfyUI
        
        Args:
            workflow_name: Название workflow
            
        Returns:
            Результат загрузки
        """
        try:
            workflow = self.build_workflow()
            
            # Проверка доступности ComfyUI
            try:
                response = requests.get(f"{self.comfyui_url}/system_stats", timeout=5)
                if response.status_code != 200:
                    raise ConnectionError("ComfyUI недоступен")
            except Exception as e:
                raise ConnectionError(f"Не удается подключиться к ComfyUI: {e}")
            
            # Загрузка workflow через API
            upload_data = {
                "workflow": workflow
            }
            
            if workflow_name:
                upload_data["name"] = workflow_name
            
            response = requests.post(
                f"{self.comfyui_url}/workflow",
                json=upload_data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"✅ Workflow загружен в ComfyUI: {result.get('id', 'unknown')}")
                return {
                    "success": True,
                    "workflow_id": result.get("id"),
                    "message": "Workflow успешно загружен"
                }
            else:
                logger.error(f"❌ Ошибка загрузки: {response.status_code} - {response.text}")
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "message": "Ошибка загрузки workflow"
                }
                
        except Exception as e:
            logger.error(f"❌ Ошибка загрузки в ComfyUI: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Ошибка загрузки в ComfyUI"
            }
    
    def execute_workflow(self, 
                        workflow_name: str = None,
                        wait_for_completion: bool = True,
                        timeout: int = 300) -> Dict[str, Any]:
        """
        Выполнение workflow в ComfyUI
        
        Args:
            workflow_name: Название workflow
            wait_for_completion: Ожидать завершения выполнения
            timeout: Таймаут ожидания в секундах
            
        Returns:
            Результат выполнения
        """
        try:
            # Загрузка workflow
            upload_result = self.upload_to_comfyui(workflow_name)
            if not upload_result["success"]:
                return upload_result
            
            workflow_id = upload_result["workflow_id"]
            
            # Запуск выполнения
            execute_data = {
                "workflow_id": workflow_id
            }
            
            response = requests.post(
                f"{self.comfyui_url}/execute",
                json=execute_data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "message": "Ошибка запуска выполнения"
                }
            
            execution_id = response.json().get("execution_id")
            
            if not wait_for_completion:
                return {
                    "success": True,
                    "execution_id": execution_id,
                    "message": "Выполнение запущено"
                }
            
            # Ожидание завершения
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    status_response = requests.get(
                        f"{self.comfyui_url}/execution/{execution_id}/status",
                        timeout=10
                    )
                    
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        status = status_data.get("status")
                        
                        if status == "completed":
                            # Получение результатов
                            results_response = requests.get(
                                f"{self.comfyui_url}/execution/{execution_id}/results",
                                timeout=10
                            )
                            
                            if results_response.status_code == 200:
                                results = results_response.json()
                                return {
                                    "success": True,
                                    "execution_id": execution_id,
                                    "status": "completed",
                                    "results": results,
                                    "message": "Выполнение завершено успешно"
                                }
                        
                        elif status == "failed":
                            return {
                                "success": False,
                                "execution_id": execution_id,
                                "status": "failed",
                                "error": status_data.get("error", "Неизвестная ошибка"),
                                "message": "Выполнение завершилось с ошибкой"
                            }
                    
                    time.sleep(1)
                    
                except requests.exceptions.RequestException as e:
                    logger.warning(f"Ошибка получения статуса: {e}")
                    time.sleep(2)
            
            return {
                "success": False,
                "execution_id": execution_id,
                "error": "Таймаут ожидания",
                "message": "Превышен таймаут ожидания выполнения"
            }
            
        except Exception as e:
            logger.error(f"❌ Ошибка выполнения workflow: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Ошибка выполнения workflow"
            }
    
    def get_available_nodes(self) -> Dict[str, Any]:
        """
        Получение списка доступных узлов
        
        Returns:
            Словарь с информацией о доступных узлах
        """
        try:
            response = requests.get(
                f"{self.comfyui_url}/nodes",
                timeout=10
            )
            
            if response.status_code == 200:
                nodes_data = response.json()
                return {
                    "success": True,
                    "nodes": nodes_data,
                    "message": "Список узлов получен"
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "message": "Ошибка получения списка узлов"
                }
                
        except Exception as e:
            logger.error(f"❌ Ошибка получения списка узлов: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Ошибка получения списка узлов"
            }
    
    def validate_workflow(self) -> Dict[str, Any]:
        """
        Валидация workflow
        
        Returns:
            Результат валидации
        """
        errors = []
        warnings = []
        
        # Проверка узлов
        if not self.nodes:
            errors.append("Workflow не содержит узлов")
        
        # Проверка соединений
        for connection in self.connections:
            if connection.from_node not in self.nodes:
                errors.append(f"Соединение ссылается на несуществующий узел {connection.from_node}")
            if connection.to_node not in self.nodes:
                errors.append(f"Соединение ссылается на несуществующий узел {connection.to_node}")
        
        # Проверка изолированных узлов
        connected_nodes = set()
        for connection in self.connections:
            connected_nodes.add(connection.from_node)
            connected_nodes.add(connection.to_node)
        
        isolated_nodes = set(self.nodes.keys()) - connected_nodes
        if isolated_nodes:
            warnings.append(f"Обнаружены изолированные узлы: {isolated_nodes}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "node_count": len(self.nodes),
            "connection_count": len(self.connections)
        }
    
    def print_workflow_info(self):
        """Вывод информации о workflow"""
        print("📋 Информация о Workflow")
        print("=" * 40)
        print(f"Узлов: {len(self.nodes)}")
        print(f"Соединений: {len(self.connections)}")
        print()
        
        print("🔧 Узлы:")
        for node_id, node_config in self.nodes.items():
            print(f"  {node_id}: {node_config.node_type}")
            if node_config.title:
                print(f"    Заголовок: {node_config.title}")
            if node_config.description:
                print(f"    Описание: {node_config.description}")
        
        print()
        print("🔗 Соединения:")
        for connection in self.connections:
            print(f"  {connection.from_node}:{connection.from_output} -> {connection.to_node}:{connection.to_input}")
        
        # Валидация
        validation = self.validate_workflow()
        print()
        print("✅ Валидация:")
        print(f"  Валиден: {validation['valid']}")
        if validation['errors']:
            print("  Ошибки:")
            for error in validation['errors']:
                print(f"    ❌ {error}")
        if validation['warnings']:
            print("  Предупреждения:")
            for warning in validation['warnings']:
                print(f"    ⚠️ {warning}")


# Предопределенные шаблоны пайплайнов
class PipelineTemplates:
    """Шаблоны готовых пайплайнов"""
    
    @staticmethod
    def openai_to_s3_pipeline(prompt: str, 
                             bucket_name: str,
                             aws_access_key_id: str = "",
                             aws_secret_access_key: str = "") -> ComfyUIPipelineBuilder:
        """
        Создание пайплайна: OpenAI -> S3
        
        Args:
            prompt: Промпт для генерации
            bucket_name: Название S3 bucket
            aws_access_key_id: AWS Access Key ID
            aws_secret_access_key: AWS Secret Access Key
            
        Returns:
            Строитель пайплайна
        """
        builder = ComfyUIPipelineBuilder()
        
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
            description="Генерация изображения через OpenAI"
        )
        
        # Узел загрузки в S3
        s3_node = builder.add_node(
            node_type="S3ImageUploader",
            inputs={
                "bucket_name": bucket_name,
                "aws_access_key_id": aws_access_key_id,
                "aws_secret_access_key": aws_secret_access_key,
                "region_name": "us-east-1",
                "metadata": json.dumps({"source": "openai", "prompt": prompt})
            },
            title="S3 Uploader",
            description="Загрузка изображения в S3"
        )
        
        # Соединение
        builder.connect_nodes(openai_node, 0, s3_node, 0)
        
        return builder
    
    @staticmethod
    def s3_to_preview_pipeline(s3_key: str,
                              bucket_name: str,
                              aws_access_key_id: str = "",
                              aws_secret_access_key: str = "") -> ComfyUIPipelineBuilder:
        """
        Создание пайплайна: S3 -> Preview
        
        Args:
            s3_key: Ключ файла в S3
            bucket_name: Название S3 bucket
            aws_access_key_id: AWS Access Key ID
            aws_secret_access_key: AWS Secret Access Key
            
        Returns:
            Строитель пайплайна
        """
        builder = ComfyUIPipelineBuilder()
        
        # Узел скачивания из S3
        s3_node = builder.add_node(
            node_type="S3ImageDownloader",
            inputs={
                "s3_key": s3_key,
                "bucket_name": bucket_name,
                "aws_access_key_id": aws_access_key_id,
                "aws_secret_access_key": aws_secret_access_key,
                "region_name": "us-east-1"
            },
            title="S3 Downloader",
            description="Скачивание изображения из S3"
        )
        
        # Узел предварительного просмотра
        preview_node = builder.add_node(
            node_type="PreviewImage",
            inputs={},
            title="Image Preview",
            description="Предварительный просмотр изображения"
        )
        
        # Соединение
        builder.connect_nodes(s3_node, 0, preview_node, 0)
        
        return builder
    
    @staticmethod
    def workflow_save_pipeline(workflow_data: Dict[str, Any],
                             bucket_name: str,
                             workflow_name: str,
                             aws_access_key_id: str = "",
                             aws_secret_access_key: str = "") -> ComfyUIPipelineBuilder:
        """
        Создание пайплайна для сохранения workflow в S3
        
        Args:
            workflow_data: Данные workflow
            bucket_name: Название S3 bucket
            workflow_name: Название workflow
            aws_access_key_id: AWS Access Key ID
            aws_secret_access_key: AWS Secret Access Key
            
        Returns:
            Строитель пайплайна
        """
        builder = ComfyUIPipelineBuilder()
        
        # Узел сохранения workflow
        save_node = builder.add_node(
            node_type="S3WorkflowSaver",
            inputs={
                "workflow_data": json.dumps(workflow_data),
                "bucket_name": bucket_name,
                "aws_access_key_id": aws_access_key_id,
                "aws_secret_access_key": aws_secret_access_key,
                "region_name": "us-east-1",
                "workflow_name": workflow_name
            },
            title="Workflow Saver",
            description="Сохранение workflow в S3"
        )
        
        return builder


# Пример использования
if __name__ == "__main__":
    # Создание простого пайплайна
    builder = ComfyUIPipelineBuilder("http://localhost:8188")
    
    # Добавление узлов
    openai_node = builder.add_node(
        node_type="OpenAIImageGenerator",
        inputs={
            "prompt": "A beautiful sunset over mountains",
            "model": "dall-e-3",
            "size": "1024x1024"
        },
        title="Sunset Generator"
    )
    
    preview_node = builder.add_node(
        node_type="PreviewImage",
        inputs={},
        title="Preview"
    )
    
    # Соединение узлов
    builder.connect_nodes(openai_node, 0, preview_node, 0)
    
    # Вывод информации
    builder.print_workflow_info()
    
    # Сохранение в файл
    builder.save_workflow("generated_workflow.json")
    
    # Загрузка в ComfyUI
    result = builder.upload_to_comfyui("Test Pipeline")
    print(f"Результат загрузки: {result}") 