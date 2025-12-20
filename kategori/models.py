from django.db import models

class kategori(models.Model):
    kategori_id = models.CharField(primary_key=True, max_length=60, unique=True )
    nama_kategori = models.TextField(max_length=60)
