import os
from django.contrib.auth.models import User

def create_superuser():

    username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
    email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
    password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

    if username and password:

        if not User.objects.filter(username=username).exists():

            print("Criando superuser automaticamente...")

            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )

        else:
            print("Superuser já existe.")