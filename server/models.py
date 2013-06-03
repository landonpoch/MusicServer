from django.db import models

# Create your models here.
class Library(models.Model):
    name = models.CharField(max_length=256)
    path = models.CharField(max_length=256)

class Artist(models.Model):
    name = models.CharField(max_length=256) 

class Album(models.Model):
    name = models.CharField(max_length=256)
    artist = models.ForeignKey(Artist)

class Song(models.Model):
    name = models.CharField(max_length=256)
    track = models.PositiveSmallIntegerField(default=None, blank=True, null=True)
    album = models.ForeignKey(Album)
    library = models.ForeignKey(Library) 
