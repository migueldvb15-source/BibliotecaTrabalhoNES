from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'biblidoaluno'

urlpatterns = [
    # Página Inicial e Filtros
    path('', views.home_view, name='home'),
    path('livros/<int:pk>/', views.detalhe_livro, name='detalhe_livro'),
    path('livros/categoria/<str:nome_categoria>/', views.listar_por_categoria, name='listar_por_categoria'),

    # Autenticação (RF01)
    path('cadastro/', views.cadastro_usuario, name='cadastro'),
    path('login/', auth_views.LoginView.as_view(template_name='biblidoaluno/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # CRUD Livros e Autores (RF02)
    path('autores/novo/', views.cadastrar_autor, name='cadastrar_autor'),
    path('livros/novo/', views.cadastrar_livro, name='cadastrar_livro'),
    path('livros/<int:pk>/editar/', views.editar_livro, name='editar_livro'),
    path('livros/<int:pk>/excluir/', views.excluir_livro, name='excluir_livro'),

    # Empréstimos
    path('emprestimos/novo/', views.registrar_emprestimo, name='registrar_emprestimo'),
    path('emprestimos/<int:pk>/devolver/', views.devolver_livro, name='devolver_livro'),
]