from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente
from .forms import ClienteForm

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.shortcuts import render

from django.contrib.auth.decorators import login_required






# LOGIN
def login_usuario(request):

    if request.user.is_authenticated:
        return redirect('lista_clientes')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('lista_clientes')
        else:
            messages.error(request, "Usuário ou senha inválidos")

    return render(request, 'clientes/login.html')


# LOGOUT
@login_required(login_url='login')
def logout_usuario(request):

    logout(request)
    messages.success(request, "Logout realizado com sucesso.")

    return redirect('login')


# LISTA CLIENTES


from django.shortcuts import render
from .models import Cliente
from django.contrib.auth.decorators import login_required

@login_required
def lista_clientes(request):
    busca = request.GET.get('busca')

    if busca:
        clientes = Cliente.objects.filter(nome__icontains=busca)
    else:
        clientes = Cliente.objects.all()

    total_clientes = clientes.count()

    context = {
        'clientes': clientes,
        'total_clientes': total_clientes
    }

    return render(request, 'clientes/lista_clientes.html', context)


# CADASTRAR CLIENTE
def cadastrar_cliente(request):

    if request.method == 'POST':

        form = ClienteForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Cliente cadastrado com sucesso!")
            return redirect('lista_clientes')

    else:

        form = ClienteForm()

    return render(request, 'clientes/form_cliente.html', {'form': form})


# EDITAR CLIENTE
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
@login_required(login_url='login')
@permission_required('clientes.delete_cliente', raise_exception=True)
def excluir_cliente(request, id):

    cliente = get_object_or_404(Cliente, id=id)

    if request.method == "POST":

        cliente.delete()

        messages.success(request, "Cliente excluído com sucesso!")

        return redirect('lista_clientes')

    return render(request, 'clientes/confirmar_exclusao.html', {
        'cliente': cliente
    })