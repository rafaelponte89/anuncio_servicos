# Generated by Django 5.0.4 on 2024-04-15 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appServicos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Avaliacao',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('avaliacao', models.IntegerField()),
            ],
            options={
                'db_table': 'avaliacao',
                'managed': False,
            },
        ),
    ]