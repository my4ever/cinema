import datetime
from django.db import models


class Time(models.Model):
    time = models.TimeField(verbose_name='Сеанс')

    class Meta:
        verbose_name = 'Сеанс'
        verbose_name_plural = 'Сеансы'
        ordering = ('time',)

    def __str__(self):
        return f'{str(self.time)[:-3]}'


class Genre(models.Model):
    name = models.CharField(max_length=30, verbose_name='Жанр')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=15, verbose_name='Зал')

    class Meta:
        verbose_name = 'Зал'
        verbose_name_plural = 'Зал'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=50, verbose_name='Страна')

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    country = models.ManyToManyField(Country, verbose_name='Страна')
    year = models.IntegerField(default=str(datetime.datetime.now().year), verbose_name='Год')
    director = models.CharField(max_length=70, verbose_name='Режисёр')
    actors = models.TextField(verbose_name='Актеры')
    genres = models.ManyToManyField(Genre, verbose_name='Жанр')
    description = models.TextField(verbose_name='Описание', null=True)
    poster = models.ImageField(upload_to='movies/movie_poster', verbose_name='Постер', null=True)
    trailer = models.URLField(verbose_name='Трейлей')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='Зал')
    start_time = models.ManyToManyField(Time, verbose_name='Cеансы')
    start_date = models.DateField(verbose_name='Начало показа')
    end_date = models.DateField(verbose_name='Конец показа')
    price = models.IntegerField(verbose_name='Цена билета')

    def __str__(self):
        return f'{self.title} c {self.start_date} до {self.end_date}'

    class Meta:
        verbose_name = 'Фильмы'
        verbose_name_plural = 'Фильмы'
        ordering = ('start_date',)
