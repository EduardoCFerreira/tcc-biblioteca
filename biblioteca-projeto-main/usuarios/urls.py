from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/create/', views.register_create, name='create'),
    path('login/', views.login_view, name='login'),
    path('login/create/', views.login_create, name='login_create'),
    path('logout/', views.logout_view, name='logout'),
    path('emprestimo/', views.emprestimo, name='emprestimo'),
    path('livro-editar-detalhe/', views.livro_editar_detalhe, name='livro_editar_detalhe'),
    path('livro-editar/<int:id>/', views.livro_editar, name='livro_editar'),
    path('livro-adicionar/', views.livro_adicionar, name='livro-adicionar'),
    path('categoria-adicionar/', views.categoria_adicionar, name='categoria-adicionar'),
    path('categoria-editar-detalhe/', views.categoria_editar_detalhe, name='categoria_editar_detalhe'),
    path('categoria-editar/<int:id>/', views.categoria_editar, name='categoria_editar'),
    path('autor-criar/', views.autor_adicionar, name='autor_adicionar'),
    path('autor-editar-detalhe/', views.autor_editar_detalhe, name='autor_editar_detalhe'),
    path('autor-editar/<int:id>/', views.autor_editar, name='autor_editar')
]
