# Платформа BankingBattle
### Описание
На платформе можно примерить роль банка и сразиться за клиентов.
### Технологии
Python 3.7
Django 3.2
Docker
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

6) Для запуска сервиса через gunicorn запустите скрипт start-server.sh
```
./start_server.sh
```

7) Для запуска сервиса папке с файлом manage.py выполните команду:
```
python3 manage.py runserver
```

8) Для сбора Docker образа выполните команду
```
docker build -t banking_battle .   
```

9) Для запуска Docker контейнера выполните команду
```
docker run -it -p 8020:8020 \                     
     -e DJANGO_SUPERUSER_USERNAME=admin \
     -e DJANGO_SUPERUSER_PASSWORD=Example_password \
     -e DJANGO_SUPERUSER_EMAIL=admin@example.com \
     banking_battle
```
Сервис запустится на 8020 порту. Будет создан пользователь с правами админа с именем admin и паролем Example_password