from django.db import models

class Formation(models.Model):
    id_formasi = models.CharField(max_length=60, primary_key=True, unique=True)
    formasi = models.CharField(max_length=10)  