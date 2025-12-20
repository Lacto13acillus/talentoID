from django.db import models

class stadion(models.Model):
    stadion = models.CharField(max_length=60, primary_key=True, unique=True)
    nama_stadion = models.CharField(max_length=60, unique=True)
    lokasi = models.CharField(max_length=200)
