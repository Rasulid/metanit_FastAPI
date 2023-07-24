# Используем базовый образ Python 3.10
FROM python:3.10

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копируем все файлы проекта внутрь контейнера
COPY . .

# Запускаем миграции базы данных
RUN chmod a+x app/docker/*.sh

# Запускаем FastAPI приложение с помощью Gunicorn
#CMD ["gunicorn", "main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]