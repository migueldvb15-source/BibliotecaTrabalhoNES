from django import forms
from .models import Autor, Livro, Emprestimo

class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['nome', 'nacionalidade']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Machado de Assis'}),
            'nacionalidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Brasileira'}),
        }

class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'categoria', 'ano_publicacao']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'autor': forms.Select(attrs={'class': 'form-select'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control'}),
            'ano_publicacao': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    # RF07: Validação customizada
    def clean_ano_publicacao(self):
        ano = self.cleaned_data.get('ano_publicacao')
        if ano and (ano < 1000 or ano > 2026):
            raise forms.ValidationError("Informe um ano de publicação válido entre 1000 e 2026.")
        return ano

class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['livro', 'nome_aluno', 'matricula_aluno', 'data_devolucao_prevista']
        widgets = {
            'livro': forms.Select(attrs={'class': 'form-select'}),
            'nome_aluno': forms.TextInput(attrs={'class': 'form-control'}),
            'matricula_aluno': forms.TextInput(attrs={'class': 'form-control'}),
            'data_devolucao_prevista': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['livro'].queryset = Livro.objects.filter(disponivel=True)