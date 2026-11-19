from django.urls import path
from . import views

app_name = 'biblidoaluno'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('livros/<int:pk>/', views.detalhe_livro, name='detalhe_livro'),
    path('livros/categoria/<str:nome_categoria>/', views.listar_por_categoria, name='listar_por_categoria'),
    
    # Rotas dos formulários e ações POST
    path('livros/novo/', views.cadastrar_livro, name='cadastrar_livro'),
    path('emprestimos/novo/', views.registrar_emprestimo, name='registrar_emprestimo'),
    path('emprestimos/<int:pk>/devolver/', views.devolver_livro, name='devolver_livro'),
]