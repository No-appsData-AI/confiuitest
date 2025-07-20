# Интеграция S3 хранилища с ComfyUI

## Обзор

Это руководство описывает интеграцию AWS S3 хранилища с ComfyUI для чтения и сохранения изображений, workflows и метаданных.

## 🎯 Возможности

### Основные функции:
- **Загрузка изображений** в S3 с метаданными
- **Скачивание изображений** из S3 в ComfyUI
- **Получение списка** изображений из хранилища
- **Сохранение workflows** в S3
- **Загрузка workflows** из S3
- **Резервное копирование** данных
- **Мониторинг** использования хранилища

### Преимущества:
- ✅ **Масштабируемость** - неограниченное хранилище
- ✅ **Надежность** - 99.99% доступность AWS S3
- ✅ **Безопасность** - шифрование и IAM роли
- ✅ **Стоимость** - платите только за использование
- ✅ **Интеграция** - прямо в ComfyUI workflows

## 🚀 Быстрый старт

### 1. Подготовка AWS

#### Создание S3 bucket:
```bash
# Через AWS CLI
aws s3 mb s3://comfyui-images --region us-east-1

# Или через AWS Console
# 1. Откройте S3 Console
# 2. Нажмите "Create bucket"
# 3. Введите название: comfyui-images
# 4. Выберите регион: us-east-1
# 5. Настройте права доступа
```

#### Создание IAM пользователя:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::comfyui-images",
        "arn:aws:s3:::comfyui-images/*"
      ]
    }
  ]
}
```

### 2. Установка на сервере

```bash
# Запуск скрипта установки
./scripts/install_s3_nodes_server.sh
```

### 3. Настройка переменных окружения

```bash
# На сервере
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"

