# Generated by Django 3.1.13 on 2021-09-26 01:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0005_auto_20210621_1445'),
        ('processos', '0005_auto_20210618_1920'),
    ]

    operations = [
        migrations.AddField(
            model_name='processocompra',
            name='subgrupo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='produtos.subgrupoproduto'),
        ),
    ]
