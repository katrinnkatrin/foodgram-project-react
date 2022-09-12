[![Django-app workflow](https://github.com/katrinnkatrin/foodgram-project-react/actions/workflows/main.yml/badge.svg)]

## Описание:

«Продуктовый помощник».
На этом сайте пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, 
добавлять понравившиеся рецепты в «Избранное», а так же скачивать список продуктов, необходимых для приготовления выбранных блюд.

## Запуск проекта в Docker контейнере
- Склонировать репозиторий на локальную машину:
git clone https://github.com/katrinnkatrin/foodgram-project-react.git
cd foodgram-project-react

- Cоздать и активировать виртуальное окружение:
python -m venv venv
source venv/Scripts/activate

- Cоздать файл .env в директории /infra/ с содержанием:
SECRET_KEY=секретный ключ django
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

- Установить Docker:
(https://www.docker.com/products/docker-desktop/)
Параметры запуска описаны в файлах docker-compose.yml и nginx.conf которые находятся в директории infra/.

- Запустить docker compose из директории infra:
docker-compose up -d --build

После сборки появляются 4 контейнера:
  * контейнер базы данных db
  * контейнер приложения backend - web
  * контейнер приложения frontend
  * контейнер web-сервера nginx

Сделать миграции
python3 manage.py makemigrations && \ 
    python3 manage.py migrate --noinput && \
    
python3 manage.py collectstatic --noinput

- Создать суперпользователя:
docker compose exec web python manage.py createsuperuser

- При первом запуске заполнить БД подготовленными данными:
docker-compose exec web python manage.py load_ingrs
docker-compose exec web python manage.py load_tags

***
## Проект будет доступен по ссылкам:

Приложение - http://localhost/

Redoc - http://localhost/api/docs/

Админка - http://localhost/admin/
