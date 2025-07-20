# Примеры базовых workflows для ComfyUI

## 1. Простая генерация изображения через OpenAI

### Описание
Базовый workflow для генерации изображения через OpenAI API с сохранением результата.

### Узлы
- **OpenAI Image Generator** - генерация изображения
- **Save Image** - сохранение результата
- **Preview Image** - предварительный просмотр

### JSON Workflow
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
        "prompt": "A beautiful sunset over mountains, digital art style",
        "api_key": "",
        "model": "dall-e-3",
        "size": "1024x1024",
        "quality": "standard",
        "style": "vivid",
        "save_to_output": true
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

### Использование
1. Загрузите workflow в ComfyUI
2. Настройте prompt в узле OpenAI Image Generator
3. Установите API ключ (или используйте переменную окружения)
4. Нажмите "Queue Prompt"

## 2. Генерация вариаций изображения

### Описание
Workflow для создания вариаций существующего изображения через OpenAI API.

### Узлы
- **Load Image** - загрузка исходного изображения
- **OpenAI Image Variation** - создание вариации
- **Save Image** - сохранение результата
- **Preview Image** - предварительный просмотр

### JSON Workflow
```json
{
  "last_node_id": 4,
  "last_link_id": 3,
  "nodes": [
    {
      "id": 1,
      "type": "LoadImage",
      "pos": [100, 200],
      "inputs": {
        "image": "example.png"
      }
    },
    {
      "id": 2,
      "type": "OpenAIImageVariation",
      "pos": [300, 200],
      "inputs": {
        "image": ["1", 0],
        "api_key": "",
        "size": "1024x1024",
        "save_to_output": true
      }
    },
    {
      "id": 3,
      "type": "SaveImage",
      "pos": [500, 200],
      "inputs": {
        "images": ["2", 0],
        "filename_prefix": "openai_variation"
      }
    },
    {
      "id": 4,
      "type": "PreviewImage",
      "pos": [500, 300],
      "inputs": {
        "images": ["2", 0]
      }
    }
  ],
  "links": [
    [1, 1, 0, 2, 0],
    [2, 2, 0, 3, 0],
    [3, 2, 0, 4, 0]
  ]
}
```

### Использование
1. Загрузите исходное изображение в узел Load Image
2. Настройте параметры вариации
3. Запустите генерацию

## 3. Генерация с постобработкой

### Описание
Workflow для генерации изображения с последующей обработкой (масштабирование, фильтры).

### Узлы
- **OpenAI Image Generator** - генерация изображения
- **Image Scale** - масштабирование
- **Save Image** - сохранение результата
- **Preview Image** - предварительный просмотр

### JSON Workflow
```json
{
  "last_node_id": 4,
  "last_link_id": 3,
  "nodes": [
    {
      "id": 1,
      "type": "OpenAIImageGenerator",
      "pos": [100, 200],
      "inputs": {
        "prompt": "A futuristic city with flying cars and neon lights",
        "model": "dall-e-3",
        "size": "1024x1024",
        "quality": "hd",
        "style": "vivid"
      }
    },
    {
      "id": 2,
      "type": "ImageScale",
      "pos": [300, 200],
      "inputs": {
        "image": ["1", 0],
        "width": 2048,
        "height": 2048,
        "crop": "disabled"
      }
    },
    {
      "id": 3,
      "type": "SaveImage",
      "pos": [500, 200],
      "inputs": {
        "images": ["2", 0],
        "filename_prefix": "openai_scaled"
      }
    },
    {
      "id": 4,
      "type": "PreviewImage",
      "pos": [500, 300],
      "inputs": {
        "images": ["2", 0]
      }
    }
  ],
  "links": [
    [1, 1, 0, 2, 0],
    [2, 2, 0, 3, 0],
    [3, 2, 0, 4, 0]
  ]
}
```

## 4. Пакетная генерация

### Описание
Workflow для генерации нескольких изображений с разными промптами.

### Узлы
- **Multiple Prompts** - несколько промптов
- **OpenAI Image Generator** - генерация для каждого промпта
- **Save Image** - сохранение всех результатов

