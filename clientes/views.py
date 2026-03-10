from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente
from .forms import ClienteForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

def criar_admin():
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(
            "admin",
            "admin@email.com",
            "admin123"
        )

criar_admin()

# LOGIN DO SISTEMA
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


# LOGOUT
@login_required
def logout_usuario(request):

    logout(request)

    return redirect('login')


# LISTA DE CLIENTES (somente logado)
@login_required(login_url='login')
def lista_clientes(request):

    if not request.user.is_staff:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("Acesso permitido apenas para administrador.")

    busca = request.GET.get('busca')

    if busca:
        clientes = Cliente.objects.filter(nome__icontains=busca)
    else:
        clientes = Cliente.objects.all()

    # CONTAGEM DE CLIENTES
    total_clientes = Cliente.objects.count()

    return render(request, 'clientes/lista_clientes.html', {
        'clientes': clientes,
        'total_clientes': total_clientes
    })

# CADASTRAR CLIENTE
@login_required(login_url='login')
def cadastrar_cliente(request):

    if request.method == 'POST':

        form = ClienteForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, "Cliente cadastrado com sucesso!")

            if request.user.is_staff:
                return redirect('lista_clientes')
            else:
                return redirect('cadastrar_cliente')

    else:
        form = ClienteForm()

    return render(request, 'clientes/cadastrar_cliente.html', {
        'form': form
    })

# EDITAR CLIENTE
@login_required(login_url='login')
def editar_cliente(request, id):

    cliente = get_object_or_404(Cliente, id=id)

    if request.method == 'POST':

        form = ClienteForm(request.POST, instance=cliente)

        if form.is_valid():
            form.save()
            return redirect('lista_clientes')

    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'clientes/form_cliente.html', {
        'form': form,
        'cliente': cliente
    })


# EXCLUIR CLIENTE
@login_required(login_url='login')
def excluir_cliente(request, id):

    cliente = get_object_or_404(Cliente, id=id)

    cliente.delete()

    return redirect('lista_clientes')