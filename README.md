# Сайт рецептов Foodgram
![Project Workflow](https://github.com/oxiplegatz/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
## Технологии
* Django 3.2
* Python 3.7
* Rest Framework 3.12.4
* Postgre SQL
* Nginx
* Docker

## О проекте
Проект Foodgram — это готовое API для сервиса, на котором пользователи могут
публиковать свои рецепты. Можно подписываться на других пользователей,
добавлять рецепты в избранное, а также составить и скачать список покупок.

Проект, реализованный с фронтендом на React, доступен по адресу http://159.223.14.232/recipes

## Как работать с репозиторием
Клонировать репозиторий на локальную машину  
`git clone https://github.com/oxiplegatz/foodgram-project-react.git`

Для того чтобы развернуть проект локально, необходимо установить Docker
и Python.   
При локальной сборке нужно поменять адрес расположения документации
в файле docker-compose на  

`- ../docs/:/usr/share/nginx/html/api/docs/`

Шаг 1. Создайте файл .env с переменными окружения
(при локальном запуске файл нужно создать в папке infra/)  
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=<имя_бд>
POSTGRES_DB=<имя_создаваемой_бд>
POSTGRES_USER=<имя_пользователя>
POSTGRES_PASSWORD=<пароль>
DB_HOST=db
DB_PORT=5432
SECRET_KEY=<SECRET_KEY_вашего_проекта>
```

Шаг 2. Выполните команды (при локальном запуске из папки infra/)  
```
docker-compose up -d  
docker-compose exec backend python manage.py migrate  
docker-compose exec backend python manage.py createsuperuser  
docker-compose exec backend python manage.py collectstatic --no-input
```  

Всё! Проект доступен на локалхосте, документацию можно посмотреть по
адресу http://localhost/api/docs/
## Запуск на виртуальной машине
Установите на виртуальную машину Docker и Docker Compose  
```
sudo apt install docker.io
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
Настройте пермишен для Docker Compose

`sudo chmod +x /usr/local/bin/docker-compose`

Скопируйте на сервер файлы с локальной машины  
`scp docker-compose.yml <user>@<server_ip>:/home/<user>/`  
`scp nginx.conf <user>@<server_ip>:/home/<user>/`

Создайте на сервере папку foodgram_docs и скопируйте в неё содержимое папки docs

Выполните шаги 1 и 2 выше.  
Готово! Главная страница проекта должна работать по адресу http://<server_ip>/recipes

## Примеры запросов к API и доступные эндпоинты

`POST auth/token/login/` — получить токен авторизации

`GET recipes/` — получить список рецептов  
`POST recipes/` — создать рецепт  
`GET recipes/{id}/` — получить рецепт по id

`POST users/` — создать пользователя  
`GET users/` — получить список пользователей  
`GET users/{id}/` — получить пользователя по id

Полную документацию API можно посмотреть по урлу api/docs/

API by [Alexei Kadaner](https://github.com/Oxiplegatz)
