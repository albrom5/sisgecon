# Generated by Django 3.1.13 on 2021-08-15 20:06

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
            name='CategoriaSOF',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Incluído em:')),
                ('modificado_em', models.DateTimeField(auto_now=True, null=True, verbose_name='Alterado em:')),
                ('cod', models.CharField(max_length=1)),
                ('descricao', models.CharField(max_length=200)),
                ('criador', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_categoriasof', to=settings.AUTH_USER_MODEL, verbose_name='Incluído por:')),
                ('ultimo_editor', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_edited_categoriasof', to=settings.AUTH_USER_MODEL, verbose_name='Alterado por:')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Dotacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Incluído em:')),
                ('modificado_em', models.DateTimeField(auto_now=True, null=True, verbose_name='Alterado em:')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sof.categoriasof')),
                ('criador', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_dotacao', to=settings.AUTH_USER_MODEL, verbose_name='Incluído por:')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UnidadeSOF',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Incluído em:')),
                ('modificado_em', models.DateTimeField(auto_now=True, null=True, verbose_name='Alterado em:')),
                ('cod', models.CharField(max_length=2)),
                ('descricao', models.CharField(max_length=200)),
                ('criador', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_unidadesof', to=settings.AUTH_USER_MODEL, verbose_name='Incluído por:')),
                ('ultimo_editor', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_edited_unidadesof', to=settings.AUTH_USER_MODEL, verbose_name='Alterado por:')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubFuncaoSOF',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Incluído em:')),
                ('modificado_em', models.DateTimeField(auto_now=True, null=True, verbose_name='Alterado em:')),
                ('cod', models.CharField(max_length=3)),
                ('descricao', models.CharField(max_length=200)),
                ('criador', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_subfuncaosof', to=settings.AUTH_USER_MODEL, verbose_name='Incluído por:')),
                ('ultimo_editor', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_edited_subfuncaosof', to=settings.AUTH_USER_MODEL, verbose_name='Alterado por:')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubElementoSOF',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Incluído em:')),
                ('modificado_em', models.DateTimeField(auto_now=True, null=True, verbose_name='Alterado em:')),
                ('cod', models.CharField(max_length=2)),
                ('descricao', models.CharField(max_length=200)),
                ('criador', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_subelementosof', to=settings.AUTH_USER_MODEL, verbose_name='Incluído por:')),
                ('ultimo_editor', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_edited_subelementosof', to=settings.AUTH_USER_MODEL, verbose_name='Alterado por:')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Incluído em:')),
                ('modificado_em', models.DateTimeField(auto_now=True, null=True, verbose_name='Alterado em:')),
                ('numero', models.CharField(max_length=9)),
                ('data_lancamento', models.DateField(blank=True, null=True)),
                ('valor', models.DecimalField(blank=True, decimal_places=6, max_digits=19, null=True)),
                ('criador', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_reserva', to=settings.AUTH_USER_MODEL, verbose_name='Incluído por:')),
                ('dotacao', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sof.dotacao')),
                ('ultimo_editor', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_edited_reserva', to=settings.AUTH_USER_MODEL, verbose_name='Alterado por:')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProjetoAtividadeSOF',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Incluído em:')),
                ('modificado_em', models.DateTimeField(auto_now=True, null=True, verbose_name='Alterado em:')),
                ('cod', models.CharField(max_length=4)),
                ('descricao', models.CharField(max_length=200)),
                ('criador', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_projetoatividadesof', to=settings.AUTH_USER_MODEL, verbose_name='Incluído por:')),
                ('ultimo_editor', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_edited_projetoatividadesof', to=settings.AUTH_USER_MODEL, verbose_name='Alterado por:')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProgramaSOF',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Incluído em:')),
                ('modificado_em', models.DateTimeField(auto_now=True, null=True, verbose_name='Alterado em:')),
                ('cod', models.CharField(max_length=4)),
                ('descricao', models.CharField(max_length=200)),
                ('criador', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_programasof', to=settings.AUTH_USER_MODEL, verbose_name='Incluído por:')),
                ('ultimo_editor', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_edited_programasof', to=settings.AUTH_USER_MODEL, verbose_name='Alterado por:')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrgaoSOF',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Incluído em:')),
                ('modificado_em', models.DateTimeField(auto_now=True, null=True, verbose_name='Alterado em:')),
                ('cod', models.CharField(max_length=2)),
                ('descricao', models.CharField(max_length=200)),
                ('criador', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_orgaosof', to=settings.AUTH_USER_MODEL, verbose_name='Incluído por:')),
                ('ultimo_editor', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_edited_orgaosof', to=settings.AUTH_USER_MODEL, verbose_name='Alterado por:')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ModalidadeSOF',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Incluído em:')),
                ('modificado_em', models.DateTimeField(auto_now=True, null=True, verbose_name='Alterado em:')),
                ('cod', models.CharField(max_length=2)),
                ('descricao', models.CharField(max_length=200)),
                ('criador', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_modalidadesof', to=settings.AUTH_USER_MODEL, verbose_name='Incluído por:')),
                ('ultimo_editor', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_edited_modalidadesof', to=settings.AUTH_USER_MODEL, verbose_name='Alterado por:')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GrupoSOF',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Incluído em:')),
                ('modificado_em', models.DateTimeField(auto_now=True, null=True, verbose_name='Alterado em:')),
                ('cod', models.CharField(max_length=1)),
                ('descricao', models.CharField(max_length=200)),
                ('criador', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_gruposof', to=settings.AUTH_USER_MODEL, verbose_name='Incluído por:')),
                ('ultimo_editor', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_edited_gruposof', to=settings.AUTH_USER_MODEL, verbose_name='Alterado por:')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FuncaoSOF',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Incluído em:')),
                ('modificado_em', models.DateTimeField(auto_now=True, null=True, verbose_name='Alterado em:')),
                ('cod', models.CharField(max_length=2)),
                ('descricao', models.CharField(max_length=200)),
                ('criador', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_funcaosof', to=settings.AUTH_USER_MODEL, verbose_name='Incluído por:')),
                ('ultimo_editor', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_edited_funcaosof', to=settings.AUTH_USER_MODEL, verbose_name='Alterado por:')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FonteRecursoSOF',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Incluído em:')),
                ('modificado_em', models.DateTimeField(auto_now=True, null=True, verbose_name='Alterado em:')),
                ('cod', models.CharField(max_length=2)),
                ('descricao', models.CharField(max_length=200)),
                ('criador', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_fonterecursosof', to=settings.AUTH_USER_MODEL, verbose_name='Incluído por:')),
                ('ultimo_editor', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_edited_fonterecursosof', to=settings.AUTH_USER_MODEL, verbose_name='Alterado por:')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Empenho',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Incluído em:')),
                ('modificado_em', models.DateTimeField(auto_now=True, null=True, verbose_name='Alterado em:')),
                ('numero', models.CharField(max_length=9)),
                ('data_lancamento', models.DateField(blank=True, null=True)),
                ('valor', models.DecimalField(blank=True, decimal_places=6, max_digits=19, null=True)),
                ('criador', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_empenho', to=settings.AUTH_USER_MODEL, verbose_name='Incluído por:')),
                ('dotacao', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sof.dotacao')),
                ('ultimo_editor', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_edited_empenho', to=settings.AUTH_USER_MODEL, verbose_name='Alterado por:')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ElementoSOF',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Incluído em:')),
                ('modificado_em', models.DateTimeField(auto_now=True, null=True, verbose_name='Alterado em:')),
                ('cod', models.CharField(max_length=2)),
                ('descricao', models.CharField(max_length=200)),
                ('criador', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_elementosof', to=settings.AUTH_USER_MODEL, verbose_name='Incluído por:')),
                ('ultimo_editor', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_edited_elementosof', to=settings.AUTH_USER_MODEL, verbose_name='Alterado por:')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='dotacao',
            name='elemento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sof.elementosof'),
        ),
        migrations.AddField(
            model_name='dotacao',
            name='fonte_recurso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sof.fonterecursosof'),
        ),
        migrations.AddField(
            model_name='dotacao',
            name='funcao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sof.funcaosof'),
        ),
        migrations.AddField(
            model_name='dotacao',
            name='grupo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sof.gruposof'),
        ),
        migrations.AddField(
            model_name='dotacao',
            name='modalidade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sof.modalidadesof'),
        ),
        migrations.AddField(
            model_name='dotacao',
            name='orgao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sof.orgaosof'),
        ),
        migrations.AddField(
            model_name='dotacao',
            name='programa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sof.programasof'),
        ),
        migrations.AddField(
            model_name='dotacao',
            name='projeto_atividade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sof.projetoatividadesof'),
        ),
        migrations.AddField(
            model_name='dotacao',
            name='subelemento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sof.subelementosof'),
        ),
        migrations.AddField(
            model_name='dotacao',
            name='subfuncao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sof.subfuncaosof'),
        ),
        migrations.AddField(
            model_name='dotacao',
            name='ultimo_editor',
            field=cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_edited_dotacao', to=settings.AUTH_USER_MODEL, verbose_name='Alterado por:'),
        ),
        migrations.AddField(
            model_name='dotacao',
            name='unidade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sof.unidadesof'),
        ),
        migrations.CreateModel(
            name='ContratoSof',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Incluído em:')),
                ('modificado_em', models.DateTimeField(auto_now=True, null=True, verbose_name='Alterado em:')),
                ('numero', models.CharField(max_length=9)),
                ('data_lancamento', models.DateField(blank=True, null=True)),
                ('valor', models.DecimalField(blank=True, decimal_places=6, max_digits=19, null=True)),
                ('criador', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_contratosof', to=settings.AUTH_USER_MODEL, verbose_name='Incluído por:')),
                ('reserva', models.ManyToManyField(to='sof.Reserva')),
                ('ultimo_editor', cuser.fields.CurrentUserField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_edited_contratosof', to=settings.AUTH_USER_MODEL, verbose_name='Alterado por:')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]