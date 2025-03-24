# Auth System with JWT, Redis, RBAC

## Описание

В проекте реализована система аутентификации и авторизации пользователей с использованием:

- **FastAPI** как основного web-фреймворка.
- **JWT (JSON Web Token)** для токен-базированной аутентификации.
- **Redis** для хранения валидных и отозванных токенов (whitelist/blacklist).
- **Role-Based Access Control (RBAC)** для разграничения доступа к контенту.
- Минимальный **фронт на Jinja2 + Tailwind CSS** для тестирования работы системы.

---

## Основной функционал

1. **Аутентификация:**
   - Пользователь выполняет вход через форму логина.
   - После логина сервер генерирует JWT токен с username, ролью и временем жизни.
   - Токен добавляется в Redis whitelist и сохраняется в cookies браузера.

2. **Авторизация:**
   - Все защищённые эндпоинты проверяют токен:
     - Подпись JWT.
     - Наличие в Redis whitelist.
     - Отсутствие в Redis blacklist.
   - Также проверяется роль пользователя для доступа к определённому контенту.

3. **Разделение контента:**
   - **Общий контент** отображается для всех авторизованных пользователей.
   - **Admin Panel** — доступен только для роли `admin`.
   - **User Dashboard** — доступен только для роли `user`.

4. **Logout:**
   - При выходе токен удаляется из whitelist и добавляется в blacklist, немедленно отзывая его.

5. **Debug-страница:**
   - Позволяет вручную сгенерировать токен с нужной ролью и проверить работу системы.

---



##  Быстрый запуск и тестирование

### Сборка и запуск:
### 1️⃣ Создание `.env` файла

Перед запуском необходимо создать файл `.env` в корне проекта. Пример содержимого:

```env
SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
REDIS_HOST=redis
REDIS_PORT=6379
```
Файл .env.example приведён в проекте — можно использовать его как шаблон.

```bash
  docker-compose up --build
```
## Доступ к приложению:
Приложение будет доступно по адресу: http://localhost:8000


## 🌐 Доступные страницы

| URL                 | Метод    | Описание                                                                                     | Доступ                              |
|--------------------|---------|--------------------------------------------------------------------------------------------|-------------------------------------|
| `/login/`           | GET/POST | Форма логина. Ввод username и выбор роли.                                                    | Доступна всем                       |
| `/content/`         | GET      | Контент с разделением: общий блок + контент по роли.                                         | Только авторизованным пользователям |
| `/logout/`          | POST     | Выход из системы. Удаляет токен из whitelist, добавляет в blacklist.                         | Только авторизованным пользователям |
| `/debug/`           | GET/POST | Debug-страница для ручного добавления токенов с нужной ролью (для тестирования).             | Доступна всем (для теста)           |
| `/admin/block/`     | GET/POST | Страница для блокировки пользователя по username (добавление всех его токенов в blacklist).  | Только для пользователей с ролью admin |
