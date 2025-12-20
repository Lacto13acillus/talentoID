from django.db import models

class status(models.Model):
    status = models.CharField(max_length=60, primary_key=True, unique=True)
    STATUS_CHOICES = [
        ('Preparing', 'preparing'),
		('Ready', 'ready'),
        ('Finished', 'finished')
    ]
    match_status = models.CharField(max_length=60, choices=STATUS_CHOICES, default="")
