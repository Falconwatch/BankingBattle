# Платформа BankingBattle
### Описание
На платформе можно примерить роль банка и сразиться за клиентов.
### Технологии
Python 3.7
Django 3.2
### Запуск проекта в dev-режиме
1) Установите и активируйте виртуальное окружение, например вот так (linux/mac):
``` 
python3 -m venv path/to/myvenv
source path/to/myvenv/bin/activate
``` 

2) Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
``` 

3) Задайте значение переменной среды SECRET_KEY:
```
export SECRET_KEY=mysecretkey
``` 

4) Для разворачивания БД выполните команды в папке с файлом manage.py :
```
python3 manage.py makemigrations 
python3 manage.py migrate
```

5) Для создания Superuser папке с файлом manage.py выполните команду:
```
python3 manage.py createsuperuser 
```

6) Для запуска сервиса папке с файлом manage.py выполните команду:
```
python3 manage.py runserver
```