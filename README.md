# EaglienUS_Russian_bot
Телеграм бот для изучения английского

## Структура репозитория:
- src/main.py - основной файл для работы с ботом
- src/data.py - данные для бота (словарик английских слов)
- src/logger.py - класс для удобного логирования в боте (в консоль и в файл)
- src/setting.py - считывание переменных виртуального окружения
- .env.dist - пример файла .env, для работы с ботом необходимо создать файл .env

## Запуск бота в Docker:
1. Форкните себе репозиторий бота, а затем склонируйте.
2. Заполните данные о боте: создайте файл .env, с полями из .env.dist. Получить токен для бота можно 
у [BotFather](https://t.me/BotFather).

## Запуск бота вручную:
1. Используйте Python 3.7.
2. Форкните себе репозиторий бота, а затем склонируйте.
3. Установите необходимые библиотеки для работы с ботом:  
`pip install -r requirements.txt`


## [П.С: я создавал другой бот](https://github.com/DenisBartos/TelegramBot1.1.5)

Бот создан для облегчения общения людей не говорящих и плохо говорящих. Помогает общаться и вести диалог, преобразуя напечатанные слова в голосовые сообщения с помощью синтезатора речи.
