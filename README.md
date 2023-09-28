# Backend Test-Task
 
Краткая инструкция по запуску проекта

# Установка

1. Клонируйте репозиторий:

```bash
   git clone https://github.com/Zavodsk0y/gr421_pekan.git

```

2. Перейдите в директорию проекта:

```bash
    cd project
```

3. Установите зависимости:

```bash
    pip install -r requirments.txt
```

# Запуск

1. Выполните миграции базы данных:

```bash
    python manage.py makemigrations
    python manage.py migrate
```

2. Запустите сервер:

```bash
    python manage.py runserver
```

## Дополнительная информация

В репозитории содержится postman-коллекция, в которой указана документация
для работы с проектом. Она не идеальна, но я действительно старался указать
всевозможные нюансы при работе с API.

Во время разработки проекта я также наследовал разные классы: APIView, models.ModelViewSet,
так как по мере написания проекта я постоянно узнавал и изучал что-то новое для себя.

Надеюсь, что все это как минимум заработает.

## Автор

- Петренко Константин
- Группа: 421