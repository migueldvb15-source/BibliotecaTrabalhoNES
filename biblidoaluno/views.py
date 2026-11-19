from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Livro, Emprestimo
from .forms import LivroForm, EmprestimoForm

def home_view(request):
    livros = Livro.objects.all()
    emprestimos_ativos = Emprestimo.objects.filter(devolvido=False)
    return render(request, "biblidoaluno/home.html", {
        "livros": livros,
        "emprestimos_ativos": emprestimos_ativos
    })

def detalhe_livro(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    return render(request, 'biblidoaluno/detalhe.html', {'livro': livro})

def listar_por_categoria(request, nome_categoria):
    livros_filtrados = Livro.objects.filter(categoria__iexact=nome_categoria)
    return render(request, 'biblidoaluno/lista_categoria.html', {
        'nome_categoria': nome_categoria,
        'livros': livros_filtrados
    })

# --- NOVAS VIEWS COM DJANGO FORMS E MÉTODO POST ---

def cadastrar_livro(request):
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('biblidoaluno:home')
    else:
        form = LivroForm()
    
    return render(request, 'biblidoaluno/form_livro.html', {'form': form})

def registrar_emprestimo(request):
    if request.method == 'POST':
        form = EmprestimoForm(request.POST)
        if form.is_valid():
            emprestimo = form.save()
            # Marca o livro como indisponível
            livro = emprestimo.livro
            livro.disponivel = False
            livro.save()
            return redirect('biblidoaluno:home')
    else:
        form = EmprestimoForm()

    return render(request, 'biblidoaluno/form_emprestimo.html', {'form': form})

def devolver_livro(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    if request.method == 'POST' and not emprestimo.devolvido:
        emprestimo.devolvido = True
        emprestimo.save()
        
        livro = emprestimo.livro
        livro.disponivel = True
        livro.save()
        
    return redirect('biblidoaluno:home')