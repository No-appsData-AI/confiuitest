#!/bin/bash
# Комплексная установка всех компонентов ComfyUI Integration
# Автор: AI Assistant
# Версия: 1.0.0

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Функции логирования
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

log_step() {
    echo -e "${PURPLE}🔧 $1${NC}"
}

log_component() {
    echo -e "${CYAN}📦 $1${NC}"
}

# Проверка аргументов
if [ $# -eq 0 ]; then
    log_error "Использование: $0 <путь_к_comfyui> [сервер_ip]"
    log_info "Пример: $0 /home/ubuntu/ComfyUI 34.245.10.81"
    exit 1
fi

COMFYUI_PATH="$1"
SERVER_IP="${2:-34.245.10.81}"

log_info "🚀 Комплексная установка ComfyUI Integration"
log_info "Путь к ComfyUI: $COMFYUI_PATH"
log_info "Сервер: $SERVER_IP"

# Функция для выполнения команд на сервере
run_on_server() {
    if [ -n "$SERVER_IP" ] && [ "$SERVER_IP" != "localhost" ]; then
        ssh -i blackholetest.pem -o StrictHostKeyChecking=no ubuntu@${SERVER_IP} "$1"
    else
        eval "$1"
    fi
}

# Функция для копирования файлов на сервер
copy_to_server() {
    local source="$1"
    local dest="$2"
    if [ -n "$SERVER_IP" ] && [ "$SERVER_IP" != "localhost" ]; then
        scp -i blackholetest.pem "$source" "ubuntu@${SERVER_IP}:$dest"
    else
        cp "$source" "$dest"
    fi
}

# Проверка подключения к серверу
if [ -n "$SERVER_IP" ] && [ "$SERVER_IP" != "localhost" ]; then
    log_step "Проверка подключения к серверу..."
    if ! run_on_server "echo 'test'" > /dev/null 2>&1; then
        log_error "Сервер недоступен: $SERVER_IP"
        exit 1
    fi
    log_success "Сервер доступен"
fi

# 1. Установка Pipeline Builder
log_component "Установка Pipeline Builder..."
run_on_server "bash -c 'cd $(pwd) && ./scripts/install_pipeline_builder_server.sh $COMFYUI_PATH'"

# 2. Установка S3 Storage узлов
log_component "Установка S3 Storage узлов..."
run_on_server "bash -c 'cd $(pwd) && ./scripts/install_s3_nodes_server.sh $COMFYUI_PATH'"

# 3. Установка OpenAI узлов
log_component "Установка OpenAI узлов..."
run_on_server "bash -c 'cd $(pwd) && ./scripts/install_openai_node_server.sh $COMFYUI_PATH'"

# 4. Установка конфигурации
log_component "Установка конфигурации..."
CONFIG_DIR="$COMFYUI_PATH/config"
run_on_server "mkdir -p $CONFIG_DIR"

# Копирование конфигурационных файлов
copy_to_server "config/settings.py" "$CONFIG_DIR/"
copy_to_server "config/comfyui.service" "$CONFIG_DIR/"

# 5. Установка документации
log_component "Установка документации..."
DOCS_DIR="$COMFYUI_PATH/docs"
run_on_server "mkdir -p $DOCS_DIR"

# Копирование документации
copy_to_server "docs/README.md" "$DOCS_DIR/"
copy_to_server "docs/01_comfyui_server_setup.md" "$DOCS_DIR/"
copy_to_server "docs/02_openai_custom_scripts.md" "$DOCS_DIR/"
copy_to_server "docs/03_comfyui_web_interface.md" "$DOCS_DIR/"
copy_to_server "docs/04_openai_api_setup.md" "$DOCS_DIR/"
copy_to_server "docs/05_s3_storage_integration.md" "$DOCS_DIR/"
copy_to_server "docs/06_pipeline_builder_guide.md" "$DOCS_DIR/"
copy_to_server "docs/07_installation_guide.md" "$DOCS_DIR/"

# 6. Установка утилит
log_component "Установка утилит..."
UTILS_DIR="$COMFYUI_PATH/utils"
run_on_server "mkdir -p $UTILS_DIR"

# Копирование утилит
copy_to_server "scripts/health_check.sh" "$UTILS_DIR/"
copy_to_server "scripts/comfyui_manager.sh" "$UTILS_DIR/"
copy_to_server "scripts/start_comfyui.sh" "$UTILS_DIR/"

# Установка прав на выполнение
run_on_server "chmod +x $UTILS_DIR/*.sh"

# 7. Установка тестов
log_component "Установка тестов..."
TESTS_DIR="$COMFYUI_PATH/tests"
run_on_server "mkdir -p $TESTS_DIR"

# Копирование тестов
copy_to_server "tests/test_basic_functionality.py" "$TESTS_DIR/"

# 8. Создание переменных окружения
log_component "Настройка переменных окружения..."
ENV_FILE="$COMFYUI_PATH/.env"
run_on_server "cat > $ENV_FILE << 'EOF'
# ComfyUI Configuration
COMFYUI_URL=http://localhost:8188
COMFYUI_PORT=8188

# AWS S3 Configuration
AWS_ACCESS_KEY_ID=your-access-key-here
AWS_SECRET_ACCESS_KEY=your-secret-key-here
AWS_REGION=us-east-1
S3_BUCKET=comfyui-images

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here

# Pipeline Builder Configuration
PIPELINE_BUILDER_LOG_LEVEL=INFO
PIPELINE_BUILDER_TIMEOUT=300

# Development Configuration
DEBUG=false
LOG_LEVEL=INFO
EOF"

# 9. Создание systemd сервиса
log_component "Настройка systemd сервиса..."
run_on_server "sudo cp $CONFIG_DIR/comfyui.service /etc/systemd/system/"
run_on_server "sudo systemctl daemon-reload"

# 10. Создание скрипта управления
log_component "Создание скрипта управления..."
MANAGER_SCRIPT="$COMFYUI_PATH/manage_comfyui.sh"
run_on_server "cat > $MANAGER_SCRIPT << 'EOF'
#!/bin/bash
# Скрипт управления ComfyUI Integration
# Автор: AI Assistant

set -e

COMFYUI_PATH=\"$(dirname \"\$0\")\"
UTILS_DIR=\"\$COMFYUI_PATH/utils\"

# Цвета для вывода
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
BLUE='\\033[0;34m'
NC='\\033[0m'

log_info() {
    echo -e \"\${BLUE}ℹ️  \$1\${NC}\"
}

log_success() {
    echo -e \"\${GREEN}✅ \$1\${NC}\"
}

log_warning() {
    echo -e \"\${YELLOW}⚠️  \$1\${NC}\"
}

log_error() {
    echo -e \"\${RED}❌ \$1\${NC}\"
}

# Функция показа справки
show_help() {
    echo \"ComfyUI Integration Manager\"
    echo \"\"
    echo \"Использование: \$0 <команда>\"
    echo \"\"
    echo \"Команды:\"
    echo \"  start     - Запуск ComfyUI сервиса\"
    echo \"  stop      - Остановка ComfyUI сервиса\"
    echo \"  restart   - Перезапуск ComfyUI сервиса\"
    echo \"  status    - Статус ComfyUI сервиса\"
    echo \"  logs      - Просмотр логов\"
    echo \"  health    - Проверка состояния системы\"
    echo \"  test      - Запуск тестов\"
    echo \"  pipeline  - Управление пайплайнами\"
    echo \"  docs      - Открытие документации\"
    echo \"  config    - Редактирование конфигурации\"
    echo \"  help      - Показать эту справку\"
    echo \"\"
}

# Функция проверки состояния
check_health() {
    log_info \"Проверка состояния системы...\"
    \"\$UTILS_DIR/health_check.sh\"
}

# Функция запуска тестов
run_tests() {
    log_info \"Запуск тестов...\"
    cd \"\$COMFYUI_PATH\"
    source venv/bin/activate
    python3 tests/test_basic_functionality.py
}

# Функция управления пайплайнами
manage_pipelines() {
    log_info \"Управление пайплайнами...\"
    cd \"\$COMFYUI_PATH/custom_nodes/pipeline_builder\"
    source \"\$COMFYUI_PATH/venv/bin/activate\"
    
    if [ \$# -eq 0 ]; then
        echo \"Доступные команды:\"
        echo \"  create <тип> [параметры] - создание пайплайна\"
        echo \"  test <файл> - тестирование пайплайна\"
        echo \"  list - список доступных узлов\"
        return
    fi
    
    case \"\$1\" in
        \"create\")
            python3 create_pipeline.py \"\${@:2}\"
            ;;
        \"test\")
            python3 test_pipeline.py \"\${@:2}\"
            ;;
        \"list\")
            python3 -c \"
from pipeline_manager import PipelineManager
manager = PipelineManager()
nodes = manager.list_available_nodes()
print('Доступные узлы:')
for node_type in nodes.keys():
    print(f'  - {node_type}')
\"
            ;;
        *)
            log_error \"Неизвестная команда: \$1\"
            ;;
    esac
}

# Основная логика
case \"\$1\" in
    \"start\")
        log_info \"Запуск ComfyUI сервиса...\"
        sudo systemctl start comfyui.service
        log_success \"ComfyUI запущен\"
        ;;
    \"stop\")
        log_info \"Остановка ComfyUI сервиса...\"
        sudo systemctl stop comfyui.service
        log_success \"ComfyUI остановлен\"
        ;;
    \"restart\")
        log_info \"Перезапуск ComfyUI сервиса...\"
        sudo systemctl restart comfyui.service
        log_success \"ComfyUI перезапущен\"
        ;;
    \"status\")
        sudo systemctl status comfyui.service
        ;;
    \"logs\")
        sudo journalctl -u comfyui.service -f
        ;;
    \"health\")
        check_health
        ;;
    \"test\")
        run_tests
        ;;
    \"pipeline\")
        manage_pipelines \"\${@:2}\"
        ;;
    \"docs\")
        log_info \"Документация доступна в: \$COMFYUI_PATH/docs/\"
        log_info \"Основной файл: \$COMFYUI_PATH/docs/README.md\"
        ;;
    \"config\")
        log_info \"Редактирование конфигурации...\"
        nano \"\$COMFYUI_PATH/.env\"
        ;;
    \"help\"|\"\"|\"--help\"|\"-h\")
        show_help
        ;;
    *)
        log_error \"Неизвестная команда: \$1\"
        show_help
        exit 1
        ;;
