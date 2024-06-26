# Generated by Django 5.0.4 on 2024-04-07 22:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('uf', models.CharField(max_length=2)),
            ],
            options={
                'db_table': 'estado',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.IntegerField()),
                ('nome', models.CharField(max_length=100)),
                ('uf', models.CharField(max_length=2)),
            ],
            options={
                'db_table': 'municipio',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Servicos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('servico', models.TextField(unique=True)),
            ],
            options={
                'db_table': 'servicos',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.TextField(unique=True)),
                ('nome', models.TextField(max_length=150)),
                ('email', models.TextField(unique=True)),
                ('cpf', models.TextField(unique=True)),
                ('celular', models.TextField(max_length=14)),
                ('cidade', models.IntegerField()),
                ('confirmacao', models.IntegerField()),
            ],
            options={
                'db_table': 'usuarios',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UsuariosServicos',
            fields=[
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='appServicos.usuarios')),
                ('descricao', models.TextField(blank=True, max_length=500, null=True)),
                ('cidade', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'usuarios_servicos',
                'managed': False,
            },
        ),
    ]
