from django.urls import path
from .views import contar_visitas, pagina_visitas

urlpatterns = [
    path('visitas/', contar_visitas),
    path('dashboard/', pagina_visitas, name='dashboard_visitas'),
]