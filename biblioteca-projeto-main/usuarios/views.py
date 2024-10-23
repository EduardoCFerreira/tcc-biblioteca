from django.urls import reverse
from django.http import Http404
from django.shortcuts import redirect, render

from usuarios.forms.livro_edit_form import AuthorLivroForm
from usuarios.forms.livro_adicionar_form import BookCreate
from usuarios.forms.categoria_adicionar_form import CategoriaCreate
from usuarios.forms.categoria_editar_form import CategoriaEditar
from usuarios.forms.autor_adicionar import AuthorCreate
from usuarios.forms.autor_editar import AuthorEditar
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from bibliotech.models import Emprestimo, Author, Category, Book


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'usuarios/pages/register_view.html',{
        'form': form,
        'form_action': reverse("usuarios:create"),
        })

def register_create(request):
    if not request.POST:
        raise Http404()
    
    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        data = form.save(commit=False)
        data.set_password(data.password)
        data.save()
        messages.success(request, 'Seu usuario foi criado, por favor faça login')

        del(request.session['register_form_data'])
        return redirect('usuarios:login')
        
    return redirect('usuarios:register')

def login_view(request):
    form = LoginForm()
    return render(request, 'usuarios/pages/login.html', {
        'form': form,
        'form_action': reverse('usuarios:login_create')
    })

def login_create(request):
    if not request.POST:
        raise Http404()
    
    form = LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            messages.success(request, 'Você está logado')
            login(request, authenticated_user)
        else:
            messages.error(request, 'Nome ou senha errados')
    else:
        messages.error(request, 'Erro de validação')

    return redirect(reverse('usuarios:emprestimo'))

@login_required(login_url='usuarios:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        return redirect(reverse('usuarios:login'))
    
    if request.POST.get('username') != request.user.username:
        return redirect(reverse('usuarios:login'))
    
    logout(request)
    return redirect(reverse('usuarios:login'))


@login_required(login_url='usuarios:login', redirect_field_name='next')
def emprestimo(request):
    emprestimos = Emprestimo.objects.filter(
        emprestado=True,
        user=request.user,
    )
    return render(request, 'usuarios/pages/emprestimo.html', context={
       'livros': emprestimos,
    })

@login_required(login_url='usuarios:login', redirect_field_name='next')
def livro_editar_detalhe(request):
    livro = Book.objects.all()
    
    return render(request, 'usuarios/pages/livro_editar_detalhe.html', context={
         'livros': livro,
    })

@login_required(login_url='usuarios:login', redirect_field_name='next')
def livro_editar(request, id):
    livro = Book.objects.filter(
        emprestado=False,
        pk = id
    ).first()

    
    form = AuthorLivroForm(
        request.POST or None,
        files=request.FILES or None,
        instance=livro
    )

    if form.is_valid():
        livro = form.save(commit=False)

        livro.auhor = request.user
        livro.emprestado = False

        livro.save()

        messages.success(request, 'Seu livro foi salvo com sucesso!')
        return redirect(reverse('livros:home'))
    
    return render(request, 'usuarios/pages/livro_editar.html', context={
        'form': form
    })

@login_required(login_url='usuarios:login', redirect_field_name='next')
def livro_adicionar(request):

    if request.user.is_staff != True:
        return redirect(reverse('usuarios:emprestimo'))

    form = BookCreate(
        request.POST or None,
        files=request.FILES or None,
    )

    if form.is_valid():
        livro = form.save(commit=False)

        livro.author = request.user
        livro.emprestado = False

        livro.save()

        messages.success(request, 'Seu livro foi salvo com sucesso!')
        return redirect(reverse('livros:home'))
    
    return render(request, 'usuarios/pages/livro_editar.html', context={
        'form': form
    })

@login_required(login_url='usuarios:login', redirect_field_name='next')
def categoria_adicionar(request):

    if request.user.is_staff != True:
        return redirect(reverse('usuarios:emprestimo'))

    form = CategoriaCreate(
        request.POST or None,
    )

    if form.is_valid():
        categoria = form.save(commit=False)

        categoria.author = request.user

        categoria.save()

        messages.success(request, 'Sua categoria foi criada com sucesso!')
        return redirect(reverse('livros:home'))
    
    return render(request, 'usuarios/pages/categoria_adicionar.html', context={
        'form': form
    })
@login_required(login_url='usuarios:login', redirect_field_name='next')
def categoria_editar_detalhe(request):
    categoria = Category.objects.all()

    return render(request, 'usuarios/pages/categoria_editar_detalhe.html', context={
        'categorias': categoria,
    })

@login_required(login_url='usuarios:login', redirect_field_name='next')
def categoria_editar(request, id):
    categoria = Category.objects.filter(
        pk = id
    ).first()

    form = CategoriaEditar(
        request.POST or None,
        instance=categoria
    )

    if form.is_valid():
        categoria = form.save(commit=False)

        categoria.author = request.user

        categoria.save()

        messages.success(request, 'Sua categoria foi salva com sucesso!')
        return redirect(reverse('livros:home'))

    return render(request, 'usuarios/pages/categoria_editar.html', context={
        'form': form
    })

@login_required(login_url='usuarios:login', redirect_field_name='next')
def autor_adicionar(request):

    if request.user.is_staff != True:
        return redirect(reverse('usuarios:emprestimo'))
    
    form = AuthorCreate(
        request.POST or None,
    )

    if form.is_valid():
        autor = form.save(commit=False)

        autor.author = request.user

        autor.save()

        messages.success(request, 'Seu autor foi salvo com sucesso!')
        return redirect(reverse('livros:home'))
    
    return render(request, 'usuarios/pages/autor_adicionar.html', context={
        'form': form
    })

@login_required(login_url='usuarios:login', redirect_field_name='next')
def autor_editar_detalhe(request):
    autor = Author.objects.all()

    return render(request, 'usuarios/pages/autor_editar_detalhe.html', context={
         'autores': autor,
    })

@login_required(login_url='usuarios:login', redirect_field_name='next')
def autor_editar(request, id):
    autor = Author.objects.filter(
        pk = id
    ).first()

    form = AuthorEditar(
        request.POST or None,
        instance=autor
    )

    if form.is_valid():
        autor = form.save(commit=False)

        autor.autor = request.user

        autor.save()

        messages.success(request, 'Seu autor foi salvo com sucesso!')
        return redirect(reverse('livros:home'))
    
    return render(request, 'usuarios/pages/autor_editar.html', context={
        'form': form
    })