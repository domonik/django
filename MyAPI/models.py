from django.db import models

# Create your models here.

# model of genearated lyrics 
class Lyrics(models.Model):
    title = models.CharField(max_length=20)
    lyrics = models.CharField(max_length=300)
    author = models.CharField(max_length=20)
