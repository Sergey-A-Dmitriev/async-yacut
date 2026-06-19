# ASYNC-YaCut + API

## Описание проекта

**Проект YaCut** — это сервис укорачивания ссылок. Его назначение — ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис.
Дополнительная функция YaCut — загрузка сразу нескольких файлов на Яндекс Диск и предоставление коротких ссылок пользователю для скачивания этих файлов.

## Технологии

- Flask 3.0.2
- Flask-SQLAlchemy 3.1.1
- Flask-WTF 1.2.1
- Python 3.12+
- aiohttp 3.10.5

## Локальное развертывание

**Клонирование репозитория:**

```bash

git clone https://github.com/Sergey-A-Dmitriev/async-yacut.git
cd async-yacut
```

**Создание и активация виртуального окружения:**

```bash

python -m venv venv

source venv/bin/activate  # Для Linux/macOS

source venv/Scripts/activate    # Для Windows
```

**Установка зависимостей:**

```bash

pip install -r requirements.txt
```

**Создать в директории проекта файл .env с переменными окружения:**

```
FLASK_APP=yacut
FLASK_DEBUG=1
SECRET_KEY=your_secret_key
DATABASE_URI=sqlite:///db.sqlite3
DISK_TOKEN=<Токен_от_ЯндексДиска>
```

**Создать базу данных и применить миграции:**

```bash

flask db upgrade
```

**Запуск проекта на локальном сервере:**

```bash

flask run
```

Сервер будет доступен по адресу  
[локальный сервер](http://127.0.0.1:5000/)


## Документация API
Доступна по адресу [http://127.0.0.1:5000/doc/](http://127.0.0.1:5000/doc/)


## Автор

[Дмитриев Сергей](https://github.com/Sergey-A-Dmitriev)

## Контакты

Email: [sadmitriev@mail.ru](mailto:sadmitriev@mail.ru)
