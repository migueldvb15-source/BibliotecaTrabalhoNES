from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q
from .models import Autor, Livro, Emprestimo
from .forms import AutorForm, LivroForm, EmprestimoForm
from django.contrib.admin.views.decorators import staff_member_required

# --- AUTENTICAÇÃO (RF01) ---
def cadastro_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, "Cadastro realizado com sucesso! Bem-vindo ao BiblioFácil.")
            return redirect('biblidoaluno:home')
        else:
            messages.error(request, "Erro no cadastro. Verifique as regras de senha e tente novamente.")
    else:
        form = UserCreationForm()
    return render(request, 'biblidoaluno/cadastro.html', {'form': form})

# --- LISTAGEM, PESQUISA E CONSULTAS ORM (RF04 / RF09) ---
def home_view(request):
    busca = request.GET.get('busca', '')
    
    # select_related otimiza a consulta trazendo o Autor junto com o Livro
    livros = Livro.objects.select_related('autor').all()
    
    if busca:
        livros = livros.filter(
            Q(titulo__icontains=busca) | Q(autor__nome__icontains=busca) | Q(categoria__icontains=busca)
        )

    # Uso explícito de exclude() exigido no edital
    livros_disponiveis_count = Livro.objects.exclude(disponivel=False).count()
    emprestimos_ativos = Emprestimo.objects.select_related('livro').filter(devolvido=False)

    return render(request, "biblidoaluno/home.html", {
        "livros": livros,
        "emprestimos_ativos": emprestimos_ativos,
        "livros_disponiveis_count": livros_disponiveis_count,
        "busca": busca,
    })

def detalhe_livro(request, pk):
    livro = get_object_or_404(Livro.objects.select_related('autor'), pk=pk)
    return render(request, 'biblidoaluno/detalhe.html', {'livro': livro})

def listar_por_categoria(request, nome_categoria):
    livros_filtrados = Livro.objects.select_related('autor').filter(categoria__iexact=nome_categoria)
    return render(request, 'biblidoaluno/lista_categoria.html', {
        'nome_categoria': nome_categoria,
        'livros': livros_filtrados
    })

# --- CRUD PROTEGIDO POR LOGIN (RF02 / RF08) ---
@staff_member_required
def cadastrar_autor(request):
    if request.method == 'POST':
        form = AutorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Autor cadastrado com sucesso!")
            return redirect('biblidoaluno:cadastrar_livro')
    else:
        form = AutorForm()
    return render(request, 'biblidoaluno/form_generico.html', {'form': form, 'titulo_pagina': 'Cadastrar Novo Autor'})

@staff_member_required
def cadastrar_livro(request):
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Livro adicionado ao acervo!")
            return redirect('biblidoaluno:home')
        else:
            messages.error(request, "Verifique os erros no formulário.")
    else:
        form = LivroForm()
    return render(request, 'biblidoaluno/form_generico.html', {'form': form, 'titulo_pagina': 'Cadastrar Novo Livro'})

@staff_member_required
def editar_livro(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    if request.method == 'POST':
        form = LivroForm(request.POST, instance=livro)
        if form.is_valid():
            form.save()
            messages.success(request, f"O livro '{livro.titulo}' foi atualizado!")
            return redirect('biblidoaluno:home')
    else:
        form = LivroForm(instance=livro)
    return render(request, 'biblidoaluno/form_generico.html', {'form': form, 'titulo_pagina': f'Editar: {livro.titulo}'})

@staff_member_required
def excluir_livro(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    if request.method == 'POST':
        titulo = livro.titulo
        livro.delete()
        messages.success(request, f"Livro '{titulo}' removido do sistema.")
        return redirect('biblidoaluno:home')
    return render(request, 'biblidoaluno/confirmar_exclusao.html', {'livro': livro})

@login_required
def registrar_emprestimo(request):
    if request.method == 'POST':
        form = EmprestimoForm(request.POST)
        if form.is_valid():
            emprestimo = form.save(commit=False)
            emprestimo.registrado_por = request.user
            emprestimo.save()
            
            livro = emprestimo.livro
            livro.disponivel = False
            livro.save()
            messages.success(request, f"Empréstimo de '{livro.titulo}' registrado para {emprestimo.nome_aluno}!")
            return redirect('biblidoaluno:home')
    else:
        form = EmprestimoForm()
    return render(request, 'biblidoaluno/form_generico.html', {'form': form, 'titulo_pagina': 'Registrar Empréstimo'})

@login_required
def devolver_livro(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    if request.method == 'POST' and not emprestimo.devolvido:
        emprestimo.devolvido = True
        emprestimo.save()
        
        livro = emprestimo.livro
        livro.disponivel = True
        livro.save()
        messages.success(request, f"Devolução de '{livro.titulo}' confirmada!")
    return redirect('biblidoaluno:home')