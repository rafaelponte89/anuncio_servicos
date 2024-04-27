from django.urls import path
from .views import (index,login, cadastro, carregar_estados, 
                    carregar_municipios, cadastrar_usuario, 
                    buscar_login, confirmar_email, sair, anunciar, cadastrar_anuncio,
                    carregar_servicos, pesquisar_prestadores, deletar_anuncio,
                    carregar_dados_cadastrais, selecionar_municipio, selecionar_estado,
                    atualizar_usuario, tela_atualizar_anuncio, atualizar_anuncio, enviar_redefinicao,
                    redefinir_senha, tela_redefinicao, exibir_meus_anuncios, avaliar_anuncio, exibir_media_avaliacao, tela_avaliar_anuncio)

urlpatterns = [
    path('',index,name='index'),
    path('login/', login, name='login'),
    path('cadastro', cadastro, name='cadastro'),
    path('carregar_estados', carregar_estados, name='carregar_estados'),
    path('carregar_municipios', carregar_municipios, name='carregar_municipios'),
    path('servicos', carregar_servicos, name='carregar_servicos'),
    path('cadastrar_usuario/', cadastrar_usuario, name='cadastrar_usuario'),
    path('buscar_login', buscar_login, name='buscar_login'),
    path('confirmar_email/<str:codigo>/<str:usuario>', confirmar_email, name='confirmar_email'),
    path('sair', sair, name='sair'),
    path('anunciar', anunciar, name='anunciar'),
    path('cadastrar_anuncio', cadastrar_anuncio, name='cadastrar_anuncio'),
    path('pesquisar_prestadores', pesquisar_prestadores, name='pesquisar_prestadores'),
    path('deletar_anuncio', deletar_anuncio,name='deletar_anuncio'),
    path('carregar_dados_cadastrais', carregar_dados_cadastrais,name='carregar_dados_cadastrais'),
    path('selecionar_municipio', selecionar_municipio, name='selecionar_municipio'),
    path('selecionar_estado', selecionar_estado,name='selecionar_estado'),
    path('atualizar_usuario', atualizar_usuario,name='atualizar_usuario'),
    path('tela_atualizar_anuncio', tela_atualizar_anuncio, name='tela_atualizar_anuncio'),
    path('atualizar_anuncio', atualizar_anuncio,name='atualizar_anuncio'),
    path('enviar_redefinicao', enviar_redefinicao, name='enviar_redefinicao'),
    path('redefinir_senha', redefinir_senha, name='redefinir_senha'),
    path('tela_redefinicao/<str:codigo>/<str:usuario>',tela_redefinicao, name='tela_redefinicao'),
    path('exibir_meus_anuncios', exibir_meus_anuncios, name='exibir_meus_anuncios'),

    path('tela_avaliar_anuncio', tela_avaliar_anuncio, name='tela_avaliar_anuncio'),
    path('avaliar_anuncio', avaliar_anuncio, name='avaliar_anuncio'),
    path('exibir_media_avaliacao', exibir_media_avaliacao, name='exibir_media_avaliacao')




    
]