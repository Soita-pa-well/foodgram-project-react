## О проекте:
Дипломная работа ЯП по специальности Python разработчик. Сайт Foodgram представляет собой сервис для любителей кулинарии, где пользователи могут публиковать и обмениваться рецептами блюд, подписываться на понравившиеся публикации других пользователей и добавлять их в Избранное. На сервисе реализована возможность скачать в формате PDF список тех ингедиетов, которые будут необходимы для приготовления выбранного блюда.
- ### Адрес проекта: https://soitafoodgramm.ddns.net/
- ### Для входа в админку:
  - email : soita.pavel@yandex.ru
  - password : gfhjkmxbr

## Запуск проекта:
для того, чтобы локально запустить проект необходимо:

клонировать проект
```bash
git clone git@github.com:Soita-pa-well/foodgram-project-react.git
```
Cоздать и активировать виртуальное окружение:
#### для Windows:
```bash
python -m venv venv
source venv/Scripts/activate
```
#### для Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

Установить зависимости:
```bash
pip install -r requirements.txt
```

 Перейти в директорию infra:
 ```bash
cd infra
```

Запустить контейнеры: 

```bash
docker-compose up -d
```

Собрать и запустить миграции:
```bash
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
```
## Используемый стек:

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)

#### Автор 
Сойта Павел


