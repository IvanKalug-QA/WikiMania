# Generated by Django 4.2.11 on 2024-05-03 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0002_wiki_subscribe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wiki',
            name='text',
            field=models.TextField(verbose_name='Описаник'),
        ),
    ]
