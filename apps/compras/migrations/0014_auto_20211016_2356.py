# Generated by Django 3.1.13 on 2021-10-17 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0013_itemlote_lote_pregao'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pregao',
            options={'ordering': ['data_disputa'], 'verbose_name': 'Pregão', 'verbose_name_plural': 'Pregões'},
        ),
        migrations.AlterField(
            model_name='itemsc',
            name='descricao',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Descrição adicional'),
        ),
    ]
