# Использование ComfyUI через веб-интерфейс

## Обзор

ComfyUI предоставляет мощный веб-интерфейс для создания сложных пайплайнов генерации изображений. Это руководство покажет, как эффективно использовать интерфейс и добавлять кастомные скрипты.

## Доступ к веб-интерфейсу

### Подключение к серверу

```bash
# Локальный доступ
http://localhost:8188

# Удаленный доступ
http://your-server-ip:8188

# Через домен (если настроен)
http://your-domain.com
```

### Проверка доступности

```bash
# Проверка статуса сервиса
curl -I http://your-server-ip:8188

# Проверка через браузер
# Откройте http://your-server-ip:8188 в браузере
```

## Основные элементы интерфейса

### 1. Панель инструментов

```
┌─────────────────────────────────────────────────────────────┐
│ [Queue Prompt] [Interrupt] [Clear] [Load] [Save] [Settings] │
└─────────────────────────────────────────────────────────────┘
```

- **Queue Prompt** - Запуск генерации
- **Interrupt** - Прерывание процесса
- **Clear** - Очистка рабочей области
- **Load** - Загрузка workflow
- **Save** - Сохранение workflow
- **Settings** - Настройки

### 2. Боковая панель узлов

```
┌─────────────────┐
│ 📁 Load         │
│ 📁 Save         │
│ 📁 Models       │
│ ─────────────── │
│ 🎨 Load Image   │
│ 🖼️ Save Image   │
│ ─────────────── │
│ 🤖 OpenAI       │ ← Наши кастомные узлы
│ ─────────────── │
│ 🔧 Utils        │
│ 📊 Sampling     │
│ 🎭 Conditioning │
└─────────────────┘
```

### 3. Рабочая область

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  [Node 1] ────→ [Node 2] ────→ [Node 3]                    │
│     │              │              │                         │
│     └──────────────┴──────────────┘                         │
│                                                             │
│  [Node 4] ←─────────────────────── [Node 5]                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Создание простого workflow

### Шаг 1: Добавление узлов

1. **Откройте ComfyUI** в браузере
2. **Найдите нужный узел** в боковой панели
3. **Перетащите узел** на рабочую область
4. **Повторите** для всех необходимых узлов

### Шаг 2: Настройка параметров

```javascript
// Пример настройки OpenAI узла
{
  "prompt": "A beautiful sunset over mountains, digital art style",
  "model": "dall-e-3",
  "size": "1024x1024",
  "quality": "standard",
  "style": "vivid",
  "save_to_output": true
}
```

### Шаг 3: Соединение узлов

1. **Найдите выходные порты** узла (обычно справа)
2. **Найдите входные порты** следующего узла (обычно слева)
3. **Перетащите** от выхода к входу для создания соединения
4. **Повторите** для всех узлов в цепочке

### Шаг 4: Запуск генерации

1. **Проверьте все соединения**
2. **Нажмите "Queue Prompt"**
3. **Дождитесь завершения** генерации
4. **Просмотрите результат** в панели предварительного просмотра

## Работа с кастомными узлами OpenAI

### Добавление OpenAI узлов

#### 1. Поиск узлов

```
В боковой панели найдите категорию "OpenAI":
├── 🤖 OpenAI
│   ├── OpenAI Image Generator
│   └── OpenAI Image Variation
```

#### 2. Настройка OpenAI Image Generator

```javascript
// Параметры узла
{
  "prompt": "A futuristic city with flying cars and neon lights",
  "api_key": "", // Оставьте пустым для использования переменной окружения
  "model": "dall-e-3",
  "size": "1024x1024",
  "quality": "hd",
  "style": "vivid",
  "save_to_output": true
}
```

#### 3. Настройка OpenAI Image Variation

```javascript
// Параметры узла
{
  "image": "IMAGE", // Подключите изображение
  "api_key": "",
  "size": "1024x1024",
  "save_to_output": true
}
```

### Пример workflow с OpenAI

#### Простая генерация

```
[OpenAI Image Generator] ────→ [Save Image]
     │
     └───→ [Preview Image]
```

#### Генерация с постобработкой

```
[OpenAI Image Generator] ────→ [Image Scale] ────→ [Save Image]
     │                           │
     └───→ [Preview Image]      └───→ [Preview Image]
```

#### Создание вариаций

```
[Load Image] ────→ [OpenAI Image Variation] ────→ [Save Image]
                      │
                      └───→ [Preview Image]
```

## Продвинутые техники

### 1. Условная генерация

```javascript
// Использование условных узлов
{
  "condition": "if image_quality > 0.8",
  "then": "generate_variation",
  "else": "generate_new"
}
```

### 2. Пакетная обработка

```javascript
// Настройка для пакетной обработки
{
  "batch_size": 4,
  "prompts": [
    "A cat in a garden",
    "A dog in a park",
    "A bird in a tree",
    "A fish in a pond"
  ]
}
```

### 3. Комбинирование с другими моделями

```
[OpenAI Generator] ────→ [Image to Latent] ────→ [Stable Diffusion] ────→ [Save]
```

## Сохранение и загрузка workflows

### Сохранение workflow

1. **Нажмите "Save"** в панели инструментов
2. **Введите имя файла** (например: `my_openai_workflow.json`)
3. **Выберите директорию** для сохранения
4. **Нажмите "Save"**

### Загрузка workflow

1. **Нажмите "Load"** в панели инструментов
2. **Выберите файл** workflow
3. **Нажмите "Open"**
4. **Проверьте соединения** узлов

