# confiuitest

## Описание

Этот проект содержит скрипты и плагины для подключения и управления ComfyUI на сервере. Он предоставляет инструменты и утилиты для упрощения настройки, конфигурации и обслуживания экземпляров ComfyUI в серверных средах.

## Возможности

- Скрипты подключения к серверу
- Утилиты управления ComfyUI
- Автоматизация конфигурации
- Система плагинов для расширенной функциональности

## Настройка ComfyUI на сервере

### Требования

- Ubuntu 24.04 LTS
- Python 3.12+
- SSH доступ к серверу
- Минимум 2GB RAM

### Установка

1. **Подключение к серверу:**
   ```bash
   ssh -i blackholetest.pem ubuntu@34.245.10.81
   ```

2. **Обновление системы:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

3. **Установка зависимостей:**
   ```bash
   sudo apt install -y python3-pip python3-venv git wget curl build-essential python3-dev
   ```

4. **Клонирование ComfyUI:**
   ```bash
   cd /home/ubuntu
   git clone https://github.com/comfyanonymous/ComfyUI.git
   ```

5. **Создание виртуального окружения:**
   ```bash
   cd ComfyUI
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   ```

6. **Установка PyTorch (CPU версия):**
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
   ```

7. **Установка зависимостей ComfyUI:**
   ```bash
   pip install -r requirements.txt
   ```

### Настройка автозапуска

1. **Создание systemd сервиса:**
   ```bash
   sudo cp comfyui.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable comfyui.service
   ```

2. **Запуск сервиса:**
   ```bash
   sudo systemctl start comfyui.service
   ```

## Управление ComfyUI

### Скрипт управления

Используйте скрипт `comfyui_manager.sh` для управления ComfyUI:

```bash
# Показать справку
./comfyui_manager.sh help

# Запустить сервис
./comfyui_manager.sh start

# Остановить сервис
./comfyui_manager.sh stop

# Перезапустить сервис
./comfyui_manager.sh restart

# Показать статус
./comfyui_manager.sh status

# Показать логи
./comfyui_manager.sh logs

# Показать URL доступа
./comfyui_manager.sh url

