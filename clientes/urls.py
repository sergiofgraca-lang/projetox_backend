from django.urls import path
from . import views

urlpatterns = [
    # LOGIN / LOGOUT
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),

    # LISTA CLIENTES
    path('', views.lista_clientes, name='lista_clientes'),  # rota principal '/' 
    path('lista/', views.lista_clientes, name='lista_clientes'),

    # CADASTRO / EDIÇÃO / EXCLUSÃO
    path('cadastrar/', views.cadastrar_cliente, name='cadastrar_cliente'),
    path('editar/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('excluir/<int:id>/', views.excluir_cliente, name='excluir_cliente'),
]