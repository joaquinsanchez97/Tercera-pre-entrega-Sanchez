from django.db import models

class Pokemon(models.Model):
    nivel = models.IntegerField()
    nombre = models.CharField(max_length=20)
    mote = models.CharField(max_length=20)

# Create your models here.
