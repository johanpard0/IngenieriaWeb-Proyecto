#!/bin/bash
# Script de inicio para FastAPI en Azure App Service

PORT=${PORT:-8000}

echo "=========================================="
echo "🚀 Iniciando FastAPI en el puerto $PORT"
echo "📁 Carpeta de trabajo: src"
echo "🔧 Archivo principal: main.py"
echo "🔧 Instancia: app"
echo "=========================================="

gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --chdir src --bind 0.0.0.0:$PORT