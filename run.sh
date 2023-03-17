#!/bin/sh
echo "##### НАЧИНАЕМ РАБОТУ #####"
echo "### 1. Собираем статику ###"
sudo docker-compose exec web python3 manage.py collectstatic --no-input
echo "### 2. Выполняем миграции ###"
sudo docker-compose exec web python3 manage.py migrate
echo "??? 3. Будем создавать суперпользователя? ('Д/н' или 'Y/n' ) "
read  yesno
if [ "$yesno" = "д" ] || [ "$yesno" = "y" ] || [ "$yesno" = "" ] || [ "$yesno" = "Y" ] || [ "$yesno" = "Д" ]
then
	echo "### 3. Создаём суперпользователя ###"
	sudo docker-compose exec web python3 manage.py createsuperuser
fi
echo "### 4. Запускаем скрипт получения данных с Гугл Таблиц ###"
sudo docker-compose exec web python3 get_data/main.py
echo "##### РАБОТА ЗАВЕРШЕНА #####"
