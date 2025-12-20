from django.db import models

class schedule(models.Model):
    schedule = models.CharField(max_length=60, primary_key=True, unique=True)
    tanggal = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
