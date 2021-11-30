from django.contrib import admin

from .models import Movie, Time, Genre, Country, Room


class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'ceahc', 'start_date', 'end_date')
    search_fields = ('title',)

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

    def ceahc(self, obj):
        return '\n'.join([str(start.time)[:-3] for start in obj.start_time.all()])

    def genre(self, obj):
        return '\n'.join([genre.name for genre in obj.genres.all()])


admin.site.register(Movie, MovieAdmin)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Genre, GenreAdmin)


class TimeAdmin(admin.ModelAdmin):
    list_display = ('time',)


admin.site.register(Time, TimeAdmin)


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Country, CountryAdmin)


class RoomAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Room, RoomAdmin)