# Проверить доступность
./comfyui_manager.sh test
```

### Ручной запуск

Для ручного запуска используйте скрипт `start_comfyui.sh`:

```bash
./start_comfyui.sh
```

## Доступ к ComfyUI

После настройки ComfyUI будет доступен по адресу:
- **Внешний доступ:** http://34.245.10.81:8188
- **Локальный доступ:** http://localhost:8188

## Мониторинг

### Проверка статуса сервиса
```bash
sudo systemctl status comfyui.service
```

### Просмотр логов
```bash
sudo journalctl -u comfyui.service -f
```

### Проверка использования ресурсов
```bash
ps aux | grep python
free -h
df -h
```

## Устранение неполадок

### Сервис не запускается
1. Проверьте логи: `sudo journalctl -u comfyui.service -n 50`
2. Убедитесь, что виртуальное окружение активировано
3. Проверьте права доступа к файлам

### Проблемы с доступом
1. Проверьте настройки firewall
2. Убедитесь, что порт 8188 открыт
3. Проверьте статус сервиса

### Проблемы с производительностью
1. Используйте CPU-оптимизированные модели
2. Увеличьте RAM на сервере
3. Рассмотрите использование GPU-инстанса

## 📁 Структура проекта

```
confiuitest/
├── 📚 docs/                           # Подробная документация
│   ├── README.md                      # Главный файл документации
│   ├── 01_comfyui_server_setup.md     # Установка на сервере
│   ├── 02_openai_custom_scripts.md    # Кастомные скрипты
│   ├── 03_comfyui_web_interface.md    # Веб-интерфейс
│   └── examples/
│       └── basic_workflows.md         # Примеры workflows
├── 🔧 scripts/                        # Скрипты управления
│   ├── start_comfyui.sh               # Ручной запуск ComfyUI
│   ├── comfyui_manager.sh             # Управление ComfyUI
│   ├── health_check.sh                # Проверка состояния системы
│   └── install_openai_node_server.sh  # Установка OpenAI узла
├── ⚙️ config/                         # Конфигурационные файлы
│   └── comfyui.service                # Systemd сервис файл
├── 📋 workflows/                      # Примеры workflows
│   └── example_openai_workflow.json   # Пример workflow с OpenAI
├── 💡 examples/                       # Примеры кода
│   ├── openai_image_generator.py      # Основной класс OpenAI
│   ├── comfyui_openai_node.py         # Кастомные узлы ComfyUI
│   └── install_openai_node.py         # Локальная установка
├── 🔑 blackholetest.pem               # SSH ключ для сервера
├── 📖 README.md                       # Основная документация
└── 🚫 .gitignore                      # Исключения Git
```

### Файлы проекта

#### 🔧 Скрипты управления (`scripts/`)
- `start_comfyui.sh` - Скрипт для ручного запуска ComfyUI
- `comfyui_manager.sh` - Скрипт управления ComfyUI (старт/стоп/статус)
- `health_check.sh` - Скрипт комплексной проверки состояния системы
- `install_openai_node_server.sh` - Скрипт установки OpenAI узла на сервере
- `install_s3_nodes_server.sh` - Скрипт установки S3 узлов на сервере

#### ⚙️ Конфигурация (`config/`)
- `comfyui.service` - Systemd сервис файл для автозапуска ComfyUI

#### 📋 Workflows (`workflows/`)
- `example_openai_workflow.json` - Пример workflow для ComfyUI с OpenAI
- `s3_integration_workflow.json` - Пример workflow с интеграцией S3

#### 💡 Примеры кода (`examples/`)
- `openai_image_generator.py` - Основной скрипт для работы с OpenAI API
- `comfyui_openai_node.py` - Кастомный узел ComfyUI для OpenAI
- `install_openai_node.py` - Скрипт установки OpenAI узла локально
- `s3_storage_manager.py` - Менеджер S3 хранилища
- `comfyui_s3_nodes.py` - Узлы для работы с S3

#### 🔑 Безопасность
- `blackholetest.pem` - SSH ключ для подключения к серверу (защищен .gitignore)

## Быстрый старт

1. **Проверка состояния системы:**
   ```bash
   ./scripts/health_check.sh
   ```

2. **Управление ComfyUI:**
   ```bash
   ./scripts/comfyui_manager.sh help
   ```

3. **Доступ к веб-интерфейсу:**
   ```
   http://34.245.10.81:8188
   ```

## 📚 Подробная документация

Полная документация по установке, настройке и использованию находится в папке [`docs/`](./docs/):

- **[📖 Главная документация](./docs/README.md)** - Обзор и навигация
- **[🚀 Установка ComfyUI на сервере](./docs/01_comfyui_server_setup.md)** - Пошаговое руководство
- **[🔧 Создание кастомных скриптов](./docs/02_openai_custom_scripts.md)** - Разработка узлов
- **[🖥️ Использование веб-интерфейса](./docs/03_comfyui_web_interface.md)** - Работа с UI
- **[📋 Примеры workflows](./docs/examples/basic_workflows.md)** - Готовые примеры

## OpenAI Интеграция

Проект включает кастомные узлы для генерации изображений через OpenAI API.

### Установленные узлы

- **OpenAI Image Generator** - Генерация изображений через DALL-E 2/3
- **OpenAI Image Variation** - Создание вариаций существующих изображений

### Использование OpenAI узлов

1. **Установите OpenAI API ключ:**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

2. **В ComfyUI найдите узлы в категории "OpenAI"**

3. **Настройте параметры:**
   - **prompt**: Описание изображения
   - **model**: dall-e-2 или dall-e-3
   - **size**: Размер изображения
   - **quality**: standard или hd (только для DALL-E 3)
   - **style**: vivid или natural (только для DALL-E 3)

### Примеры использования

**Генерация пейзажа:**
```
prompt: "A beautiful sunset over mountains, digital art style"
model: dall-e-3
size: 1024x1024
quality: standard
style: vivid
```

**Генерация портрета:**
```
prompt: "A professional portrait of a woman, studio lighting"
model: dall-e-3
size: 1024x1024
quality: hd
style: natural
```

### Установка узлов

Узлы уже установлены на сервере. Для переустановки используйте:
```bash
# OpenAI узлы
./scripts/install_openai_node_server.sh

# S3 Storage узлы
./scripts/install_s3_nodes_server.sh
```

### Пример Workflow

В файле `example_openai_workflow.json` содержится пример workflow, который демонстрирует:
1. Генерацию изображения через OpenAI
2. Сохранение результата
3. Предварительный просмотр
4. Создание вариации изображения

Для загрузки workflow в ComfyUI:
1. Откройте ComfyUI: http://34.245.10.81:8188
2. Нажмите "Load" в правом верхнем углу
3. Выберите файл `workflows/example_openai_workflow.json`
4. Установите ваш OpenAI API ключ в узле
5. Нажмите "Queue Prompt" для запуска генерации