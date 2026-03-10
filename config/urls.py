from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def home(request):
    return redirect('/clientes/login/')

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('clientes/', include('clientes.urls')),
]