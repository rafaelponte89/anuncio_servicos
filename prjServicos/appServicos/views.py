from django.shortcuts import render, HttpResponse
from .models import Estado, Municipio, Usuarios, UsuariosServicos, Servicos, Avaliacao
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.db.models import Avg

from django.conf import settings
# Create your views here.
import random
import hashlib


def calcular_hash(texto):
    # Crie um objeto hash (usando SHA-256 neste exemplo)
    h = hashlib.sha256()
    # Atualize o hash com o texto
    h.update(texto.encode('utf-8'))
    # Obtenha o valor de hash em hexadecimal
    return h.hexdigest()

def index(request):

    autenticado = esta_autenticado(request)
    print(autenticado)

    if autenticado:
        nome = request.session['nome']
        estado = request.session['estado']
        municipio = request.session['municipio']
        return render(request,'index.html',{'autenticado':autenticado,'nome':nome,'estado':estado,'municipio':municipio})
    else:
       return render(request, 'index.html')
    
def login(request):
    return render(request, 'login.html')

def cadastro(request):
    
    return render(request, 'cadastro.html')


def carregar_estados(request):
    estados = Estado.objects.all().order_by('uf')
    opcao = '<option value=0> Selecione </option>'

    for estado in estados:
        opcao += f'<option value={estado.id}> {estado.uf} </option>'

    return HttpResponse(opcao)

def carregar_municipios(request):
    opcao = ''
    estado = request.GET.get('estado')
    municipios = Municipio.objects.filter(uf=estado).order_by('nome')
    for municipio in municipios:
        opcao += f'<option value={municipio.id}> {municipio.nome} </option>'

    return HttpResponse(opcao)


def carregar_servicos(request):
    opcao = ''
    servicos = Servicos.objects.all().order_by('servico')
    for servico in servicos:
        opcao += f'<option value={servico.id}> {servico.servico} </option>'

    return HttpResponse(opcao)


def cadastrar_usuario(request):
    login = request.POST.get('usuario')
    nome = request.POST.get('nome')
    email = request.POST.get('email')
    cpf = request.POST.get('cpf')
    celular = request.POST.get('celular')
    estado = request.POST.get('estado')
    municipio = request.POST.get('municipio')
    municipio = Municipio.objects.get(pk=municipio)
    estado = Estado.objects.get(pk=estado)
    senha = request.POST.get('senha')

    usuario = Usuarios(usuario=login, nome=nome, email=email, cpf=cpf, celular=celular,uf=estado,cidade=municipio, senha=senha)

    usuario.save()
  
    enviar_email(request, usuario)
   
    return HttpResponse('salvo')

def buscar_login(request):
    login = request.POST.get('login')
    senha = request.POST.get('senha')
    usuario = (Usuarios.objects.filter(usuario__exact = login ).filter(senha__exact=senha) or 
               Usuarios.objects.filter(email__exact = login).filter(senha__exact=senha))

    if usuario and usuario[0].confirmacao:
        request.session['id_usuario'] = usuario[0].id
        request.session['nome'] = usuario[0].nome
        request.session['login'] = usuario[0].usuario
        request.session['estado'] = usuario[0].uf.id
        request.session['municipio'] = usuario[0].cidade.id

        return HttpResponse("1")
    else:
        return HttpResponse("0")


def enviar_email(request,usuario):
    codigo = calcular_hash(usuario.email)
    mensagem = (f'<a href="http://localhost:7010/confirmar_email/{codigo}/{usuario.usuario}">Confirmação do Email</a>')
    destinatario = request.POST.get('email')

    email = EmailMessage(subject='Confirmação de Email', body=mensagem,
                             from_email=settings.EMAIL_HOST_USER,
                             to=[destinatario])
    email.content_subtype='html'
    email.send()
    


def confirmar_email(request,codigo, usuario):
    
    obj_usuario = Usuarios.objects.filter(usuario__exact = usuario)[0]
    mensagem =''
    print(codigo)
   
    obj_hash = calcular_hash(obj_usuario.email)
   
    print(obj_hash)


    if obj_usuario and obj_hash == codigo:
        obj_usuario.confirmacao = 1
        obj_usuario.save()
        mensagem = 'Email confirmado com sucesso!'
    else:
        mensagem = 'Email não confirmado!'
    

    return render(request, 'confirmacao.html', {'mensagem':mensagem})


