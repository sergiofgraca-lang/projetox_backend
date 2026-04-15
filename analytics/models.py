from django.db import models

class Visita(models.Model):
    ip = models.GenericIPAddressField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip} - {self.data}"