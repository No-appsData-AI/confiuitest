# Pipeline Builder для ComfyUI

## Обзор

Pipeline Builder - это мощный инструмент для программного создания пайплайнов ComfyUI. Позволяет создавать сложные workflows с помощью кода, автоматизировать процесс разработки и интегрировать ComfyUI в ваши приложения.

## 🎯 Возможности

### Основные функции:
- **Программное создание** пайплайнов ComfyUI
- **Автоматическое позиционирование** узлов
- **Валидация** workflows
- **Загрузка в ComfyUI** через API
- **Выполнение** пайплайнов программно
- **Шаблоны** готовых решений
- **Интеграция с S3** хранилищем

### Преимущества:
- ✅ **Гибкость** - полный контроль над созданием пайплайнов
- ✅ **Автоматизация** - создание workflows программно
- ✅ **Переиспользование** - шаблоны и компоненты
- ✅ **Интеграция** - работа с внешними системами
- ✅ **Валидация** - проверка корректности пайплайнов
- ✅ **Масштабируемость** - создание сложных систем

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
pip install requests
```

### 2. Базовый пример

```python
from comfyui_pipeline_builder import ComfyUIPipelineBuilder

# Создание строителя
builder = ComfyUIPipelineBuilder("http://localhost:8188")

# Добавление узла генерации OpenAI
openai_node = builder.add_node(
    node_type="OpenAIImageGenerator",
    inputs={
        "prompt": "A beautiful sunset over mountains",
        "model": "dall-e-3",
        "size": "1024x1024"
    },
    title="Sunset Generator"
)

# Добавление узла предварительного просмотра
preview_node = builder.add_node(
    node_type="PreviewImage",
    inputs={},
    title="Preview"
)

# Соединение узлов
builder.connect_nodes(openai_node, 0, preview_node, 0)

# Сохранение в файл
builder.save_workflow("my_pipeline.json")

# Загрузка в ComfyUI
result = builder.upload_to_comfyui("My Pipeline")
print(result)
```

### 3. Выполнение пайплайна

```python
# Выполнение с ожиданием результата
result = builder.execute_workflow("My Pipeline", wait_for_completion=True)
print(f"Результат: {result}")
```

## 📋 API Reference

### ComfyUIPipelineBuilder

#### Инициализация

```python
builder = ComfyUIPipelineBuilder(comfyui_url="http://localhost:8188")
```

**Параметры:**
- `comfyui_url` - URL ComfyUI сервера

#### Добавление узлов

```python
node_id = builder.add_node(
    node_type="OpenAIImageGenerator",
    inputs={
        "prompt": "Your prompt here",
        "model": "dall-e-3",
        "size": "1024x1024"
    },
    position=(100, 100),  # опционально
    size=(300, 200),      # опционально
    title="My Node",      # опционально
    description="Description"  # опционально
)
```

**Параметры:**
- `node_type` - тип узла ComfyUI
- `inputs` - входные параметры узла
- `position` - позиция узла (x, y)
- `size` - размер узла (width, height)
- `title` - заголовок узла
- `description` - описание узла

**Возвращает:** ID добавленного узла

#### Соединение узлов

```python
link_id = builder.connect_nodes(
    from_node=1,
    from_output=0,
    to_node=2,
    to_input=0
)
```

**Параметры:**
- `from_node` - ID исходного узла
- `from_output` - номер выхода исходного узла
- `to_node` - ID целевого узла
- `to_input` - номер входа целевого узла

**Возвращает:** ID соединения

#### Сохранение workflow

```python
success = builder.save_workflow("pipeline.json")
```

**Параметры:**
- `filepath` - путь к файлу для сохранения

**Возвращает:** True если сохранение успешно

#### Загрузка workflow

```python
success = builder.load_workflow("pipeline.json")
```

**Параметры:**
- `filepath` - путь к файлу workflow

**Возвращает:** True если загрузка успешна

#### Загрузка в ComfyUI

```python
result = builder.upload_to_comfyui("My Pipeline")
```

**Параметры:**
- `workflow_name` - название workflow (опционально)

**Возвращает:** Результат загрузки

#### Выполнение workflow

```python
result = builder.execute_workflow(
    workflow_name="My Pipeline",
    wait_for_completion=True,
    timeout=300
)
```

**Параметры:**
- `workflow_name` - название workflow
- `wait_for_completion` - ожидать завершения
- `timeout` - таймаут ожидания в секундах

**Возвращает:** Результат выполнения

#### Валидация workflow

```python
validation = builder.validate_workflow()
```

**Возвращает:** Результат валидации

#### Получение информации

```python
builder.print_workflow_info()
```

Выводит подробную информацию о workflow в консоль.

### PipelineTemplates

#### OpenAI -> S3 пайплайн

```python
builder = PipelineTemplates.openai_to_s3_pipeline(
    prompt="Your prompt here",
    bucket_name="your-bucket",
    aws_access_key_id="your-key",
    aws_secret_access_key="your-secret"
)
```

#### S3 -> Preview пайплайн

```python
builder = PipelineTemplates.s3_to_preview_pipeline(
    s3_key="comfyui/images/image.png",
    bucket_name="your-bucket",
    aws_access_key_id="your-key",
    aws_secret_access_key="your-secret"
)
```

#### Workflow Save пайплайн

```python
builder = PipelineTemplates.workflow_save_pipeline(
    workflow_data={"name": "My Workflow"},
    bucket_name="your-bucket",
    workflow_name="workflow.json",
    aws_access_key_id="your-key",
    aws_secret_access_key="your-secret"
)
```

### PipelineManager

#### Инициализация

```python
manager = PipelineManager("http://localhost:8188")
```

#### Создание пайплайнов

```python
# OpenAI пайплайн
builder = manager.create_openai_pipeline(
    prompt="Your prompt",
    model="dall-e-3",
    size="1024x1024"
)

