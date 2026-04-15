from django.urls import path
from .views import contar_visitas

urlpatterns = [
    path('visitas/', contar_visitas),
]

from .views import pagina_visitas

urlpatterns = [
    path("dashboard/", pagina_visitas, name="dashboard_visitas"),
]