from django.db import models

class trainingcategory(models.Model):
    trainingcategory = models.CharField(max_length=60, primary_key=True, unique=True)
    nama_category = models.CharField(max_length=60)