# S3 upload пайплайн
builder = manager.create_s3_upload_pipeline(
    bucket_name="your-bucket",
    aws_access_key_id="your-key",
    aws_secret_access_key="your-secret"
)

# S3 download пайплайн
builder = manager.create_s3_download_pipeline(
    s3_key="comfyui/images/image.png",
    bucket_name="your-bucket",
    aws_access_key_id="your-key",
    aws_secret_access_key="your-secret"
)

# Сложный пайплайн
builder = manager.create_complex_pipeline(
    prompt="Your prompt",
    bucket_name="your-bucket",
    aws_access_key_id="your-key",
    aws_secret_access_key="your-secret"
)
```

#### Управление пайплайнами

```python
# Загрузка из файла
builder = manager.load_pipeline_from_file("pipeline.json")

# Сохранение в файл
manager.save_pipeline_to_file(builder, "pipeline.json")

# Загрузка в ComfyUI
result = manager.upload_pipeline(builder, "My Pipeline")

# Выполнение
result = manager.execute_pipeline(builder, "My Pipeline")

# Валидация
validation = manager.validate_pipeline(builder)

# Список узлов
nodes = manager.list_available_nodes()
```

## 🔄 Примеры использования

### 1. Простой пайплайн генерации

```python
from comfyui_pipeline_builder import ComfyUIPipelineBuilder

def create_simple_generation_pipeline(prompt: str):
    builder = ComfyUIPipelineBuilder()
    
    # Узел генерации
    generator = builder.add_node(
        node_type="OpenAIImageGenerator",
        inputs={
            "prompt": prompt,
            "model": "dall-e-3",
            "size": "1024x1024"
        },
        title="Image Generator"
    )
    
    # Узел предварительного просмотра
    preview = builder.add_node(
        node_type="PreviewImage",
        inputs={},
        title="Preview"
    )
    
    # Соединение
    builder.connect_nodes(generator, 0, preview, 0)
    
    return builder

