# API для Yatube
 
## Описание
 
Yatube API — это REST API для платформы блогов Yatube. Проект позволяет пользователям публиковать посты, объединять их в тематические сообщества, оставлять комментарии и подписываться на других авторов.
 
Реализовано:
- **Публикации (Post)** — создание, чтение, изменение и удаление постов; посты можно привязывать к сообществу и прикреплять изображение.
- **Сообщества (Group)** — доступны только на чтение.
- **Комментарии (Comment)** — вложены под конкретным постом, доступны для CRUD.
- **Подписки (Follow)** — подписка на других пользователей и просмотр списка своих подписок с возможностью поиска.
- **Аутентификация по JWT** через Djoser.
- **Права доступа**: чтение — всем, изменение и удаление контента — только автору. Эндпоинт `/follow/` доступен только авторизованным пользователям.
- **Пагинация** списка публикаций (`limit`/`offset`).
## Технологии
 
- Python 3.12.7
- Django 5.1
- Django REST Framework
- Djoser + Simple JWT
- SQLite

## Установка
 
1. Клонировать репозиторий и перейти в него в командной строке:
```bash
git clone https://github.com/<username>/api_final_yatube.git
cd api_final_yatube
```
 
2. Создать и активировать виртуальное окружение:
```bash
python3 -m venv venv
source venv/bin/activate   # для Windows: venv\Scripts\activate
```
 
3. Установить зависимости из файла `requirements.txt`:
```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
 
4. Выполнить миграции:
```bash
python manage.py migrate
```
 
5. (опционально) Создать суперпользователя:
```bash
python manage.py createsuperuser
```
 
6. Запустить проект:
```bash
python manage.py runserver
```
 
После запуска API доступно по адресу: `http://127.0.0.1:8000/api/v1/`
 
## Примеры запросов
 
### Получение JWT-токена
 
```
POST /api/v1/jwt/create/
```
 
Тело запроса:
 
```json
{
  "username": "lisa",
  "password": "your_password"
}
```
 
Ответ:
 
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```
 
### Получение списка публикаций
 
```
GET /api/v1/posts/
```
 
Ответ:
 
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "author": "lisa",
      "text": "Первый пост",
      "pub_date": "2026-08-10T12:00:00Z",
      "image": null,
      "group": null
    }
  ]
}
```
 
### Создание публикации
 
```
POST /api/v1/posts/
Authorization: Bearer <access_token>
```
 
Тело запроса:
 
```json
{
  "text": "Новый пост",
  "group": 1
}
```
 
### Добавление комментария к публикации
 
```
POST /api/v1/posts/1/comments/
Authorization: Bearer <access_token>
```
 
Тело запроса:
 
```json
{
  "text": "Отличный пост!"
}
```
 
### Подписка на пользователя
 
```
POST /api/v1/follow/
Authorization: Bearer <access_token>
```
 
Тело запроса:
 
```json
{
  "following": "some_username"
}
```