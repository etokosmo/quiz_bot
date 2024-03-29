# Бот-викторина для VK и Telegram

## Цели проекта

* Сделать кнопочное меню
* Подключить базу данных Redis
* Анализировать ответы пользователей

## Пример работы программы
Пример результата для Telegram:

Реальный [пример бота tg](https://t.me/etokosmo1337_bot):


![Пример результата для Telegram](https://dvmn.org/filer/canonical/1569215494/324/)

Пример результата для ВКонтакте:

Реальный [пример бота vk](https://vk.com/im?media=&sel=-165088738): 


![Пример результата для ВКонтакте](https://dvmn.org/filer/canonical/1569215498/325/)

## Конфигурации

* Python version: 3.8.5
* Libraries: requirements.txt

## Запуск

- Скачайте код
- Через консоль в директории с кодом установите виртуальное окружение командой:

```bash
python3 -m venv env
```

- Активируйте виртуальное окружение командой:
```bash
source env/bin/activate
```

- Установите библиотеки командой:
```bash
pip install -r requirements.txt
```

- Запишите переменные окружения в файле `.env` в формате КЛЮЧ=ЗНАЧЕНИЕ


`TELEGRAM_API_TOKEN` Токен Телеграмма. Получить можно у [BotFather](https://telegram.me/BotFather).

`TELEGRAM_CHAT_ID` ID чата в телеграм, куда будут приходить возникшие ошибки бота

`VK_API_TOKEN` API токен группы Вконтакте. Получить можно в настройках группы во вкладке "Работа с API".

`REDIS_ADDRESS` Адрес базы данных redis

`REDIS_PORT` Порт базы данных redis

`REDIS_PASSWORD` Пароль базы данных redis

- Для создания базы данных с вопросами введите команду:
```bash
python3 redis_tools.py
```

- Для запуска бота в Телеграм запустите скрипт командой:
```bash
python3 quiz_tg_bot.py
```
- Для запуска бота во Вконтакте запустите скрипт командой:
```bash
python3 quiz_vk_bot.py
```

## Деплой
Деплой можно осуществить на [heroku](https://id.heroku.com/login).

Для этого там необходимо: 
* Зарегестировать аккаунт и создать приложение. 
* Интегрировать код из собственного репозитория на GitHub.
* В репозитории необходим файл `Procfile` в котором прописано:
```bash
quiz_vk: python3 quiz_vk_bot.py
quiz_tg: python3 quiz_tg_bot.py
```
* В `Resources` активировать ботов.
* Во вкладке `Settings` -> `Config Vars` прописать переменные окружения из `.env`.
* Для удобства отслеживания логов можно установить `Heroku CLI`.
* Для подключения приложения в `CLI` прописать в корне проекта
```bash
heroku login
heroku git:remote -a app_name
heroku logs --tail
```