# Использование
pipeline = create_simple_generation_pipeline("A beautiful landscape")
pipeline.save_workflow("landscape_pipeline.json")
```

### 2. Пайплайн с S3 интеграцией

```python
def create_s3_pipeline(prompt: str, bucket: str):
    builder = ComfyUIPipelineBuilder()
    
    # Генерация
    generator = builder.add_node(
        node_type="OpenAIImageGenerator",
        inputs={"prompt": prompt, "model": "dall-e-3"},
        title="Generator"
    )
    
    # Загрузка в S3
    uploader = builder.add_node(
        node_type="S3ImageUploader",
        inputs={
            "bucket_name": bucket,
            "metadata": '{"prompt": "' + prompt + '"}'
        },
        title="S3 Uploader"
    )
    
    # Предварительный просмотр
    preview = builder.add_node(
        node_type="PreviewImage",
        inputs={},
        title="Preview"
    )
    
    # Соединения
    builder.connect_nodes(generator, 0, uploader, 0)
    builder.connect_nodes(generator, 0, preview, 0)
    
    return builder

# Использование
pipeline = create_s3_pipeline("A futuristic city", "my-bucket")
pipeline.upload_to_comfyui("S3 Pipeline")
```

### 3. Пакетная обработка

```python
def create_batch_processing_pipeline(bucket: str):
    builder = ComfyUIPipelineBuilder()
    
    # Список изображений
    lister = builder.add_node(
        node_type="S3ImageLister",
        inputs={
            "bucket_name": bucket,
            "prefix": "comfyui/images/",
            "max_keys": 50
        },
        title="Image Lister"
    )
    
    # Скачивание изображения
    downloader = builder.add_node(
        node_type="S3ImageDownloader",
        inputs={
            "bucket_name": bucket,
            "s3_key": "comfyui/images/sample.png"
        },
        title="Image Downloader"
    )
    
    # Предварительный просмотр
    preview = builder.add_node(
        node_type="PreviewImage",
        inputs={},
        title="Preview"
    )
    
    # Соединение
    builder.connect_nodes(downloader, 0, preview, 0)
    
    return builder
```

### 4. Автоматизация с Pipeline Manager

```python
from pipeline_manager import PipelineManager

def automate_workflow_creation():
    manager = PipelineManager()
    
    # Создание пайплайна
    pipeline = manager.create_complex_pipeline(
        prompt="A magical forest",
        bucket_name="comfyui-images",
        aws_access_key_id="your-key",
        aws_secret_access_key="your-secret"
    )
    
    # Валидация
    validation = manager.validate_pipeline(pipeline)
    if not validation["valid"]:
        print(f"Ошибки валидации: {validation['errors']}")
        return
    
    # Загрузка в ComfyUI
    upload_result = manager.upload_pipeline(pipeline, "Magical Forest")
    if upload_result["success"]:
        print("Пайплайн загружен успешно")
        
        # Выполнение
        execution_result = manager.execute_pipeline(pipeline, "Magical Forest")
        print(f"Результат выполнения: {execution_result}")
    else:
        print(f"Ошибка загрузки: {upload_result['error']}")

# Запуск автоматизации
automate_workflow_creation()
```

## 🛠️ Командная строка

### Использование Pipeline Manager CLI

```bash
# Создание OpenAI пайплайна
python pipeline_manager.py create-openai \
    --prompt "A beautiful sunset" \
    --model dall-e-3 \
    --size 1024x1024 \
    --output sunset_pipeline.json \
    --upload \
    --execute

# Создание S3 пайплайна
python pipeline_manager.py create-s3 \
    --type upload \
    --bucket comfyui-images \
    --aws-key YOUR_KEY \
    --aws-secret YOUR_SECRET \
    --output s3_pipeline.json \
    --upload

# Создание сложного пайплайна
python pipeline_manager.py create-complex \
    --prompt "A futuristic city" \
    --bucket comfyui-images \
    --aws-key YOUR_KEY \
    --aws-secret YOUR_SECRET \
    --output complex_pipeline.json \
    --upload \
    --execute