def esta_autenticado(request):
    try:
        return True if request.session['login'] else False
    except:
        return False
    

def sair(request):
    try:
        request.session.clear()
        return render(request,'index.html')
    except:
        pass

def anunciar(request):
    autenticado = esta_autenticado(request)

    return render(request, 'anunciar.html',{'autenticado':autenticado})

def cadastrar_anuncio(request):
    
    servico = Servicos.objects.get(pk=request.POST.get('servico'))
    usuario = Usuarios.objects.get(pk=request.session['id_usuario'])
    anuncio = UsuariosServicos(servico=servico, usuario=usuario, uf=usuario.uf, cidade=usuario.cidade, descricao=request.POST.get('descricao'))
    anuncio.save()
    return HttpResponse('Anúncio Salvo com Sucesso!!!')

def deletar_anuncio(request):
    identificador = request.POST.get('id')
    anuncio = UsuariosServicos.objects.get(pk=identificador)
    anuncio.delete()
    return HttpResponse('DELETEADO COM SUCESSO')

def pesquisar_prestadores(request):
    texto = request.GET.get('texto')
    estado = request.GET.get('estado')
    municipio = request.GET.get('municipio')
    media_rank = int(request.GET.get('media_rank'))
    autenticado = esta_autenticado(request)
   
    print(media_rank)
    
    try:
        cartoes = ''
      
        if media_rank:
            anuncios = ((UsuariosServicos.objects.filter(descricao__contains=texto) or 
                    UsuariosServicos.objects.filter(servico__servico__contains=texto) and
                    UsuariosServicos.objects.filter(usuario__usuario__contains=texto)) and 
                    UsuariosServicos.objects.filter(media__gte=media_rank)).filter(uf=estado).filter(cidade=municipio)[:30]
        else:
            anuncios = ((UsuariosServicos.objects.filter(descricao__contains=texto) or 
                    UsuariosServicos.objects.filter(servico__servico__contains=texto) or 
                    UsuariosServicos.objects.filter(usuario__usuario__contains=texto)) or 
                    UsuariosServicos.objects.filter(media__gte=media_rank)).filter(uf=estado).filter(cidade=municipio)[:30]

       # anuncios = anuncios.filter(avalicao__usuariosservicos__)
      
        

               
         
       # selecao=''
       # x = 1
       # y = 6
       # h = 0
       # rotulo = ['Prazo','Preço', 'Qualidade','Transparencia']
       # for i in range(0,4):
       #     selecao += f'<div>{rotulo[i]}'
       #     for j in range(x,y):
       #         h += 1
       #         selecao +=  f""" <label id='estrela{j}' for='selecao{j}'>
       #     <i  class='bi bi-star-fill' > </i>
       #  </label>
       #  <input id='selecao{j}' type='radio' name='{i}'  value='{h}' style='display: none;' />"""
       #     selecao += '</div>'
       #     x += 5
       #     y += 5
       #     h = 0


        for anuncio in anuncios:
                        
            if autenticado:
                if anuncio.usuario.id == request.session['id_usuario']:
                    cartoes += f"""<div class="card m-2" style="width: 18rem;">
                    <!--<img class="card-img-top" src="..." alt="Card image cap"> -->
                    <div class="card-body">
                    <h5 class="card-title">{anuncio.servico.servico}</h5>
                    <p class="card-text">{anuncio.descricao}</p>
                    <p class="card-text">{anuncio.usuario.nome}</p>
                    <p class="card-text">{anuncio.usuario.celular}</p>

                
                    <button class="btn btn-danger excluir" value={anuncio.id}>Excluir</button>

                    <button type='button' class="btn btn-warning editar" data-bs-toggle='modal' data-bs-target='#editarAnuncio' value={anuncio.id}>Editar</button>
                                <button type='button' class="btn btn-primary exibir_media mt-2" data-bs-toggle='modal' data-bs-target='#mediaModal' value={anuncio.id}>Avaliação Geral</button>

                         </div>
                    </div>
                """
                else:
                    cartoes += f"""<div class="card m-2" style="width: 18rem;">
                <!--<img class="card-img-top" src="..." alt="Card image cap"> -->
                <div class="card-body">
                <h5 class="card-title">{anuncio.servico.servico}</h5>
                <p class="card-text">{anuncio.descricao}</p>
                <p class="card-text">{anuncio.usuario.nome}</p>
                <button class="btn btn-success ver" value={anuncio.usuario.celular}><i class="bi bi-eye"></i>Ver Telefone</button>
                
                
                                <button class="btn btn-dark avaliar" data-bs-toggle='modal' data-bs-target='#avaliacaoModal' value='{anuncio.id}'><i class="bi bi-pen"></i>Avaliar</button>
                                                   
                                <button type='button' class="btn btn-primary exibir_media mt-2" data-bs-toggle='modal' data-bs-target='#mediaModal' value={anuncio.id}>Avaliação Geral</button>

                    </div>
                </div>
                 """ 
    
            else:
                cartoes += f"""<div class="card m-2" style="width: 18rem;">
                <!--<img class="card-img-top" src="..." alt="Card image cap"> -->
                <div class="card-body">
                <h5 class="card-title">{anuncio.servico.servico}</h5>
                <p class="card-text">{anuncio.descricao}</p>
                <p class="card-text">{anuncio.usuario.nome}</p>
                <button class="btn btn-success ver" value={anuncio.usuario.celular}><i class="bi bi-eye"></i>Ver Telefone</button>
                                <button type='button' class="btn btn-primary exibir_media mt-2" data-bs-toggle='modal' data-bs-target='#mediaModal' value={anuncio.id}>Avaliação Geral</button>

                    </div>
                </div>
                """ 
        if anuncios:
            return HttpResponse(cartoes)
        else:
            return HttpResponse("<div class='text-info rounded-2 mt-5 shadow p-3'> <h2>Nenhum Prestador Encontrado para esta Pesquisa!!!</h2></div>")
    except Exception as e:    
        return HttpResponse(e)

