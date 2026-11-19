from django import forms
from .models import Livro, Emprestimo

class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'categoria', 'ano_publicacao']
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Ex: Dom Casmurro'}),
            'autor': forms.TextInput(attrs={'placeholder': 'Ex: Machado de Assis'}),
            'categoria': forms.TextInput(attrs={'placeholder': 'Ex: Ficcao, Didatico, Historia'}),
            'ano_publicacao': forms.NumberInput(attrs={'placeholder': 'Ex: 1899'}),
        }

class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['livro', 'nome_aluno', 'matricula_aluno', 'data_devolucao_prevista']
        widgets = {
            'data_devolucao_prevista': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra o campo 'livro' para mostrar APENAS livros disponíveis no formulário
        self.fields['livro'].queryset = Livro.objects.filter(disponivel=True)