# Загрузка пайплайна из файла
python pipeline_manager.py load \
    --file my_pipeline.json \
    --validate \
    --upload \
    --execute

# Получение списка узлов
python pipeline_manager.py nodes
```

### Параметры командной строки

#### Общие параметры:
- `--url` - URL ComfyUI сервера (по умолчанию: http://localhost:8188)

#### create-openai:
- `--prompt` - Промпт для генерации (обязательно)
- `--model` - Модель OpenAI (по умолчанию: dall-e-3)
- `--size` - Размер изображения (по умолчанию: 1024x1024)
- `--output` - Файл для сохранения пайплайна
- `--upload` - Загрузить в ComfyUI
- `--execute` - Выполнить пайплайн

#### create-s3:
- `--type` - Тип S3 пайплайна (upload/download)
- `--bucket` - Название S3 bucket (обязательно)
- `--s3-key` - Ключ файла в S3 (для download)
- `--aws-key` - AWS Access Key ID
- `--aws-secret` - AWS Secret Access Key
- `--region` - AWS регион (по умолчанию: us-east-1)
- `--output` - Файл для сохранения пайплайна
- `--upload` - Загрузить в ComfyUI

#### create-complex:
- `--prompt` - Промпт для генерации (обязательно)
- `--bucket` - Название S3 bucket (обязательно)
- `--aws-key` - AWS Access Key ID
- `--aws-secret` - AWS Secret Access Key
- `--region` - AWS регион (по умолчанию: us-east-1)
- `--output` - Файл для сохранения пайплайна
- `--upload` - Загрузить в ComfyUI
- `--execute` - Выполнить пайплайн

#### load:
- `--file` - Файл пайплайна (обязательно)
- `--validate` - Валидировать пайплайн
- `--upload` - Загрузить в ComfyUI
- `--execute` - Выполнить пайплайн

## 🔧 Интеграция с внешними системами

### 1. Интеграция с веб-приложением

```python
from flask import Flask, request, jsonify
from comfyui_pipeline_builder import ComfyUIPipelineBuilder

app = Flask(__name__)

@app.route('/create-pipeline', methods=['POST'])
def create_pipeline():
    data = request.json
    
    # Создание пайплайна
    builder = ComfyUIPipelineBuilder()
    
    # Добавление узлов на основе данных запроса
    generator = builder.add_node(
        node_type="OpenAIImageGenerator",
        inputs={
            "prompt": data["prompt"],
            "model": data.get("model", "dall-e-3"),
            "size": data.get("size", "1024x1024")
        }
    )
    
    preview = builder.add_node(
        node_type="PreviewImage",
        inputs={}
    )
    
    builder.connect_nodes(generator, 0, preview, 0)
    
    # Загрузка в ComfyUI
    result = builder.upload_to_comfyui(data.get("name", "Generated Pipeline"))
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
```

### 2. Интеграция с планировщиком задач

```python
import schedule
import time
from pipeline_manager import PipelineManager

def scheduled_pipeline_creation():
    manager = PipelineManager()
    
    # Создание пайплайна
    pipeline = manager.create_openai_pipeline(
        prompt="Daily inspiration image",
        model="dall-e-3"
    )
    
    # Выполнение
    result = manager.execute_pipeline(pipeline, "Daily Pipeline")
    print(f"Ежедневный пайплайн выполнен: {result}")

# Планирование выполнения каждый день в 9:00
schedule.every().day.at("09:00").do(scheduled_pipeline_creation)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### 3. Интеграция с базой данных

