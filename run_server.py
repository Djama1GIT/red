import os

os.system("python .\\red\\manage.py makemigrations")
os.system("python .\\red\\manage.py migrate")
os.system("python .\\red\\manage.py loaddata dump.json")
os.system("python .\\red\\manage.py runserver 80")
