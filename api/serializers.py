from rest_framework import serializers

from movies.models import Movie, Time, Genre, Country


class TimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Time
        fields = ('time',)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name',)


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ('name',)


class MovieSerializer(serializers.ModelSerializer):
    start_time = TimeSerializer(read_only=True, many=True)
    genres = GenreSerializer(read_only=True, many=True)
    room = serializers.StringRelatedField(read_only=True)
    country = CountrySerializer(read_only=True, many=True)

    class Meta:
        fields = ('title', 'country', 'year', 'director', 'actors', 'genres', 'description', 'trailer',
                  'room', 'start_time', 'start_date', 'end_date')
        model = Movie
