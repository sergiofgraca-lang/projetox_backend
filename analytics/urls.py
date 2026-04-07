from django.urls import path
from .views import contar_visitas

urlpatterns = [
    path('visitas/', contar_visitas),
]