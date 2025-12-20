from django.db import models

class season(models.Model):
    season = models.CharField(max_length=60, primary_key=True, unique=True)
    nama_season = models.CharField(max_length=60, unique=True)
    


