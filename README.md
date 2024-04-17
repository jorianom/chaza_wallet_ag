
## installs
pip install django\
pip install graphene-django\
pip install requests
python -m pip install pika --upgrade

## start -> python manage.py runserver
## [python manage.py runserver] (http://127.0.0.1:/graphql)
## examples:
```
{
  externalData2(id: 1){
    name
    id
  }
}
-----
{
  externalData{
    name
  }
}
```
python -m venv venv f1 select interpreter

pip install django

django-admin startproject core  .

python manage.py startapp microserves

add microserves to core/settings.py -> INSTALLED_APPS

python manage.py makemigrations -> add models

pip install graphene-django
