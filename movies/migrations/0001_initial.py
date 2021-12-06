# Generated by Django 3.2.6 on 2021-12-06 10:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Страна')),
            ],
            options={
                'verbose_name': 'Страна',
                'verbose_name_plural': 'Страны',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Жанр')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15, verbose_name='Зал')),
            ],
            options={
                'verbose_name': 'Зал',
                'verbose_name_plural': 'Зал',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField(verbose_name='Сеанс')),
            ],
            options={
                'verbose_name': 'Сеанс',
                'verbose_name_plural': 'Сеансы',
                'ordering': ('time',),
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('year', models.IntegerField(default='2021', verbose_name='Год')),
                ('director', models.CharField(max_length=70, verbose_name='Режисёр')),
                ('actors', models.TextField(null=True, verbose_name='Актеры')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
                ('poster', models.ImageField(null=True, upload_to='movies/movie_poster', verbose_name='Постер')),
                ('trailer', models.URLField(verbose_name='Трейлей')),
                ('start_date', models.DateField(verbose_name='Начало показа')),
                ('end_date', models.DateField(verbose_name='Конец показа')),
                ('price', models.IntegerField(verbose_name='Цена билета')),
                ('country', models.ManyToManyField(null=True, to='movies.Country', verbose_name='Страна')),
                ('genres', models.ManyToManyField(null=True, to='movies.Genre', verbose_name='Жанр')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.room', verbose_name='Зал')),
                ('start_time', models.ManyToManyField(null=True, to='movies.Time', verbose_name='Cеансы')),
            ],
            options={
                'verbose_name': 'Фильмы',
                'verbose_name_plural': 'Фильмы',
                'ordering': ('start_date',),
            },
        ),
    ]