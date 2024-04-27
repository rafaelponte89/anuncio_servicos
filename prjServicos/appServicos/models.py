# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Estado(models.Model):
    nome = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)

    class Meta:
        managed = False
        db_table = 'estado'


class Municipio(models.Model):
    codigo = models.IntegerField()
    nome = models.CharField(max_length=100)
    uf = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'municipio'


class Servicos(models.Model):
    servico = models.TextField(unique=True)

    class Meta:
        managed = False
        db_table = 'servicos'


class Usuarios(models.Model):
    usuario = models.TextField(unique=True)
    nome = models.TextField(max_length=150)
    email = models.TextField(unique=True)
    senha = models.TextField(max_length=15)
    cpf = models.TextField(unique=True)
    celular = models.TextField()
    uf = models.ForeignKey(Estado, models.DO_NOTHING, db_column='uf')
    cidade = models.ForeignKey(Municipio, models.DO_NOTHING, db_column='cidade')
    confirmacao = models.IntegerField(default=0)
    

    class Meta:
        managed = False
        db_table = 'usuarios'

    def __eq__(self, other):
       
        # Equality Comparison between two objects
        return (self.usuario == other.usuario and self.nome == other.nome and 
                self.email == other.email and 
                self.senha == other.senha and self.cpf == other.cpf and
                self.celular == other.celular and self.uf == other.uf and
                self.cidade == other.cidade)
 


class UsuariosServicos(models.Model):
    id = models.IntegerField(models.DO_NOTHING, primary_key=True)  # The composite primary key (usuario_id, servico_id) found, that is not supported. The first column is selected.
    usuario = models.ForeignKey(Usuarios, models.DO_NOTHING)  # The composite primary key (usuario_id, servico_id) found, that is not supported. The first column is selected.
    servico = models.ForeignKey(Servicos, models.DO_NOTHING)
    descricao = models.TextField(blank=True, null=True,max_length=500)
    uf = models.ForeignKey(Estado, models.DO_NOTHING, db_column='uf', blank=True, null=True)
    cidade = models.ForeignKey(Municipio, models.DO_NOTHING, db_column='cidade', blank=True, null=True)
    media = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'usuarios_servicos'
        unique_together = [('usuario','servico')]

class Avaliacao(models.Model):
    id = models.BigAutoField(primary_key=True)
    prazo = models.IntegerField()
    preco = models.IntegerField()
    qualidade = models.IntegerField()
    transparencia = models.IntegerField()
    usuario = models.ForeignKey(Usuarios, models.DO_NOTHING) #Usuário quem avaliou o serviço prestado
    anuncio = models.ForeignKey(UsuariosServicos, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'avaliacao'
        unique_together = [('usuario_id','anuncio_id')]