def carregar_dados_cadastrais(request):
    autenticado = esta_autenticado(request)
    if autenticado:
        print("autenticado")
        usuario = Usuarios.objects.get(pk=request.session['id_usuario'])
        
        dados = {
            'id': usuario.id,
            'usuario':usuario.usuario,
            'nome':usuario.nome,
            'email':usuario.email,
            'senha':usuario.senha,
            'cpf': usuario.cpf,
            'celular': usuario.celular,
            'estado': usuario.uf,
            'cidade': usuario.cidade
            }
        return render(request, 'cadastro.html',{'dados':dados})
    else:
        return HttpResponse('É preciso estar autenticado para acessar os dados cadastrais!!! <a href="http://localhost:7010/login">Clique aqui!!!</a>')

  
def selecionar_estado(request):
    autenticado = esta_autenticado(request)
    if autenticado:
        usuario = int(request.session['id_usuario'])
        usuario = Usuarios.objects.get(pk=usuario)
        estados = Estado.objects.all().order_by('uf')
        opcao = '<option value=0> Selecione </option>'


        for estado in estados:
            if usuario.uf.id == estado.id:
                print(estado.id)
                print(usuario.uf)
                opcao += f'<option value={estado.id} selected> {estado.uf} </option>'
            else:
                opcao += f'<option value={estado.id} > {estado.uf} </option>'


        return HttpResponse(opcao)
    

def selecionar_municipio(request):
    autenticado = esta_autenticado(request)
    if autenticado:
        usuario = int(request.session['id_usuario'])
        usuario = Usuarios.objects.get(pk=usuario)
        municipios = Municipio.objects.filter(uf=usuario.uf.id).order_by('nome')
        opcao = '<option value=0> Selecione </option>'


        for municipio in municipios:
            if usuario.cidade.id == municipio.id:
           
                opcao += f'<option value={municipio.id} selected> {municipio.nome} </option>'
            else:
                opcao += f'<option value={municipio.id}> {municipio.nome} </option>'

    return HttpResponse(opcao)