esac
EOF"

run_on_server "chmod +x $MANAGER_SCRIPT"

# 11. Создание README для сервера
log_component "Создание README для сервера..."
SERVER_README="$COMFYUI_PATH/README_SERVER.md"
run_on_server "cat > $SERVER_README << 'EOF'
# ComfyUI Integration Server

Этот сервер настроен для работы с ComfyUI и всеми дополнительными компонентами.

## Установленные компоненты

### 🎨 Pipeline Builder
- Программное создание пайплайнов ComfyUI
- Интеграция с OpenAI и AWS S3
- Готовые шаблоны пайплайнов
- CLI интерфейс для управления

### ☁️ S3 Storage Integration
- Загрузка изображений в AWS S3
- Скачивание изображений из S3
- Управление workflows в облаке
- Информация о хранилище

### 🤖 OpenAI Integration
- Генерация изображений через DALL-E
- Создание вариаций изображений
- Интеграция в пайплайны ComfyUI

## Управление сервером

### Основные команды
```bash
# Управление ComfyUI
./manage_comfyui.sh start      # Запуск
./manage_comfyui.sh stop       # Остановка
./manage_comfyui.sh restart    # Перезапуск
./manage_comfyui.sh status     # Статус
./manage_comfyui.sh logs       # Логи

# Проверка состояния
./manage_comfyui.sh health     # Проверка здоровья
./manage_comfyui.sh test       # Запуск тестов

# Управление пайплайнами
./manage_comfyui.sh pipeline create openai \"Beautiful sunset\"
./manage_comfyui.sh pipeline test my_pipeline.json
./manage_comfyui.sh pipeline list

# Документация и конфигурация
./manage_comfyui.sh docs       # Открыть документацию
./manage_comfyui.sh config     # Редактировать конфигурацию
```

