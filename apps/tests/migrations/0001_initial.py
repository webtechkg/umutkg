# Generated by Django 5.0.6 on 2024-06-15 07:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(verbose_name='Номер вопроса')),
                ('text_ru', models.TextField(verbose_name='Текст Вопроса')),
                ('text_kg', models.TextField(verbose_name='Вопросдын тексты')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='tests/test')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
            },
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, verbose_name='Название темы')),
                ('photo', models.ImageField(upload_to='tests/theme')),
                ('desc', models.TextField(verbose_name='Описание темы')),
            ],
            options={
                'verbose_name': 'Тема',
                'verbose_name_plural': 'Темы',
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_ru', models.TextField(verbose_name='Ответ на русском')),
                ('text_kg', models.TextField(verbose_name='Ответ на кыргызском')),
                ('is_correct', models.BooleanField(default=False, verbose_name='Правильный ли ответ?')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='tests.question', verbose_name='Вопрос')),
            ],
            options={
                'verbose_name': 'Ответ',
                'verbose_name_plural': 'Ответы',
            },
        ),
        migrations.AddField(
            model_name='question',
            name='theme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.theme', verbose_name='Тема вопроса'),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(verbose_name='Номер вопроса')),
                ('questions', models.ManyToManyField(to='tests.question', verbose_name='Вопрос')),
            ],
            options={
                'verbose_name': 'Билет',
                'verbose_name_plural': 'Билеты',
            },
        ),
    ]