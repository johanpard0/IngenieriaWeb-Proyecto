PORT=${PORT:-8000}
echo "========================================================="
echo "Iniciando FastAPI"

gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:$PORT