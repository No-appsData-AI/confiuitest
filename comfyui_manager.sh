#!/bin/bash

# Скрипт для управления ComfyUI на сервере
# Автор: AI Assistant

COMFYUI_SERVICE="comfyui.service"
SERVER_IP="34.245.10.81"
SERVER_PORT="8188"

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для вывода справки
show_help() {
    echo -e "${BLUE}ComfyUI Manager - Скрипт для управления ComfyUI на сервере${NC}"
    echo ""
    echo "Использование: $0 [команда]"
    echo ""
    echo "Команды:"
    echo "  start     - Запустить ComfyUI сервис"
    echo "  stop      - Остановить ComfyUI сервис"
    echo "  restart   - Перезапустить ComfyUI сервис"
    echo "  status    - Показать статус сервиса"
    echo "  logs      - Показать логи сервиса"
    echo "  url       - Показать URL для доступа к ComfyUI"
    echo "  test      - Проверить доступность ComfyUI"
    echo "  help      - Показать эту справку"
    echo ""
    echo "Примеры:"
    echo "  $0 start"
    echo "  $0 status"
    echo "  $0 logs"
}

# Функция для выполнения команд на сервере
run_on_server() {
    ssh -i blackholetest.pem -o StrictHostKeyChecking=no ubuntu@${SERVER_IP} "$1"
}

# Функция для запуска сервиса
start_service() {
    echo -e "${YELLOW}Запуск ComfyUI сервиса...${NC}"
    run_on_server "sudo systemctl start ${COMFYUI_SERVICE}"
    sleep 3
    status_service
}

# Функция для остановки сервиса
stop_service() {
    echo -e "${YELLOW}Остановка ComfyUI сервиса...${NC}"
    run_on_server "sudo systemctl stop ${COMFYUI_SERVICE}"
    echo -e "${GREEN}Сервис остановлен${NC}"
}

# Функция для перезапуска сервиса
restart_service() {
    echo -e "${YELLOW}Перезапуск ComfyUI сервиса...${NC}"
    run_on_server "sudo systemctl restart ${COMFYUI_SERVICE}"
    sleep 3
    status_service
}

# Функция для показа статуса сервиса
status_service() {
    echo -e "${BLUE}Статус ComfyUI сервиса:${NC}"
    run_on_server "sudo systemctl status ${COMFYUI_SERVICE}"
}

# Функция для показа логов
show_logs() {
    echo -e "${BLUE}Логи ComfyUI сервиса (последние 20 строк):${NC}"
    run_on_server "sudo journalctl -u ${COMFYUI_SERVICE} -n 20"
}

# Функция для показа URL
show_url() {
    echo -e "${GREEN}URL для доступа к ComfyUI:${NC}"
    echo "http://${SERVER_IP}:${SERVER_PORT}"
    echo ""
    echo -e "${YELLOW}Локальный доступ:${NC}"
    echo "http://localhost:${SERVER_PORT}"
}

# Функция для тестирования доступности
test_connection() {
    echo -e "${BLUE}Проверка доступности ComfyUI...${NC}"
    if curl -s http://${SERVER_IP}:${SERVER_PORT} > /dev/null; then
        echo -e "${GREEN}✓ ComfyUI доступен по адресу http://${SERVER_IP}:${SERVER_PORT}${NC}"
    else
        echo -e "${RED}✗ ComfyUI недоступен${NC}"
    fi
}

# Основная логика
case "$1" in
    start)
        start_service
        ;;
    stop)
        stop_service
        ;;
    restart)
        restart_service
        ;;
    status)
        status_service
        ;;
    logs)
        show_logs
        ;;
    url)
        show_url
        ;;
    test)
        test_connection
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}Ошибка: Неизвестная команда '$1'${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac 