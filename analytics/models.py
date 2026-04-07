from django.db import models

class Visita(models.Model):
    total = models.IntegerField(default=0)

    def __str__(self):
        return f"Visitas: {self.total}"
