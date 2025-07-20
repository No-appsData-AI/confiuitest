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

## Файлы проекта

- `blackholetest.pem` - SSH ключ для подключения к серверу
- `start_comfyui.sh` - Скрипт для ручного запуска ComfyUI
- `comfyui.service` - Systemd сервис файл
- `comfyui_manager.sh` - Скрипт управления ComfyUI
- `health_check.sh` - Скрипт комплексной проверки состояния системы
- `README.md` - Документация проекта

## Быстрый старт

1. **Проверка состояния системы:**
   ```bash
   ./health_check.sh
   ```

2. **Управление ComfyUI:**
   ```bash
   ./comfyui_manager.sh help
   ```

3. **Доступ к веб-интерфейсу:**
   ```
   http://34.245.10.81:8188
   ```