# Постоянная установка
echo 'export AWS_ACCESS_KEY_ID="your-access-key"' >> ~/.bashrc
echo 'export AWS_SECRET_ACCESS_KEY="your-secret-key"' >> ~/.bashrc
source ~/.bashrc
```

### 4. Проверка установки

1. Откройте ComfyUI: http://your-server-ip:8188
2. Найдите категорию "S3 Storage" в списке узлов
3. Добавьте узел "S3 Storage Info"
4. Запустите для проверки подключения

## 📋 Узлы S3 Storage

### S3 Image Uploader

**Назначение**: Загружает изображения в S3 хранилище

**Входы**:
- `image` - Изображение для загрузки
- `bucket_name` - Название S3 bucket
- `aws_access_key_id` - AWS Access Key ID
- `aws_secret_access_key` - AWS Secret Access Key
- `region_name` - AWS регион
- `s3_key` - Ключ в S3 (опционально)
- `metadata` - Дополнительные метаданные (JSON)
- `prompt` - Промпт для генерации (опционально)
- `model` - Модель генерации (опционально)
- `workflow_name` - Название workflow (опционально)

**Выходы**:
- `s3_key` - Ключ загруженного файла в S3
- `s3_url` - URL для доступа к файлу
- `status` - Статус операции

**Пример использования**:
```json
{
  "type": "S3ImageUploader",
  "inputs": {
    "image": ["OpenAIImageGenerator", 0],
    "bucket_name": "comfyui-images",
    "aws_access_key_id": "AKIA...",
    "aws_secret_access_key": "secret...",
    "region_name": "us-east-1",
    "metadata": "{\"prompt\": \"A beautiful sunset\", \"model\": \"dall-e-3\"}"
  }
}
```

### S3 Image Downloader

**Назначение**: Скачивает изображения из S3 хранилища

**Входы**:
- `s3_key` - Ключ файла в S3
- `bucket_name` - Название S3 bucket
- `aws_access_key_id` - AWS Access Key ID
- `aws_secret_access_key` - AWS Secret Access Key
- `region_name` - AWS регион

**Выходы**:
- `image` - Скачанное изображение
- `local_path` - Локальный путь к файлу
- `status` - Статус операции

**Пример использования**:
```json
{
  "type": "S3ImageDownloader",
  "inputs": {
    "s3_key": "comfyui/images/20241201_120000_image.png",
    "bucket_name": "comfyui-images",
    "aws_access_key_id": "AKIA...",
    "aws_secret_access_key": "secret...",
    "region_name": "us-east-1"
  }
}
```

### S3 Image Lister

**Назначение**: Получает список изображений из S3

**Входы**:
- `bucket_name` - Название S3 bucket
- `aws_access_key_id` - AWS Access Key ID
- `aws_secret_access_key` - AWS Secret Access Key
- `region_name` - AWS регион
- `prefix` - Префикс для поиска
- `max_keys` - Максимальное количество ключей

**Выходы**:
- `images_list` - JSON список изображений
- `status` - Статус операции

**Пример вывода**:
```json
[
  {
    "key": "comfyui/images/20241201_120000_image.png",
    "size_mb": 2.5,
    "last_modified": "2024-12-01T12:00:00Z",
    "url": "https://..."
  }
]
```

### S3 Workflow Saver

**Назначение**: Сохраняет workflow в S3

**Входы**:
- `workflow_data` - JSON данные workflow
- `bucket_name` - Название S3 bucket
- `aws_access_key_id` - AWS Access Key ID
- `aws_secret_access_key` - AWS Secret Access Key
- `region_name` - AWS регион
- `workflow_name` - Название workflow

**Выходы**:
- `s3_key` - Ключ сохраненного workflow
- `status` - Статус операции

### S3 Workflow Loader

**Назначение**: Загружает workflow из S3

**Входы**:
- `workflow_name` - Название workflow
- `bucket_name` - Название S3 bucket
- `aws_access_key_id` - AWS Access Key ID
- `aws_secret_access_key` - AWS Secret Access Key
- `region_name` - AWS регион

**Выходы**:
- `workflow_data` - JSON данные workflow
- `status` - Статус операции

### S3 Storage Info

**Назначение**: Получает информацию о S3 хранилище

**Входы**:
- `bucket_name` - Название S3 bucket
- `aws_access_key_id` - AWS Access Key ID
- `aws_secret_access_key` - AWS Secret Access Key
- `region_name` - AWS регион

**Выходы**:
- `storage_info` - JSON информация о хранилище
- `status` - Статус операции

**Пример вывода**:
```json
{
  "bucket_name": "comfyui-images",
  "region": "us-east-1",
  "total_files": 150,
  "total_size_bytes": 524288000,
  "total_size_mb": 500.0,
  "categories": {
    "images": {"count": 100, "files": [...]},
    "workflows": {"count": 30, "files": [...]},
    "backups": {"count": 20, "files": [...]}
  }
}
```

## 🏗️ Структура S3 хранилища

```
comfyui-images/
├── comfyui/
│   ├── images/          # Изображения
│   │   ├── 20241201_120000_image1.png
│   │   ├── 20241201_120100_image2.png
│   │   └── ...
│   ├── workflows/       # Workflows
│   │   ├── landscape_workflow.json
│   │   ├── portrait_workflow.json
│   │   └── ...
│   ├── metadata/        # Метаданные
│   │   ├── image_metadata.json
│   │   └── ...
│   ├── temp/           # Временные файлы
│   │   └── ...
│   └── backups/        # Резервные копии
│       ├── backup_20241201.json
│       └── ...
```

## 🔄 Примеры workflows

### 1. Генерация и загрузка в S3

```json
{
  "nodes": [
    {
      "id": 1,
      "type": "OpenAIImageGenerator",
      "inputs": {
        "prompt": "A beautiful sunset over mountains",
        "model": "dall-e-3",
        "size": "1024x1024"
      }
    },
    {
      "id": 2,
      "type": "S3ImageUploader",
      "inputs": {
        "image": ["1", 0],
        "bucket_name": "comfyui-images",
        "metadata": "{\"prompt\": \"A beautiful sunset over mountains\"}"
      }
    }
  ],
  "links": [[1, 1, 0, 2, 0]]
}
```

### 2. Скачивание и обработка

```json
{
  "nodes": [
    {
      "id": 1,
      "type": "S3ImageDownloader",
      "inputs": {
        "s3_key": "comfyui/images/20241201_120000_image.png",
        "bucket_name": "comfyui-images"
      }
    },
    {
      "id": 2,
      "type": "PreviewImage",
      "inputs": {
        "images": ["1", 0]
      }
    }
  ],
  "links": [[1, 1, 0, 2, 0]]
}
```

### 3. Сохранение workflow

```json
{
  "nodes": [
    {
      "id": 1,
      "type": "S3WorkflowSaver",
      "inputs": {
        "workflow_data": "{\"name\": \"My Workflow\", \"nodes\": [...]}",
        "bucket_name": "comfyui-images",
        "workflow_name": "my_workflow.json"
      }
    }
  ]
}
```

## 🔒 Безопасность

### Рекомендации:

1. **IAM роли с минимальными правами**:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "s3:GetObject",
           "s3:PutObject",
           "s3:DeleteObject",
           "s3:ListBucket"
         ],
         "Resource": [
           "arn:aws:s3:::comfyui-images",
           "arn:aws:s3:::comfyui-images/*"
         ]
       }
     ]
   }
   ```

2. **Шифрование данных**:
   ```bash
   # Включение шифрования на bucket
   aws s3api put-bucket-encryption \
     --bucket comfyui-images \
     --server-side-encryption-configuration '{
       "Rules": [
         {
           "ApplyServerSideEncryptionByDefault": {
             "SSEAlgorithm": "AES256"
           }
         }
       ]
     }'
   ```

3. **CORS настройки**:
   ```json
   {
     "CORSRules": [
       {
         "AllowedHeaders": ["*"],
         "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
         "AllowedOrigins": ["http://your-comfyui-domain:8188"],
         "ExposeHeaders": ["ETag"]
       }
     ]
   }
   ```

4. **Переменные окружения**:
   ```bash
   # Никогда не коммитьте ключи в код
   export AWS_ACCESS_KEY_ID="your-key"
   export AWS_SECRET_ACCESS_KEY="your-secret"
   ```

