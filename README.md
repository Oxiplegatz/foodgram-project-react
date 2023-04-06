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

Проект доступен по адресу http://159.223.14.232/recipes

## Как работать с репозиторием
Клонировать репозиторий на локальную машину  
`git clone https://github.com/oxiplegatz/foodgram-project-react.git`

Для того чтобы развернуть проект локально, необходимо установить Docker
и Python.   
При локальной сборке нужно поменять адрес расположения документации
в файле docker-compose на  

`- ../docs/:/usr/share/nginx/html/api/docs/`

Затем из папки infra/ выполните команды  
```
docker-compose up -d  
docker-compose exec backend python manage.py migrate  
docker-compose exec backend python manage.py createsuperuser  
docker-compose exec backend python manage.py collectstatic --no-input
```  

Всё! Проект доступен на локалхосте, документацию можно посмотреть по
адресу http://127.0.0.1/api/docs/
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

Затем выполните команды  
```
docker-compose up -d  
docker-compose exec backend python manage.py migrate  
docker-compose exec backend python manage.py createsuperuser  
docker-compose exec backend python manage.py collectstatic --no-input
```  

Готово!