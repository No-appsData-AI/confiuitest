# Настройка OpenAI API ключа

## Обзор

Для работы с кастомными узлами OpenAI в ComfyUI необходимо настроить API ключ. Это руководство покажет все способы добавления и настройки ключа.

## 🔑 Получение OpenAI API ключа

### 1. Создание аккаунта OpenAI

1. **Перейдите на [OpenAI Platform](https://platform.openai.com/)**
2. **Зарегистрируйтесь** или войдите в существующий аккаунт
3. **Подтвердите email** и настройте двухфакторную аутентификацию

### 2. Создание API ключа

1. **Откройте [API Keys](https://platform.openai.com/api-keys)**
2. **Нажмите "Create new secret key"**
3. **Введите название** ключа (например: "ComfyUI Integration")
4. **Скопируйте ключ** (он начинается с `sk-`)
5. **Сохраните ключ** в безопасном месте

⚠️ **Важно**: Ключ показывается только один раз!

## 🛠️ Способы настройки API ключа

### 1. Переменная окружения (Рекомендуемый способ)

#### На сервере Ubuntu:

```bash
# Временная установка (до перезагрузки)
export OPENAI_API_KEY="sk-your-api-key-here"

# Постоянная установка для пользователя
echo 'export OPENAI_API_KEY="sk-your-api-key-here"' >> ~/.bashrc
source ~/.bashrc

# Постоянная установка для системы
sudo bash -c 'echo "OPENAI_API_KEY=sk-your-api-key-here" >> /etc/environment'
```

#### Проверка установки:

```bash
# Проверка переменной
echo $OPENAI_API_KEY

# Проверка в Python
python3 -c "import os; print('API Key:', os.getenv('OPENAI_API_KEY', 'Not found'))"
```

### 2. Файл конфигурации

#### Создание .env файла:

```bash
# Создание файла в домашней директории
cat > ~/.openai_config << 'EOF'
OPENAI_API_KEY=sk-your-api-key-here
EOF

# Установка прав доступа
chmod 600 ~/.openai_config
```

#### Загрузка в Python:

```python
# В начале скрипта
import os
from dotenv import load_dotenv

load_dotenv('~/.openai_config')
api_key = os.getenv('OPENAI_API_KEY')
```

### 3. Прямая передача в коде

```python
# В Python скрипте
from examples.openai_image_generator import OpenAIImageGenerator

generator = OpenAIImageGenerator(api_key="sk-your-api-key-here")
```

### 4. Через веб-интерфейс ComfyUI

1. **Откройте ComfyUI**: http://your-server-ip:8188
2. **Добавьте узел OpenAI Image Generator**
3. **В поле "api_key" введите ваш ключ**
4. **Нажмите "Queue Prompt"**

## 🔧 Настройка для ComfyUI сервиса

### Обновление systemd сервиса:

```bash
# Остановка сервиса
sudo systemctl stop comfyui.service

# Редактирование сервисного файла
sudo nano /etc/systemd/system/comfyui.service
```

#### Добавление переменной окружения в сервис:

```ini
[Unit]
Description=ComfyUI Service
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/ComfyUI
Environment=PATH=/home/ubuntu/comfyui_env/bin
Environment=OPENAI_API_KEY=sk-your-api-key-here
ExecStart=/home/ubuntu/comfyui_env/bin/python main.py --listen 0.0.0.0 --port 8188 --enable-cors-header --cpu
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

#### Перезапуск сервиса:

```bash
# Перезагрузка конфигурации
sudo systemctl daemon-reload

# Запуск сервиса
sudo systemctl start comfyui.service

# Проверка статуса
sudo systemctl status comfyui.service
```

## 🧪 Тестирование API ключа

### 1. Простой тест Python:

```python
#!/usr/bin/env python3
import os
import requests

# Получение API ключа
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("❌ OPENAI_API_KEY не установлен")
    exit(1)

# Тестовый запрос
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.get("https://api.openai.com/v1/models", headers=headers)

if response.status_code == 200:
    print("✅ API ключ работает корректно")
    models = response.json()
    print(f"Доступные модели: {len(models['data'])}")
else:
    print(f"❌ Ошибка API: {response.status_code}")
    print(f"Ответ: {response.text}")
```

### 2. Тест через наш генератор:

```python
#!/usr/bin/env python3
import os
from examples.openai_image_generator import OpenAIImageGenerator

# Получение API ключа
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("❌ OPENAI_API_KEY не установлен")
    exit(1)

# Создание генератора
generator = OpenAIImageGenerator(api_key)

# Тестовая генерация
result = generator.generate_image(
    prompt="A simple red circle on white background",
    model="dall-e-3",
    size="1024x1024"
)

if result["success"]:
    print("✅ Генерация успешна!")
    print(f"Модель: {result['model']}")
    print(f"Создано: {result['created']}")
else:
    print(f"❌ Ошибка генерации: {result['error']}")
```

### 3. Тест через ComfyUI:

1. **Откройте ComfyUI**
2. **Добавьте узел OpenAI Image Generator**
3. **Введите простой промпт**: "A red circle"
4. **Нажмите "Queue Prompt"**
5. **Проверьте результат**

## 🔒 Безопасность

### Рекомендации по безопасности:

1. **Никогда не коммитьте API ключи в Git**
   ```bash
   # Добавьте в .gitignore
   echo "*.key" >> .gitignore
   echo ".env" >> .gitignore
   echo "api_keys.txt" >> .gitignore
   ```

2. **Используйте переменные окружения**
   ```bash
   # Вместо хардкода в коде
   api_key = "sk-..."  # ❌ Плохо
   
   # Используйте переменные окружения
   api_key = os.getenv('OPENAI_API_KEY')  # ✅ Хорошо
   ```

3. **Ограничьте права доступа к файлам**
   ```bash
   chmod 600 ~/.openai_config
   chmod 600 ~/.env
   ```

4. **Регулярно ротируйте ключи**
   - Создавайте новые ключи каждые 3-6 месяцев
   - Удаляйте неиспользуемые ключи

### Мониторинг использования:

```bash
# Проверка баланса аккаунта
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
     https://api.openai.com/v1/dashboard/billing/usage

# Проверка лимитов
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
     https://api.openai.com/v1/dashboard/billing/subscription
```

## 🚨 Устранение неполадок

### Проблема: "API key not found"

```bash
# Проверка переменной окружения
echo $OPENAI_API_KEY

# Переустановка переменной
export OPENAI_API_KEY="sk-your-api-key-here"

# Проверка в Python
python3 -c "import os; print(os.getenv('OPENAI_API_KEY'))"
```

### Проблема: "Invalid API key"

```bash
# Проверка формата ключа
echo $OPENAI_API_KEY | grep -E "^sk-[a-zA-Z0-9]{32,}$"

# Проверка на лишние символы
echo $OPENAI_API_KEY | tr -d ' '
```

### Проблема: "Insufficient quota"

```bash
# Проверка баланса
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
     https://api.openai.com/v1/dashboard/billing/usage

# Пополнение баланса на OpenAI Platform
```

### Проблема: "Rate limit exceeded"

```bash
# Добавление задержки между запросами
import time
time.sleep(1)  # Задержка 1 секунда между запросами
```

## 📊 Мониторинг использования

### Скрипт мониторинга:

```bash
#!/bin/bash
# monitor_openai_usage.sh

API_KEY=$OPENAI_API_KEY
if [ -z "$API_KEY" ]; then
    echo "❌ OPENAI_API_KEY не установлен"
    exit 1
fi

echo "📊 Мониторинг использования OpenAI API"
echo "======================================"

# Получение информации об использовании
USAGE=$(curl -s -H "Authorization: Bearer $API_KEY" \
     https://api.openai.com/v1/dashboard/billing/usage)

# Получение информации о подписке
SUBSCRIPTION=$(curl -s -H "Authorization: Bearer $API_KEY" \
     https://api.openai.com/v1/dashboard/billing/subscription)

echo "Использование: $USAGE"
echo "Подписка: $SUBSCRIPTION"
```

### Автоматический мониторинг:

```bash
# Добавление в crontab
crontab -e

# Проверка каждые 6 часов
0 */6 * * * /path/to/monitor_openai_usage.sh >> /var/log/openai_usage.log 2>&1
```

## 🎯 Лучшие практики

### 1. Организация ключей:

```bash
# Структура для множественных ключей
~/.openai/
├── keys/
│   ├── comfyui.key
│   ├── development.key
│   └── production.key
├── config/
│   └── settings.json
└── logs/
    └── usage.log
```

### 2. Автоматическая загрузка:

```bash
# В ~/.bashrc
if [ -f ~/.openai/load_keys.sh ]; then
    source ~/.openai/load_keys.sh
fi
```

### 3. Ротация ключей:

```bash
#!/bin/bash
# rotate_keys.sh

# Создание нового ключа
NEW_KEY=$(curl -X POST \
    -H "Authorization: Bearer $CURRENT_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"name":"ComfyUI-$(date +%Y%m%d)"}' \
    https://api.openai.com/v1/api_keys | jq -r '.secret')

# Обновление переменной окружения
echo "export OPENAI_API_KEY=\"$NEW_KEY\"" > ~/.openai/current_key.sh
source ~/.openai/current_key.sh
```

## Заключение

Правильная настройка OpenAI API ключа критически важна для работы с кастомными узлами в ComfyUI. Следуйте рекомендациям по безопасности и регулярно мониторьте использование API.

### ✅ Чек-лист настройки:

- [ ] Получен API ключ с OpenAI Platform
- [ ] Ключ установлен как переменная окружения
- [ ] Обновлен systemd сервис ComfyUI
- [ ] Протестирована работа API
- [ ] Настроена безопасность
- [ ] Настроен мониторинг использования 