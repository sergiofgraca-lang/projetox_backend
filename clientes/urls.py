from django.urls import path
from . import views

urlpatterns = [

    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),

    path('lista/', views.lista_clientes, name='lista_clientes'),
    path('cadastrar/', views.cadastrar_cliente, name='cadastrar_cliente'),

    path('editar/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('excluir/<int:id>/', views.excluir_cliente, name='excluir_cliente'),
]