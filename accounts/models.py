from django.db import models

# Create your models here.

class Lyrics(models.Model):
    title = CharField(max_length=20)
    lyrics = CharField()
    author = CharField(max_length=20)
    