from django.db import models
from django.utils import timezone
from datetime import timedelta

class Livro(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título")
    autor = models.CharField(max_length=150, verbose_name="Autor")
    categoria = models.CharField(max_length=50, default="Geral", verbose_name="Categoria")
    ano_publicacao = models.IntegerField(verbose_name="Ano de Publicação")
    disponivel = models.BooleanField(default=True, verbose_name="Disponível")

    def __str__(self):
        return f"{self.titulo} ({self.categoria})"

class Emprestimo(models.Model):
    nome_aluno = models.CharField(max_length=120, verbose_name="Nome do Aluno")
    matricula_aluno = models.CharField(max_length=30, verbose_name="Matrícula")
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name="emprestimos", verbose_name="Livro")
    data_emprestimo = models.DateField(default=timezone.now, verbose_name="Data de Empréstimo")
    data_devolucao_prevista = models.DateField(verbose_name="Data Prevista de Devolução")
    devolvido = models.BooleanField(default=False, verbose_name="Devolvido")

    def save(self, *args, **kwargs):
        if not self.data_devolucao_prevista:
            self.data_devolucao_prevista = self.data_emprestimo + timedelta(days=7)
        super().save(*args, **kwargs)

    def esta_atrasado(self):
        return not self.devolvido and timezone.now().date() > self.data_devolucao_prevista

    def __str__(self):
        return f"{self.livro.titulo} -> {self.nome_aluno}"