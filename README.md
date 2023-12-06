# Linux_BackUP_service

Telegram - бот который выполняет копирование файла по команде пользователя . 
### Стек технологий

- python-telegram-bot
- python

### Установка

клонировать репозиторий 
```Bash
git clone https://github.com/femakc/Linux_BackUP_service
```
Активировать виртуальное окружение 
```Bfsh
python -m venv venv
```

Установить зависимости 
```Bash
pip install -r requirements.txt
```

В корне проекта создать файл **.env**
```Bash
TELEGRAM_TOKEN = token
TELEGRAM_CHAT_ID = chat_id
SRC_PATH = path_from
DSC_PATH = path_to
```

Запустить скрипт 

```Bash
python -m main
```