def atualizar_usuario(request):
    usuario_atualizacao = Usuarios.objects.get(pk=request.POST.get('id'))
    usuario = Usuarios()
    usuario.usuario = request.POST.get('usuario')
    usuario.nome = request.POST.get('nome')
    usuario.email = request.POST.get('email')
    usuario.cpf = request.POST.get('cpf')
    usuario.celular = request.POST.get('celular')
    estado = request.POST.get('estado')

    cidade = request.POST.get('municipio')

    cidade = Municipio.objects.get(pk=cidade)
    estado = Estado.objects.get(pk=estado)
    usuario.uf = estado
    usuario.cidade = cidade
    usuario.senha = request.POST.get('senha')

    if usuario != usuario_atualizacao:
       
        usuario.id = usuario_atualizacao.id
        usuario.confirmacao = 1
        usuario.save(force_update=True)
        anuncios = UsuariosServicos.objects.filter(usuario=usuario)
        for anuncio in anuncios:
            anuncio.uf = usuario.uf
            anuncio.cidade = usuario.cidade
            anuncio.save()
        if usuario.email != usuario_atualizacao.email:
            usuario.confirmacao = 0
            enviar_email(request, usuario)
   
        return HttpResponse('Atualizado!')
    else:
        return HttpResponse('Nada foi alterado!')
    
def avaliar_anuncio(request):
    autenticado = esta_autenticado(request)
    if autenticado:
        usuario = Usuarios(pk=request.session['id_usuario'])
        anuncio = int(request.POST.get('anuncio'))
        prazo = request.POST.get('prazo')
        preco = request.POST.get('preco')
        qualidade = request.POST.get('qualidade')
        transparencia = request.POST.get('transparencia')
        anuncio = UsuariosServicos.objects.get(pk=anuncio)
        avaliacao = Avaliacao.objects.filter(anuncio=anuncio).filter(usuario=usuario)
        
        
        
        
       

        if avaliacao:
            avaliacao[0].prazo = prazo
            avaliacao[0].preco = preco
            avaliacao[0].qualidade = qualidade
            avaliacao[0].transparencia = transparencia
            
            avaliacao[0].save()

            a,b,c,d, media = calcular_media_criterios(anuncio)
            anuncio.media = media
            anuncio.save()
            
            
            return HttpResponse('Avaliação Atualizada!!!')

        else: 
            avaliacao = Avaliacao(prazo=prazo, preco=preco, qualidade=qualidade, transparencia=transparencia,anuncio=anuncio, usuario=usuario)
            avaliacao.save()
            
            a,b,c,d, media = calcular_media_criterios(anuncio)

            anuncio.media = media
            anuncio.save()

            return HttpResponse('Avaliação Gravada!!!')
    else:
        return HttpResponse('É necessário se autenticar para fazer a avaliação!!!')



def calcular_media_criterios(anuncio):
    prazo_m = round(Avaliacao.objects.filter(anuncio=anuncio).aggregate(Avg('prazo'))['prazo__avg'])
    preco_m = round(Avaliacao.objects.filter(anuncio=anuncio).aggregate(Avg('preco'))['preco__avg'])
    qualidade_m = round(Avaliacao.objects.filter(anuncio=anuncio).aggregate(Avg('qualidade'))['qualidade__avg'])
    transparencia_m= round(Avaliacao.objects.filter(anuncio=anuncio).aggregate(Avg('transparencia'))['transparencia__avg'])
    lista = [prazo_m,preco_m,qualidade_m]
    geral_m=  int(sum(lista)/len(lista))

    return prazo_m, preco_m, qualidade_m, transparencia_m, geral_m

