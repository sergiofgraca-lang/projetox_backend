from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
import os
from .models import Visita

ARQUIVO = "contador.txt"

def contar_visitas(request):
    visita, created = Visita.objects.get_or_create(id=1)

    visita.total += 1
    visita.save()

    return JsonResponse({"total": visita.total})