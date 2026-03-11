from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente
from .forms import ClienteForm

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# LOGIN
def login_usuario(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if user.has_perm('clientes.view_cliente'):
                return redirect('lista_clientes')
            else:
                return redirect('cadastrar_cliente')

        return render(request, 'clientes/login.html', {
            'erro': 'Usuário ou senha inválidos'
        })

    return render(request, 'clientes/login.html')


# LOGOUT
@login_required(login_url='login')
def logout_usuario(request):

    logout(request)

    return redirect('login')


# LISTA CLIENTES
@login_required
@permission_required('clientes.view_cliente', raise_exception=True)
def lista_clientes(request):

    busca = request.GET.get('busca')

    if busca:
        clientes = Cliente.objects.filter(nome__icontains=busca)
    else:
        clientes = Cliente.objects.all()

    total_clientes = clientes.count()

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

            if request.user.has_perm('clientes.view_cliente'):
                return redirect('lista_clientes')

            return redirect('cadastrar_cliente')

    else:

        form = ClienteForm()

    return render(request, 'clientes/cadastrar_cliente.html', {'form': form})


# EDITAR CLIENTE
@login_required
@permission_required('clientes.change_cliente', raise_exception=True)
def editar_cliente(request, id):

    cliente = get_object_or_404(Cliente, id=id)

    if request.method == 'POST':

        form = ClienteForm(request.POST, instance=cliente)

        if form.is_valid():
            form.save()
            messages.success(request, "Cliente atualizado com sucesso!")
            return redirect('lista_clientes')

    else:

        form = ClienteForm(instance=cliente)

    return render(request, 'clientes/form_cliente.html', {
        'form': form,
        'cliente': cliente
    })


# EXCLUIR CLIENTE
@login_required
@permission_required('clientes.delete_cliente', raise_exception=True)
def excluir_cliente(request, id):

    cliente = get_object_or_404(Cliente, id=id)

    if request.method == "POST":
        cliente.delete()
        messages.success(request, "Cliente excluído com sucesso!")

    return redirect('lista_clientes')