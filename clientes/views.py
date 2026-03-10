from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente
from .forms import ClienteForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
import os


# --- CRIA SUPERUSER AUTOMATICAMENTE ---
def create_superuser():
    username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
    email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
    password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

    if username and password:
        if not User.objects.filter(username=username).exists():
            print("Criando superuser automaticamente...")
            User.objects.create_superuser(username=username, email=email, password=password)
        else:
            print("Superuser já existe.")

create_superuser()

# --- LOGIN ---
def login_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('lista_clientes')
            else:
                return redirect('cadastrar_cliente')
        else:
            return render(request, 'clientes/login.html', {
                'erro': 'Usuário ou senha inválidos'
            })

    return render(request, 'clientes/login.html')


# --- LOGOUT ---
@login_required(login_url='login')
def logout_usuario(request):
    logout(request)
    return redirect('login')


# --- LISTA DE CLIENTES (SOMENTE ADMIN) ---
@login_required(login_url='login')
def lista_clientes(request):
    if not request.user.is_staff:
        return redirect('cadastrar_cliente')

    busca = request.GET.get('busca')
    clientes = Cliente.objects.filter(nome__icontains=busca) if busca else Cliente.objects.all()
    total_clientes = clientes.count()

    return render(request, 'clientes/lista_clientes.html', {
        'clientes': clientes,
        'total_clientes': total_clientes
    })


# --- CADASTRAR CLIENTE (TODOS OS USUÁRIOS LOGADOS) ---
@login_required(login_url='login')
def cadastrar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente cadastrado com sucesso!")
            return redirect('lista_clientes') if request.user.is_staff else redirect('cadastrar_cliente')
    else:
        form = ClienteForm()
    return render(request, 'clientes/cadastrar_cliente.html', {'form': form})


# --- EDITAR CLIENTE (SOMENTE ADMIN) ---
@login_required(login_url='login')
def editar_cliente(request, id):
    if not request.user.is_staff:
        return redirect('cadastrar_cliente')

    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'clientes/form_cliente.html', {'form': form, 'cliente': cliente})


# --- EXCLUIR CLIENTE (SOMENTE ADMIN) ---
@login_required(login_url='login')
def excluir_cliente(request, id):
    if not request.user.is_staff:
        return redirect('cadastrar_cliente')

    cliente = get_object_or_404(Cliente, id=id)
    cliente.delete()
    return redirect('lista_clientes')