### Утилиты
- `utils/health_check.sh` - Проверка состояния системы
- `utils/comfyui_manager.sh` - Управление ComfyUI
- `utils/start_comfyui.sh` - Ручной запуск ComfyUI

## Конфигурация

### Переменные окружения
Файл: `.env`
```bash
# AWS S3
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=us-east-1
S3_BUCKET=comfyui-images

# OpenAI
OPENAI_API_KEY=your-openai-key

# ComfyUI
COMFYUI_URL=http://localhost:8188
```

### Настройка
1. Отредактируйте файл `.env`
2. Установите ваши API ключи
3. Перезапустите сервис: `./manage_comfyui.sh restart`

## Доступ

- **Веб-интерфейс ComfyUI**: http://localhost:8188
- **Внешний доступ**: http://SERVER_IP:8188
- **Документация**: `docs/README.md`
- **Логи**: `sudo journalctl -u comfyui.service -f`

## Структура проекта

```
ComfyUI/
├── custom_nodes/
│   ├── pipeline_builder/     # Pipeline Builder
│   ├── s3_storage/          # S3 Storage узлы
│   └── openai_integration/  # OpenAI узлы
├── config/                  # Конфигурация
├── docs/                    # Документация
├── utils/                   # Утилиты
├── tests/                   # Тесты
├── .env                     # Переменные окружения
├── manage_comfyui.sh        # Скрипт управления
└── README_SERVER.md         # Эта документация
```

