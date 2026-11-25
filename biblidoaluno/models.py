from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Autor(models.Model):
    nome = models.CharField(max_length=150, verbose_name="Nome do Autor")
    nacionalidade = models.CharField(max_length=80, blank=True, verbose_name="Nacionalidade")

    def __str__(self):
        return self.nome

class Livro(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título")
    # Relacionamento 1: Livro pertence a um Autor (ForeignKey)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name="livros", verbose_name="Autor")
    categoria = models.CharField(max_length=50, default="Geral", verbose_name="Categoria")
    ano_publicacao = models.IntegerField(verbose_name="Ano de Publicação")
    disponivel = models.BooleanField(default=True, verbose_name="Disponível")

    def __str__(self):
        return f"{self.titulo} ({self.autor.nome})"

class Emprestimo(models.Model):
    # Relacionamento 2: Empréstimo vinculado a um Livro (ForeignKey)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name="emprestimos", verbose_name="Livro")
    # Relacionamento 3: Bibliotecário/Usuário que registrou (ForeignKey com User)
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    nome_aluno = models.CharField(max_length=120, verbose_name="Nome do Aluno")
    matricula_aluno = models.CharField(max_length=30, verbose_name="Matrícula")
    data_emprestimo = models.DateField(default=timezone.now, verbose_name="Data de Empréstimo")
    data_devolucao_prevista = models.DateField(verbose_name="Data Prevista de Devolução")
    devolvido = models.BooleanField(default=False, verbose_name="Devolvido")

    def save(self, *args, **kwargs):
        if not self.data_devolucao_prevista:
            self.data_devolucao_prevista = self.data_emprestimo + timedelta(days=7)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.livro.titulo} -> {self.nome_aluno}"