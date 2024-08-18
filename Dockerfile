# Используем базовый образ с поддержкой CUDA для GPU
FROM nvidia/cuda:11.6.2-base-ubuntu20.04

# Установите зависимости для установки Python 3.9
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.9 python3.9-distutils python3-pip ffmpeg

# Создайте символическую ссылку на python3.9
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1 && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1

# Обновите pip
RUN pip install -r requirements.txt
RUN python -m pip install --upgrade pip setuptools wheel

# Установите необходимые Python библиотеки
RUN pip install torch==2.1.0
RUN pip install audiocraft

# Создайте рабочую директорию
WORKDIR /app

# Скопируйте ваш скрипт в контейнер
COPY app.py /app/app.py

# Откройте порт 5000
EXPOSE 5000

# Запустите скрипт
CMD ["python", "app.py"]
