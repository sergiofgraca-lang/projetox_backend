from django.db import models


class Cliente(models.Model):

    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)

    endereco = models.CharField(max_length=200, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)
    cep = models.CharField(max_length=10, blank=True, null=True)

    data_nascimento = models.DateField(blank=True, null=True)

    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome