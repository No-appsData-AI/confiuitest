# 🚀 Быстрый старт с OpenAI API

## 🔑 Добавление OpenAI API ключа

### 1. Получение API ключа
1. Зайдите на [OpenAI Platform](https://platform.openai.com/)
2. Создайте аккаунт или войдите
3. Перейдите в [API Keys](https://platform.openai.com/api-keys)
4. Нажмите "Create new secret key"
5. Скопируйте ключ (начинается с `sk-`)

### 2. Установка на сервере

```bash
# Подключение к серверу
ssh -i blackholetest.pem ubuntu@34.245.10.81

# Установка переменной окружения
export OPENAI_API_KEY="sk-your-api-key-here"

# Постоянная установка
echo 'export OPENAI_API_KEY="sk-your-api-key-here"' >> ~/.bashrc
source ~/.bashrc

# Обновление systemd сервиса
sudo systemctl stop comfyui.service
sudo nano /etc/systemd/system/comfyui.service
```

Добавьте в секцию `[Service]`:
```ini
Environment=OPENAI_API_KEY=sk-your-api-key-here
```

```bash
# Перезапуск сервиса
sudo systemctl daemon-reload
sudo systemctl start comfyui.service
```

### 3. Проверка работы

```bash
# Проверка переменной
echo $OPENAI_API_KEY

# Проверка в Python
python3 -c "import os; print('API Key:', os.getenv('OPENAI_API_KEY', 'Not found'))"

# Проверка ComfyUI
curl -I http://34.245.10.81:8188
```

### 4. Использование в ComfyUI

1. Откройте http://34.245.10.81:8188
2. Найдите узлы в категории "OpenAI"
3. Добавьте узел "OpenAI Image Generator"
4. Введите промпт и нажмите "Queue Prompt"

## 📚 Подробная документация

- **[Полная документация](./docs/README.md)** - Обзор всех руководств
- **[Настройка API ключа](./docs/04_openai_api_setup.md)** - Подробные инструкции
- **[Установка сервера](./docs/01_comfyui_server_setup.md)** - Развертывание ComfyUI
- **[Создание скриптов](./docs/02_openai_custom_scripts.md)** - Разработка узлов
- **[Веб-интерфейс](./docs/03_comfyui_web_interface.md)** - Работа с UI

## 🔧 Быстрые команды

```bash
# Проверка состояния системы
./scripts/health_check.sh

# Управление ComfyUI
./scripts/comfyui_manager.sh help

# Установка OpenAI узла
./scripts/install_openai_node_server.sh
```

## 🎯 Примеры использования

### Простая генерация
```python
from examples.openai_image_generator import OpenAIImageGenerator

generator = OpenAIImageGenerator(api_key="sk-your-key")
result = generator.generate_image(
    prompt="A beautiful sunset over mountains",
    model="dall-e-3",
    size="1024x1024"
)
```

### Workflow в ComfyUI
Загрузите файл `workflows/example_openai_workflow.json` в ComfyUI

## 🚨 Устранение неполадок

### API ключ не работает
```bash
# Проверка переменной
echo $OPENAI_API_KEY

# Переустановка
export OPENAI_API_KEY="sk-your-api-key-here"
```

### ComfyUI не запускается
```bash
# Проверка статуса
sudo systemctl status comfyui.service

# Просмотр логов
sudo journalctl -u comfyui.service -f
```

### Узлы не загружаются
```bash
# Перезапуск сервиса
sudo systemctl restart comfyui.service
```

## 📞 Поддержка

- **Документация**: [docs/README.md](./docs/README.md)
- **OpenAI API**: [platform.openai.com](https://platform.openai.com/)
- **ComfyUI**: [github.com/comfyanonymous/ComfyUI](https://github.com/comfyanonymous/ComfyUI)

---

**Готово!** Теперь вы можете использовать OpenAI для генерации изображений в ComfyUI! 🎉 