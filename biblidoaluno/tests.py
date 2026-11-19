from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Livro, Emprestimo
from .forms import LivroForm, EmprestimoForm

class BiblioFacilTests(TestCase):

    def setUp(self):
        # Cria um livro padrão antes de cada teste
        self.livro = Livro.objects.create(
            titulo="O Pequeno Príncipe",
            autor="Antoine de Saint-Exupéry",
            categoria="Ficcao",
            ano_publicacao=1943,
            disponivel=True
        )

    def test_criacao_livro_str(self):
        """Testa se o __str__ do Model Livro retorna o formato esperado"""
        self.assertEqual(str(self.livro), "O Pequeno Príncipe (Ficcao)")
        self.assertTrue(self.livro.disponivel)

    def test_formulario_livro_valido(self):
        """Testa se o LivroForm valida corretamente dados reais"""
        dados = {
            'titulo': '1984',
            'autor': 'George Orwell',
            'categoria': 'Ficcao',
            'ano_publicacao': 1949
        }
        form = LivroForm(data=dados)
        self.assertTrue(form.is_valid())

    def test_formulario_livro_invalido(self):
        """Testa se o LivroForm rejeita formulário sem título"""
        dados = {'titulo': '', 'autor': 'Autor Teste', 'categoria': 'Geral', 'ano_publicacao': 2020}
        form = LivroForm(data=dados)
        self.assertFalse(form.is_valid())

    def test_view_home_status_200(self):
        """Testa se a página inicial carrega com sucesso (HTTP 200)"""
        response = self.client.get(reverse('biblidoaluno:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "O PEQUENO PRÍNCIPE")

    def test_registrar_emprestimo_via_post(self):
        """Testa o fluxo completo de POST para emprestar um livro"""
        amanha = timezone.now().date() + timedelta(days=7)
        url = reverse('biblidoaluno:registrar_emprestimo')
        
        response = self.client.post(url, {
            'livro': self.livro.id,
            'nome_aluno': 'João da Silva',
            'matricula_aluno': '2026001',
            'data_devolucao_prevista': amanha
        })

        # Verifica se redirecionou após salvar (HTTP 302)
        self.assertEqual(response.status_code, 302)
        
        # Atualiza o objeto do banco e verifica se ficou indisponível
        self.livro.refresh_from_db()
        self.assertFalse(self.livro.disponivel)
        self.assertEqual(Emprestimo.objects.count(), 1)
