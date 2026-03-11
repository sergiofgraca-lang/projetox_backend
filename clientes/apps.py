from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.auth.models import User
import os

class ClientesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clientes'

    def ready(self):
        post_migrate.connect(create_admin_user, sender=self)

def create_admin_user(sender, **kwargs):
    username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
    email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@email.com")
    password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "senha123")

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f"Superuser '{username}' criado automaticamente.")