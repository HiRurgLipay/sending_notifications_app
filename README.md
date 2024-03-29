
# Руководство по запуску

Для запуска проекта необходимо выполнить следующие шаги:

* **Настройка виртуального окружения и установка зависимостей:**

  * ``poetry shell``
  * ``poetry install``
* **Запуск сервиса Redis:**
  Для запуска сервиса Redis в зависимости от вашей операционной системы:

  * **Linux:**
    * ``sudo systemctl start redis``
  * **MacOS:**
    * ``brew services start redis``
  * **Windows**:
    * Запустите сервер Redis через менеджер служб Windows или используйте WSL для запуска Redis на Linux.
* **Создание базы данных:**
  Убедитесь, что у вас настроена и запущена база данных PostgreSQL. Создайте базу данных и укажите ее параметры в файле `.env`.
* **Настройка файла `.env`:**
  Скопируйте файл `.env.template` и переименуйте его в `.env`. Внесите необходимые параметры, такие как настройки базы данных, url сервера Редис, уровень логирования и JWT-токен доступа к внешнему api.
* **Запуск Django проекта:**
  После выполнения предыдущих шагов можно запустить Django проект:

  Эта команда запустит сервер разработки Django на локальном хосте по адресу `http://127.0.0.1:8000/`.
* Запуск Воркера Celery:
  ``celery -A sending_notifications_app worker``

## Описание бизнес логики

Проект содержит следующие сервисы для работы с данными:

### Сервис рассылок (`core.services.mailing_service`)

* `create_mailing_service` Создает новую рассылку на основе предоставленных данных. Если время начала рассылки наступило, запускает задачу по отправке сообщений.
* `update_mailing_service` Обновляет информацию о рассылке по ее идентификатору.
* `delete_mailing_service` Удаляет рассылку по ее идентификатору.

### Сервис клиентов (`core.services.client_service`)

* `create_client_service` Создает нового клиента на основе предоставленных данных.
* `update_client_service` Обновляет информацию о клиенте по его идентификатору.
* `delete_client_service `Удаляет клиента по его идентификатору.

### Статистика рассылок (`core.services.statistics_service`)

* `get_mailing_statistics_service` Возвращает статистику по рассылке (общее количество, количество отправленных, ожидающих отправки и неотправленных сообщений).
* `get_detailed_message_statistics_service(` Возвращает подробную статистику о сообщениях в рамках рассылки.

## Документация по задачам Celery

Файл `tasks.py` содержит задачу Celery для отправки сообщений:

* `send_messages_task` Асинхронная задача для отправки сообщений рассылки. Использует данные о рассылке и клиентах для отправки сообщений и обновления статусов сообщений в базе данных.