### Пример файла workflow

```json
{
  "last_node_id": 3,
  "last_link_id": 2,
  "nodes": [
    {
      "id": 1,
      "type": "OpenAIImageGenerator",
      "pos": [100, 200],
      "size": {"0": 300, "1": 400},
      "inputs": {
        "prompt": "A beautiful sunset over mountains",
        "model": "dall-e-3",
        "size": "1024x1024",
        "quality": "standard",
        "style": "vivid"
      }
    },
    {
      "id": 2,
      "type": "SaveImage",
      "pos": [500, 200],
      "inputs": {
        "images": ["1", 0],
        "filename_prefix": "openai_generated"
      }
    },
    {
      "id": 3,
      "type": "PreviewImage",
      "pos": [500, 300],
      "inputs": {
        "images": ["1", 0]
      }
    }
  ],
  "links": [
    [1, 1, 0, 2, 0],
    [2, 1, 0, 3, 0]
  ]
}
```

## Добавление кастомных скриптов

### 1. Подготовка файлов

```bash
# Структура кастомного узла
custom_nodes/
└── my_custom_node/
    ├── __init__.py
    ├── my_node.py
    ├── requirements.txt
    └── README.md
```

### 2. Создание узла

```python
# my_node.py
import torch
import numpy as np

class MyCustomNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "parameter": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 10.0})
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "process_image"
    CATEGORY = "My Custom Nodes"
    
    def process_image(self, image, parameter):
        # Ваша логика обработки
        processed_image = image * parameter
        return (processed_image,)

# Регистрация узла
NODE_CLASS_MAPPINGS = {
    "MyCustomNode": MyCustomNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MyCustomNode": "My Custom Node"
}
```

### 3. Установка узла

```bash
# Копирование файлов
cp -r my_custom_node /path/to/ComfyUI/custom_nodes/

# Установка зависимостей
cd /path/to/ComfyUI/custom_nodes/my_custom_node
pip install -r requirements.txt

# Перезапуск ComfyUI
sudo systemctl restart comfyui.service
```

### 4. Проверка установки

1. **Откройте ComfyUI**
2. **Найдите категорию** "My Custom Nodes"
3. **Проверьте наличие** вашего узла
4. **Протестируйте** функциональность

## Оптимизация производительности

### 1. Настройки браузера

```javascript
// Отключение ненужных расширений
// Очистка кэша
// Использование аппаратного ускорения
```

### 2. Настройки ComfyUI

```bash
# Оптимизация для CPU
export OMP_NUM_THREADS=4
export MKL_NUM_THREADS=4

# Оптимизация для GPU
export CUDA_VISIBLE_DEVICES=0
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:128
```

### 3. Мониторинг ресурсов

```bash
# Мониторинг CPU и RAM
htop

# Мониторинг GPU
nvidia-smi

# Мониторинг диска
df -h
```

## Устранение неполадок

### Проблема: Узлы не загружаются

```bash
# Проверка логов
sudo journalctl -u comfyui.service -f

# Проверка прав доступа
ls -la /path/to/ComfyUI/custom_nodes/

# Проверка синтаксиса Python
python3 -m py_compile /path/to/custom_node.py
```

### Проблема: Ошибки в браузере

```javascript
// Откройте Developer Tools (F12)
// Проверьте Console на ошибки
// Проверьте Network на проблемы с запросами
```

### Проблема: Медленная работа

```bash
# Проверка ресурсов сервера
top
free -h
df -h

# Оптимизация настроек
# Уменьшение размера изображений
# Использование более легких моделей
```

## Полезные советы

### 1. Организация workflows

```
workflows/
├── basic/
│   ├── simple_generation.json
│   └── image_variation.json
├── advanced/
│   ├── conditional_generation.json
│   └── batch_processing.json
└── experimental/
    ├── new_technique.json
    └── test_workflow.json
```

### 2. Документирование

```markdown
# My Workflow Documentation

## Описание
Этот workflow генерирует изображения через OpenAI API.

## Узлы
- OpenAI Image Generator: Основная генерация
- Save Image: Сохранение результата
- Preview Image: Предварительный просмотр

## Параметры
- prompt: Описание изображения
- model: dall-e-3
- size: 1024x1024

## Использование
1. Загрузите workflow
2. Настройте параметры
3. Нажмите "Queue Prompt"
```

### 3. Автоматизация

```bash
# Скрипт для автоматической загрузки workflow
#!/bin/bash
curl -X POST http://localhost:8188/prompt \
  -H "Content-Type: application/json" \
  -d @my_workflow.json
```

### 4. Резервное копирование

```bash
# Создание бэкапа workflows
tar -czf workflows_backup_$(date +%Y%m%d).tar.gz workflows/

# Создание бэкапа настроек
cp ~/.config/ComfyUI/settings.json settings_backup.json
```

## Заключение

ComfyUI предоставляет мощный и гибкий интерфейс для работы с генеративными моделями. Основные преимущества:

- ✅ Визуальный редактор пайплайнов
- ✅ Поддержка кастомных узлов
- ✅ Мощные возможности комбинирования
- ✅ Сохранение и загрузка workflows
- ✅ Веб-интерфейс доступен из любого браузера
- ✅ Поддержка различных моделей и API

Следуя этому руководству, вы сможете эффективно использовать ComfyUI для создания сложных пайплайнов генерации изображений с интеграцией OpenAI API. 