## 💰 Стоимость

### Примеры затрат:

- **Хранение**: $0.023 за GB в месяц
- **Запросы GET**: $0.0004 за 1000 запросов
- **Запросы PUT**: $0.0005 за 1000 запросов
- **Передача данных**: $0.09 за GB (выход)

### Расчет для типичного использования:

- 1000 изображений по 2MB = 2GB
- 1000 запросов в день
- **Месячная стоимость**: ~$0.05

## 🚨 Устранение неполадок

### Проблема: "Access Denied"

```bash
# Проверка прав доступа
aws s3 ls s3://comfyui-images

# Проверка IAM политики
aws iam get-user-policy --user-name comfyui-user --policy-name S3Access
```

### Проблема: "Bucket not found"

```bash
# Создание bucket
aws s3 mb s3://comfyui-images --region us-east-1

# Проверка существования
aws s3 ls | grep comfyui-images
```

### Проблема: "Invalid credentials"

```bash
# Проверка переменных окружения
echo $AWS_ACCESS_KEY_ID
echo $AWS_SECRET_ACCESS_KEY

# Тест подключения
aws sts get-caller-identity
```

### Проблема: "Connection timeout"

```bash
# Проверка сетевого подключения
ping s3.amazonaws.com

# Проверка DNS
nslookup s3.amazonaws.com

# Проверка файрвола
sudo ufw status
```

## 📊 Мониторинг

### CloudWatch метрики:

```bash
# Получение метрик bucket
aws cloudwatch get-metric-statistics \
  --namespace AWS/S3 \
  --metric-name NumberOfObjects \
  --dimensions Name=BucketName,Value=comfyui-images \
  --start-time 2024-12-01T00:00:00Z \
  --end-time 2024-12-02T00:00:00Z \
  --period 3600 \
  --statistics Average
```

### Скрипт мониторинга:

```python
#!/usr/bin/env python3
import boto3
from datetime import datetime

def monitor_s3_usage():
    s3 = boto3.client('s3')
    cloudwatch = boto3.client('cloudwatch')
    
    # Получение статистики
    response = s3.list_objects_v2(Bucket='comfyui-images')
    
    total_size = sum(obj['Size'] for obj in response.get('Contents', []))
    total_objects = len(response.get('Contents', []))
    
    print(f"Объектов: {total_objects}")
    print(f"Размер: {total_size / (1024*1024):.2f} MB")
    
    # Отправка метрик в CloudWatch
    cloudwatch.put_metric_data(
        Namespace='ComfyUI/S3',
        MetricData=[
            {
                'MetricName': 'ObjectCount',
                'Value': total_objects,
                'Unit': 'Count'
            },
            {
                'MetricName': 'StorageSize',
                'Value': total_size,
                'Unit': 'Bytes'
            }
        ]
    )

if __name__ == "__main__":
    monitor_s3_usage()
```

## 🔄 Автоматизация

### Cron job для резервного копирования:

```bash
# Добавление в crontab
crontab -e

# Резервное копирование каждый день в 2:00
0 2 * * * /path/to/backup_script.sh
```

### Скрипт резервного копирования:

```bash
#!/bin/bash
# backup_script.sh

BUCKET="comfyui-images"
BACKUP_BUCKET="comfyui-backups"
DATE=$(date +%Y%m%d)

# Создание резервной копии
aws s3 sync s3://$BUCKET s3://$BACKUP_BUCKET/backup-$DATE

# Удаление старых резервных копий (старше 30 дней)
aws s3 ls s3://$BACKUP_BUCKET/ | grep backup- | awk '{print $2}' | \
while read backup; do
    backup_date=$(echo $backup | sed 's/backup-//')
    if [ $(date -d "$backup_date" +%s) -lt $(date -d "30 days ago" +%s) ]; then
        aws s3 rm s3://$BACKUP_BUCKET/$backup --recursive
    fi
done
```

## 🎯 Лучшие практики

### 1. Организация файлов:
- Используйте префиксы для категоризации
- Добавляйте временные метки к именам файлов
- Сохраняйте метаданные вместе с файлами

### 2. Оптимизация производительности:
- Используйте CloudFront для кэширования
- Группируйте запросы в батчи
- Используйте multipart upload для больших файлов

### 3. Безопасность:
- Регулярно ротируйте ключи доступа
- Используйте VPC endpoints для приватного доступа
- Настройте bucket policies

### 4. Мониторинг:
- Настройте CloudWatch алерты
- Логируйте все операции
- Отслеживайте стоимость

## Заключение

Интеграция S3 с ComfyUI предоставляет мощное решение для масштабируемого хранения изображений и workflows. Следуйте рекомендациям по безопасности и мониторингу для оптимального использования.

### ✅ Чек-лист внедрения:

- [ ] Создан S3 bucket
- [ ] Настроены IAM права
- [ ] Установлены S3 узлы
- [ ] Настроены переменные окружения
- [ ] Протестирована загрузка/скачивание
- [ ] Настроен мониторинг
- [ ] Созданы резервные копии
- [ ] Документированы процессы 