def exibir_media_avaliacao(request):
    codigo_anuncio = int(request.GET.get('id'))
    anuncio = UsuariosServicos.objects.get(pk=codigo_anuncio)
    avaliacao = Avaliacao.objects.filter(anuncio = anuncio)
    qtd = avaliacao.count()
    selecao=''
    tela =''

    if avaliacao:
        
        prazo_m, preco_m, qualidade_m, transparencia_m, geral_m = calcular_media_criterios(anuncio)

        x = 1
        y = 6
        h = 0
        rotulo = ['Prazo','Preço', 'Qualidade','Transparência','<strong class="text-success">Média</strong>']
        for i in range(0,5):
            if i == 0:
                valor = prazo_m
            elif i == 1:
                valor = preco_m
            elif i == 2:
                valor= qualidade_m
            elif i == 3:
                valor = transparencia_m
            else:
                
                valor = geral_m
            
            selecao += f'<div>{rotulo[i]}'
            for j in range(x,y):
                h += 1
                if h <= valor:
                    classe='text-warning'
                    checado = 'checked'
                else:
                    checado = ''
                    classe=''
                selecao +=  f""" <label id='' for='selecao' class='{classe}'>
                <i  class='bi bi-star-fill' > </i>
                </label>
                    <input id='' type='radio' name=''  value='{h}' style='display: none;' {checado} disable />"""
            selecao += '</div>'
            x += 5
            y += 5
            h = 0
        tela = f"""<div> 
                <input type='hidden' id='anuncio' value='{anuncio.id}' />
                    {selecao}
                </div>
                <div class='text-primary'>
               Quantidade de Avaliações: {qtd}
                </div>
                """
    else:
        tela = "<div class='text-primary'>Sem avaliações!!! </div>"

    return HttpResponse(tela)

def tela_avaliar_anuncio(request):
    codigo_anuncio = int(request.GET.get('id'))
    anuncio = UsuariosServicos.objects.get(pk=codigo_anuncio)
    usuario = Usuarios.objects.get(pk=request.session['id_usuario'])
    avaliacao = Avaliacao.objects.filter(anuncio = anuncio).filter(usuario = usuario)
    selecao=''

     #prazo_m = round(Avaliacao.objects.filter(anuncio=anuncio).aggregate(Avg('prazo'))['prazo__avg'])
     #preco_m = round(Avaliacao.objects.filter(anuncio=anuncio).aggregate(Avg('preco'))['preco__avg'])
     #qualidade_m = round(Avaliacao.objects.filter(anuncio=anuncio).aggregate(Avg('qualidade'))['qualidade__avg'])
     #transparencia_m= round(Avaliacao.objects.filter(anuncio=anuncio).aggregate(Avg('transparencia'))['transparencia__avg'])

    if avaliacao:
        avaliacao = avaliacao[0]
        x = 1
        y = 6
        h = 0
        rotulo = ['Prazo','Preço', 'Qualidade','Transparencia']
        for i in range(0,4):
            if i == 0:
                valor = avaliacao.prazo
            elif i == 1:
                valor = avaliacao.preco
            elif i == 2:
                valor= avaliacao.qualidade
            else:
                valor = avaliacao.transparencia
            
            selecao += f'<div>{rotulo[i]}'
            for j in range(x,y):
                h += 1
                if h <= valor:
                    classe='text-warning'
                    checado = 'checked'
                else:
                    checado = ''
                    classe=''
                selecao +=  f""" <label id='estrela{j}' for='selecao{j}' class='{classe}'>
                <i  class='bi bi-star-fill' > </i>
                </label>
                    <input id='selecao{j}' type='radio' name='{i}'  value='{h}' style='display: none;' {checado} />"""
            selecao += '</div>'
            x += 5
            y += 5
            h = 0
        tela = f"""<div> 
                <input type='hidden' id='anuncio' value='{anuncio.id}' />
                    {selecao}
                </div>"""
    else:
        x = 1
        y = 6
        h = 0
        rotulo = ['Prazo','Preço', 'Qualidade','Transparencia']
        for i in range(0,4):
            selecao += f'<div>{rotulo[i]}'
            for j in range(x,y):
                h += 1
                selecao +=  f""" <label id='estrela{j}' for='selecao{j}'>
                <i  class='bi bi-star-fill' > </i>
                </label>
                    <input id='selecao{j}' type='radio' name='{i}'  value='{h}' style='display: none;' />"""
            selecao += '</div>'
            x += 5
            y += 5
            h = 0
        tela = f"""<div> 
                <input type='hidden' id='anuncio' value='{anuncio.id}' />
                    {selecao}
                </div>"""
    
    return HttpResponse(tela)

