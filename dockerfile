FROM python:3.8

# Копирование requirements.txt и установка зависимостей
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Копирование приложения в контейнер
COPY . /app
WORKDIR /app

# Определение переменной среды
ENV FLASK_APP=main.py

# Открытие порта
EXPOSE 5000

# Запуск приложения
CMD ["flask", "run", "--host=0.0.0.0"]
