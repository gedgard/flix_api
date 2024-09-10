from django.db.models import Avg
from rest_framework import serializers
from movies.models import Movie
from datetime import date
from genres.models import Genre
from genres.serializers import GenreSerializer
from actors.models import Actor
from actors.serializers import ActorSerializer


class MovieModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'


    # a função deve ter o nome validate_campotabela)
    def validate_release_date(self, value):
        if value.year < 1930:
            raise serializers.ValidationError('Data de lançamento não pode ser anterior a 1930')

        if value > date.today():
            raise serializers.ValidationError('Data de lançamento não pode ser posterior a hoje')

        return value

    def validate_resume(self, value):
        if len(value) > 300:
            raise serializers.ValidationError('O resumo não pode ter mais de 300 caracteres')
        return value


class MovieListDetailSerializer(serializers.ModelSerializer):
    actors = ActorSerializer(many=True)
    genre = GenreSerializer()
    rate = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'genre', 'actors', 'release_date', 'rate', 'resume']

    # metodo get para calcular algo
    def get_rate(self, obj):
        rate =  obj.reviews.aggregate(Avg('stars'))['stars__avg']

        if rate:
            return round(rate, 1)

        return None
