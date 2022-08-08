# Платформа BankingBattle
### Описание
На платформе можно примерить роль банка и сразиться за клиентов.
### Технологии
Python 3.7
Django 3.2
### Запуск проекта в dev-режиме
- Установите и активируйте виртуальное окружение
- Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
``` 
- Для разворачивания БД выполните команды в папке с файлом manage.py :
```
python3 manage.py makemigrations 
python3 manage.py migrate
```

- Для создания Superuser папке с файлом manage.py выполните команду:
```
python3 manage.py createsuperuser 
```

- Для запуска сервиса папке с файлом manage.py выполните команду:
```
python3 manage.py runserver
```