```python
import sqlite3
from comfyui_pipeline_builder import ComfyUIPipelineBuilder

class PipelineDatabase:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pipelines (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                workflow_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_pipeline(self, name: str, description: str, builder: ComfyUIPipelineBuilder):
        workflow_data = json.dumps(builder.build_workflow())
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO pipelines (name, description, workflow_data)
            VALUES (?, ?, ?)
        ''', (name, description, workflow_data))
        
        conn.commit()
        conn.close()
    
    def load_pipeline(self, pipeline_id: int) -> ComfyUIPipelineBuilder:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT workflow_data FROM pipelines WHERE id = ?', (pipeline_id,))
        result = cursor.fetchone()
        
        conn.close()
        
        if result:
            builder = ComfyUIPipelineBuilder()
            workflow_data = json.loads(result[0])
            
            # Восстановление пайплайна из данных
            for node_data in workflow_data["nodes"]:
                builder.add_node(
                    node_type=node_data["type"],
                    inputs=node_data["inputs"],
                    position=tuple(node_data["pos"]),
                    size=(node_data["size"]["0"], node_data["size"]["1"])
                )
            
            return builder
        
        return None

# Использование
db = PipelineDatabase("pipelines.db")

# Сохранение пайплайна
builder = ComfyUIPipelineBuilder()
# ... создание пайплайна ...
db.save_pipeline("My Pipeline", "Description", builder)

# Загрузка пайплайна
loaded_builder = db.load_pipeline(1)
if loaded_builder:
    loaded_builder.upload_to_comfyui("Loaded Pipeline")
```

## 🚨 Устранение неполадок

### Проблема: "Connection refused"

```python
# Проверка доступности ComfyUI
import requests

try:
    response = requests.get("http://localhost:8188/system_stats", timeout=5)
    if response.status_code == 200:
        print("ComfyUI доступен")
    else:
        print("ComfyUI недоступен")
except requests.exceptions.RequestException:
    print("Не удается подключиться к ComfyUI")
```

### Проблема: "Node type not found"

```python
# Получение списка доступных узлов
builder = ComfyUIPipelineBuilder()
nodes = builder.get_available_nodes()

if nodes["success"]:
    available_nodes = nodes["nodes"]
    print("Доступные узлы:")
    for node_type in available_nodes:
        print(f"  - {node_type}")
else:
    print(f"Ошибка получения узлов: {nodes['error']}")
```

### Проблема: "Invalid workflow"

```python
# Валидация пайплайна
validation = builder.validate_workflow()

if not validation["valid"]:
    print("Ошибки валидации:")
    for error in validation["errors"]:
        print(f"  ❌ {error}")
    
    print("Предупреждения:")
    for warning in validation["warnings"]:
        print(f"  ⚠️ {warning}")
else:
    print("Пайплайн валиден")
```

### Проблема: "Execution failed"

```python
# Выполнение с подробным логированием
result = builder.execute_workflow(
    "My Pipeline",
    wait_for_completion=True,
    timeout=600  # Увеличенный таймаут
)

if not result["success"]:
    print(f"Ошибка выполнения: {result['error']}")
    print(f"Статус: {result.get('status', 'unknown')}")
else:
    print("Выполнение успешно")
    print(f"Результаты: {result.get('results', {})}")
```

## 🎯 Лучшие практики

### 1. Организация кода

```python
# Разделение на модули
class PipelineFactory:
    def __init__(self, comfyui_url: str):
        self.comfyui_url = comfyui_url
    
    def create_image_generation_pipeline(self, prompt: str, **kwargs):
        builder = ComfyUIPipelineBuilder(self.comfyui_url)
        # Логика создания пайплайна
        return builder
    
    def create_s3_pipeline(self, bucket: str, **kwargs):
        builder = ComfyUIPipelineBuilder(self.comfyui_url)
        # Логика создания S3 пайплайна
        return builder

# Использование
factory = PipelineFactory("http://localhost:8188")
pipeline = factory.create_image_generation_pipeline("A beautiful landscape")
```

### 2. Обработка ошибок

