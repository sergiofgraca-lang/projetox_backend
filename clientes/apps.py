from django.apps import AppConfig
from django.db.models.signals import post_migrate

class ClientesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clientes'

    def ready(self):
        """Cria superuser automaticamente após migrações, se não existir."""
        from django.contrib.auth.models import User
        from django.conf import settings

        def criar_superusuario(sender, **kwargs):
            # Pega variáveis de ambiente, ou usa valores padrão
            username = getattr(settings, "DJANGO_SUPERUSER_USERNAME", "admin")
            email = getattr(settings, "DJANGO_SUPERUSER_EMAIL", "admin@example.com")
            password = getattr(settings, "DJANGO_SUPERUSER_PASSWORD", "admin123")

            # Só cria se não existir
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(username=username, email=email, password=password)
                print(f"Superuser '{username}' criado com sucesso!")

        # Conecta ao sinal post_migrate, garantindo que os apps estão prontos
        post_migrate.connect(criar_superusuario, sender=self)