def atualizar_anuncio(request):
    anuncio = UsuariosServicos.objects.get(pk=request.POST.get('id'))
    servico = Servicos.objects.get(pk=request.POST.get('servico'))
    anuncio.servico = servico
    anuncio.descricao = request.POST.get('descricao')
    anuncio.save()
    return HttpResponse('Anúncio Atualizado com Sucesso!!!')

def tela_atualizar_anuncio(request):
    codigo_anuncio = int(request.GET.get('id'))
    anuncio = UsuariosServicos.objects.get(pk=codigo_anuncio)
    servicos = Servicos.objects.all().order_by('servico')
    opcoes = '' 

    for servico in servicos:
        if anuncio.servico == servico:
            opcoes += f"<option value={servico.id} selected> {servico.servico} </option>"

        else:
            opcoes += f"<option value={servico.id}> {servico.servico} </option>"

    tela = f"""
        <form class="rounded-2 mt-5 bg-warning pt-5 pb-5">
            <input id="codigoAnuncio" type="hidden" value="{anuncio.id}"/>
           
            <div class="row">
                <div class="col"></div>
           
                <div class="col-10"> 
                    Serviço:
                    <div class="form-group mt-2">
                        <select id="servicos" class="form-control">
                        {opcoes}
                    </select>
                    </div>
                </div>
                
                <div class="col"></div>
            </div>

            <div class="row">
                <div class="col"></div>
                <div class="col-10">
                    Descrição:
                    <div class="form-group mt-2">
                        <textarea class="form-control" id="descricao" rows="3">{anuncio.descricao}</textarea>
                    </div>
                </div>
                <div class="col"></div>
            </div>
        

          </form>
"""
    return HttpResponse(tela)

def enviar_redefinicao(request):
    login = request.POST.get('login')
    usuario = (Usuarios.objects.filter(usuario=login) or Usuarios.objects.filter(email=login))[0]
    codigo = calcular_hash(usuario.cpf)
    mensagem = (f'<a href="http://localhost:7010/tela_redefinicao/{codigo}/{usuario.usuario}">Redefinir Senha</a>')
    destinatario = usuario.email

    email = EmailMessage(subject='Redefinição de Senha', body=mensagem,
                             from_email=settings.EMAIL_HOST_USER,
                             to=[destinatario])
    email.content_subtype='html'
    email.send()

    return HttpResponse(1)


def redefinir_senha(request):
    senha = request.POST.get('senha')
    login = request.POST.get('login')
    usuario = (Usuarios.objects.filter(usuario = login) or Usuarios.objects.filter(email=login))[0]
    usuario.senha = senha
    usuario.save()
    return HttpResponse(1)

def tela_redefinicao(request,codigo,usuario):
    usuario = (Usuarios.objects.filter(usuario = usuario))[0]



    return render(request, 'redefinicao.html',{'login':usuario.usuario})

def exibir_meus_anuncios(request):
    id_usuario = request.session['id_usuario']
    usuario = Usuarios.objects.get(pk=id_usuario)
    anuncios = UsuariosServicos.objects.filter(usuario=usuario)
    cartoes = ''

    for anuncio in anuncios:
        cartoes += f"""<div class="card m-2" style="width: 18rem;">
                <!--<img class="card-img-top" src="..." alt="Card image cap"> -->
                <div class="card-body">
                <h5 class="card-title">{anuncio.servico.servico}</h5>
                <p class="card-text">{anuncio.descricao}</p>
                <p class="card-text">{anuncio.usuario.nome}</p>
                <p class="card-text">{anuncio.usuario.celular}</p>

            
                <button class="btn btn-danger excluir" value={anuncio.id}>Excluir</button>

                <button type='button' class="btn btn-warning editar" data-bs-toggle='modal' data-bs-target='#editarAnuncio' value={anuncio.id}>Editar</button>
                    
                    </div>
                </div>
            """
    return HttpResponse(cartoes)