## Поддержка

При возникновении проблем:
1. Проверьте логи: `./manage_comfyui.sh logs`
2. Запустите тесты: `./manage_comfyui.sh test`
3. Проверьте состояние: `./manage_comfyui.sh health`
4. Обратитесь к документации: `./manage_comfyui.sh docs`
EOF"

# 12. Финальная проверка
log_component "Финальная проверка установки..."
run_on_server "cd $COMFYUI_PATH && ./manage_comfyui.sh health"

# 13. Запуск ComfyUI
log_component "Запуск ComfyUI..."
run_on_server "sudo systemctl enable comfyui.service"
run_on_server "sudo systemctl start comfyui.service"

# Ожидание запуска
log_info "Ожидание запуска ComfyUI..."
sleep 10

# Проверка статуса
if run_on_server "sudo systemctl is-active comfyui.service" | grep -q "active"; then
    log_success "ComfyUI успешно запущен"
else
    log_warning "ComfyUI не запустился автоматически"
    log_info "Запустите вручную: ./manage_comfyui.sh start"
fi

# Итоговый отчет
log_success "🎉 Комплексная установка завершена!"
echo ""
log_info "📋 Установленные компоненты:"
log_info "  ✅ Pipeline Builder - программное создание пайплайнов"
log_info "  ✅ S3 Storage Integration - интеграция с AWS S3"
log_info "  ✅ OpenAI Integration - интеграция с OpenAI API"
log_info "  ✅ Конфигурация и документация"
log_info "  ✅ Утилиты управления"
log_info "  ✅ Автоматические тесты"
echo ""
log_info "🔧 Управление:"
log_info "  Основной скрипт: ./manage_comfyui.sh"
log_info "  Справка: ./manage_comfyui.sh help"
echo ""
log_info "🌐 Доступ:"
if [ -n "$SERVER_IP" ] && [ "$SERVER_IP" != "localhost" ]; then
    log_info "  Внешний: http://$SERVER_IP:8188"
else
    log_info "  Локальный: http://localhost:8188"
fi
echo ""
log_info "📚 Документация:"
log_info "  Серверная: $COMFYUI_PATH/README_SERVER.md"
log_info "  Полная: $COMFYUI_PATH/docs/README.md"
echo ""
log_info "🔑 Следующие шаги:"
log_info "  1. Настройте API ключи в файле .env"
log_info "  2. Запустите тесты: ./manage_comfyui.sh test"
log_info "  3. Создайте первый пайплайн: ./manage_comfyui.sh pipeline create openai 'Test prompt'" 