```python
def safe_pipeline_execution(builder, name: str):
    try:
        # Валидация
        validation = builder.validate_workflow()
        if not validation["valid"]:
            raise ValueError(f"Пайплайн невалиден: {validation['errors']}")
        
        # Загрузка
        upload_result = builder.upload_to_comfyui(name)
        if not upload_result["success"]:
            raise RuntimeError(f"Ошибка загрузки: {upload_result['error']}")
        
        # Выполнение
        execution_result = builder.execute_workflow(name, wait_for_completion=True)
        if not execution_result["success"]:
            raise RuntimeError(f"Ошибка выполнения: {execution_result['error']}")
        
        return execution_result
        
    except Exception as e:
        logger.error(f"Ошибка выполнения пайплайна: {e}")
        return {"success": False, "error": str(e)}
```

### 3. Кэширование пайплайнов

```python
import hashlib
import pickle
import os

class PipelineCache:
    def __init__(self, cache_dir: str = "cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def get_cache_key(self, pipeline_config: dict) -> str:
        """Генерация ключа кэша на основе конфигурации"""
        config_str = json.dumps(pipeline_config, sort_keys=True)
        return hashlib.md5(config_str.encode()).hexdigest()
    
    def get_cached_pipeline(self, pipeline_config: dict):
        """Получение пайплайна из кэша"""
        cache_key = self.get_cache_key(pipeline_config)
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.pkl")
        
        if os.path.exists(cache_file):
            with open(cache_file, 'rb') as f:
                return pickle.load(f)
        
        return None
    
    def cache_pipeline(self, pipeline_config: dict, builder: ComfyUIPipelineBuilder):
        """Сохранение пайплайна в кэш"""
        cache_key = self.get_cache_key(pipeline_config)
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.pkl")
        
        with open(cache_file, 'wb') as f:
            pickle.dump(builder, f)

# Использование
cache = PipelineCache()

pipeline_config = {
    "type": "openai",
    "prompt": "A beautiful landscape",
    "model": "dall-e-3"
}

# Попытка получить из кэша
cached_pipeline = cache.get_cached_pipeline(pipeline_config)

if cached_pipeline is None:
    # Создание нового пайплайна
    builder = ComfyUIPipelineBuilder()
    # ... создание пайплайна ...
    
    # Сохранение в кэш
    cache.cache_pipeline(pipeline_config, builder)
else:
    builder = cached_pipeline
```

### 4. Мониторинг и логирование

```python
import logging
from datetime import datetime

class PipelineMonitor:
    def __init__(self):
        self.logger = logging.getLogger("pipeline_monitor")
        self.logger.setLevel(logging.INFO)
        
        # Настройка файлового хендлера
        handler = logging.FileHandler("pipeline_executions.log")
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def log_pipeline_execution(self, pipeline_name: str, result: dict):
        """Логирование выполнения пайплайна"""
        if result["success"]:
            self.logger.info(f"Пайплайн {pipeline_name} выполнен успешно")
        else:
            self.logger.error(f"Пайплайн {pipeline_name} завершился с ошибкой: {result['error']}")
    
    def get_execution_stats(self):
        """Получение статистики выполнения"""
        # Логика анализа логов
        pass

# Использование
monitor = PipelineMonitor()

def execute_pipeline_with_monitoring(builder, name: str):
    start_time = datetime.now()
    
    result = builder.execute_workflow(name)
    
    execution_time = (datetime.now() - start_time).total_seconds()
    result["execution_time"] = execution_time
    
    monitor.log_pipeline_execution(name, result)
    
    return result
```

## Заключение

Pipeline Builder предоставляет мощные возможности для программного создания и управления пайплайнами ComfyUI. Используйте его для автоматизации процессов, интеграции с внешними системами и создания сложных workflows.

### ✅ Чек-лист внедрения:

- [ ] Установлены зависимости
- [ ] Настроено подключение к ComfyUI
- [ ] Созданы базовые пайплайны
- [ ] Настроена валидация
- [ ] Интегрирована обработка ошибок
- [ ] Настроено логирование
- [ ] Протестированы шаблоны
- [ ] Документированы процессы 