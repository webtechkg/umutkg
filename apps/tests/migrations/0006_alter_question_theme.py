# Generated by Django 5.1.7 on 2025-03-09 03:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0005_alter_answer_text_kg_alter_question_text_kg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='theme',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tests.theme', verbose_name='Тема вопроса'),
        ),
    ]
