#!/bin/bash

# Скрипт для комплексной проверки состояния ComfyUI и сервера
# Автор: AI Assistant

SERVER_IP="34.245.10.81"
SERVER_PORT="8188"
COMFYUI_SERVICE="comfyui.service"

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== ComfyUI Health Check ===${NC}"
echo ""

# Функция для выполнения команд на сервере
run_on_server() {
    ssh -i blackholetest.pem -o StrictHostKeyChecking=no ubuntu@${SERVER_IP} "$1"
}

# Проверка подключения к серверу
echo -e "${YELLOW}1. Проверка подключения к серверу...${NC}"
if ssh -i blackholetest.pem -o StrictHostKeyChecking=no -o ConnectTimeout=5 ubuntu@${SERVER_IP} "echo 'test'" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Сервер доступен${NC}"
else
    echo -e "${RED}✗ Сервер недоступен${NC}"
    exit 1
fi

# Проверка статуса ComfyUI сервиса
echo -e "${YELLOW}2. Проверка статуса ComfyUI сервиса...${NC}"
SERVICE_STATUS=$(run_on_server "sudo systemctl is-active ${COMFYUI_SERVICE}")
if [ "$SERVICE_STATUS" = "active" ]; then
    echo -e "${GREEN}✓ ComfyUI сервис активен${NC}"
else
    echo -e "${RED}✗ ComfyUI сервис неактивен (статус: $SERVICE_STATUS)${NC}"
fi

# Проверка доступности веб-интерфейса
echo -e "${YELLOW}3. Проверка доступности веб-интерфейса...${NC}"
if curl -s http://${SERVER_IP}:${SERVER_PORT} > /dev/null; then
    echo -e "${GREEN}✓ Веб-интерфейс доступен${NC}"
    echo -e "${BLUE}  URL: http://${SERVER_IP}:${SERVER_PORT}${NC}"
else
    echo -e "${RED}✗ Веб-интерфейс недоступен${NC}"
fi

# Проверка использования ресурсов
echo -e "${YELLOW}4. Проверка использования ресурсов...${NC}"
MEMORY_USAGE=$(run_on_server "free -h | grep Mem | awk '{print \$3}'")
TOTAL_MEMORY=$(run_on_server "free -h | grep Mem | awk '{print \$2}'")
DISK_USAGE=$(run_on_server "df -h / | tail -1 | awk '{print \$5}'")

echo -e "${BLUE}  Память: ${MEMORY_USAGE} / ${TOTAL_MEMORY}${NC}"
echo -e "${BLUE}  Диск: ${DISK_USAGE}${NC}"

# Проверка процессов ComfyUI
echo -e "${YELLOW}5. Проверка процессов ComfyUI...${NC}"
PROCESS_COUNT=$(run_on_server "ps aux | grep -v grep | grep -c python.*main.py")
if [ "$PROCESS_COUNT" -gt 0 ]; then
    echo -e "${GREEN}✓ Найдено процессов ComfyUI: $PROCESS_COUNT${NC}"
else
    echo -e "${RED}✗ Процессы ComfyUI не найдены${NC}"
fi

# Проверка последних логов
echo -e "${YELLOW}6. Последние записи в логах...${NC}"
run_on_server "sudo journalctl -u ${COMFYUI_SERVICE} -n 5 --no-pager"

# Проверка версии ComfyUI
echo -e "${YELLOW}7. Информация о версии...${NC}"
VERSION_INFO=$(run_on_server "cd /home/ubuntu/ComfyUI && source venv/bin/activate && python -c \"import sys; print('Python:', sys.version.split()[0])\"")
echo -e "${BLUE}  $VERSION_INFO${NC}"

# Проверка портов
echo -e "${YELLOW}8. Проверка открытых портов...${NC}"
PORT_STATUS=$(run_on_server "ss -tlnp | grep :${SERVER_PORT}")
if [ -n "$PORT_STATUS" ]; then
    echo -e "${GREEN}✓ Порт ${SERVER_PORT} открыт${NC}"
else
    echo -e "${RED}✗ Порт ${SERVER_PORT} не открыт${NC}"
fi

echo ""
echo -e "${BLUE}=== Результаты проверки ===${NC}"

# Итоговая оценка
if [ "$SERVICE_STATUS" = "active" ] && curl -s http://${SERVER_IP}:${SERVER_PORT} > /dev/null; then
    echo -e "${GREEN}✓ ComfyUI работает корректно!${NC}"
    echo -e "${GREEN}  Доступен по адресу: http://${SERVER_IP}:${SERVER_PORT}${NC}"
else
    echo -e "${RED}✗ Обнаружены проблемы с ComfyUI${NC}"
    echo -e "${YELLOW}  Проверьте логи: ./comfyui_manager.sh logs${NC}"
fi

echo ""
echo -e "${BLUE}Для управления используйте: ./comfyui_manager.sh help${NC}" 