# Generated by Django 3.1.11 on 2021-06-01 05:37

import cuser.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Processo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Incluído em:')),
                ('modificado_em', models.DateTimeField(auto_now=True, null=True, verbose_name='Alterado em:')),
                ('numero_sei', models.CharField(max_length=19, unique=True, verbose_name='Número SEI')),
                ('criador', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_processo', to=settings.AUTH_USER_MODEL, verbose_name='Incluído por:')),
                ('ultimo_editor', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_edited_processo', to=settings.AUTH_USER_MODEL, verbose_name='Alterado por:')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