### JSON Workflow
```json
{
  "last_node_id": 6,
  "last_link_id": 4,
  "nodes": [
    {
      "id": 1,
      "type": "OpenAIImageGenerator",
      "pos": [100, 100],
      "inputs": {
        "prompt": "A cat in a garden, digital art",
        "model": "dall-e-3",
        "size": "1024x1024"
      }
    },
    {
      "id": 2,
      "type": "OpenAIImageGenerator",
      "pos": [100, 300],
      "inputs": {
        "prompt": "A dog in a park, digital art",
        "model": "dall-e-3",
        "size": "1024x1024"
      }
    },
    {
      "id": 3,
      "type": "OpenAIImageGenerator",
      "pos": [100, 500],
      "inputs": {
        "prompt": "A bird in a tree, digital art",
        "model": "dall-e-3",
        "size": "1024x1024"
      }
    },
    {
      "id": 4,
      "type": "SaveImage",
      "pos": [300, 100],
      "inputs": {
        "images": ["1", 0],
        "filename_prefix": "cat_garden"
      }
    },
    {
      "id": 5,
      "type": "SaveImage",
      "pos": [300, 300],
      "inputs": {
        "images": ["2", 0],
        "filename_prefix": "dog_park"
      }
    },
    {
      "id": 6,
      "type": "SaveImage",
      "pos": [300, 500],
      "inputs": {
        "images": ["3", 0],
        "filename_prefix": "bird_tree"
      }
    }
  ],
  "links": [
    [1, 1, 0, 4, 0],
    [2, 2, 0, 5, 0],
    [3, 3, 0, 6, 0]
  ]
}
```

## 5. Комбинированная генерация

### Описание
Workflow, комбинирующий OpenAI генерацию с другими моделями (например, Stable Diffusion).

### Узлы
- **OpenAI Image Generator** - начальная генерация
- **Image to Latent** - конвертация в латентное пространство
- **KSampler** - дополнительная обработка
- **VAE Decode** - декодирование
- **Save Image** - сохранение

### JSON Workflow
```json
{
  "last_node_id": 6,
  "last_link_id": 5,
  "nodes": [
    {
      "id": 1,
      "type": "OpenAIImageGenerator",
      "pos": [100, 200],
      "inputs": {
        "prompt": "A beautiful landscape, oil painting style",
        "model": "dall-e-3",
        "size": "1024x1024"
      }
    },
    {
      "id": 2,
      "type": "ImageToLatent",
      "pos": [300, 200],
      "inputs": {
        "image": ["1", 0]
      }
    },
    {
      "id": 3,
      "type": "KSampler",
      "pos": [500, 200],
      "inputs": {
        "latent": ["2", 0],
        "steps": 20,
        "cfg": 7.0,
        "sampler_name": "euler",
        "scheduler": "normal"
      }
    },
    {
      "id": 4,
      "type": "VAEDecode",
      "pos": [700, 200],
      "inputs": {
        "latent": ["3", 0]
      }
    },
    {
      "id": 5,
      "type": "SaveImage",
      "pos": [900, 200],
      "inputs": {
        "images": ["4", 0],
        "filename_prefix": "combined_generation"
      }
    },
    {
      "id": 6,
      "type": "PreviewImage",
      "pos": [900, 300],
      "inputs": {
        "images": ["4", 0]
      }
    }
  ],
  "links": [
    [1, 1, 0, 2, 0],
    [2, 2, 0, 3, 0],
    [3, 3, 0, 4, 0],
    [4, 4, 0, 5, 0],
    [5, 4, 0, 6, 0]
  ]
}
```

## Полезные советы

### 1. Оптимизация промптов
- Используйте конкретные описания
- Добавляйте стилистические указания
- Экспериментируйте с разными подходами

### 2. Управление качеством
- DALL-E 3 HD качество для важных проектов
- Standard качество для быстрых экспериментов
- Разные стили (vivid/natural) для разных эффектов

### 3. Организация файлов
```bash
output/
├── landscapes/
├── portraits/
├── variations/
└── experiments/
```

### 4. Автоматизация
```bash
# Скрипт для автоматического запуска workflow
#!/bin/bash
curl -X POST http://localhost:8188/prompt \
  -H "Content-Type: application/json" \
  -d @workflow.json
```

## Расширенные возможности

### Условная генерация
```python
# Пример условной логики
if image_quality > 0.8:
    generate_variation()
else:
    generate_new()
```

### Пакетная обработка
```python
# Обработка множества промптов
prompts = [
    "A cat in a garden",
    "A dog in a park",
    "A bird in a tree"
]

for prompt in prompts:
    generate_image(prompt)
```

### Интеграция с API
```python
# Программное управление ComfyUI
import requests

def queue_workflow(workflow_json):
    response = requests.post(
        "http://localhost:8188/prompt",
        json=workflow_json
    )
    return response.json()
``` 