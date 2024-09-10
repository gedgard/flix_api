from django.db import models
from actors.models import Actor
from genres.models import Genre

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=255)
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT, related_name= 'movies') # related_name dá um nome para a relação inversa, como usar genres.objects.movies.all()
    release_date = models.DateField(null=True, blank=True)
    actors = models.ManyToManyField(Actor, related_name='movies')
    resume = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
    
