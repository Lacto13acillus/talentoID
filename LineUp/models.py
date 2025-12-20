# models/lineup.py
from django.db import models
import player.models as player
import pertandingan.models as pertandingan

class LineUp(models.Model):
    id_lineup = models.CharField(max_length=60, primary_key=True, unique=True)
    match = models.ForeignKey(pertandingan.pertandingan, on_delete=models.CASCADE, default="")
    player = models.ForeignKey(player.player, on_delete=models.CASCADE)
    index = models.IntegerField(choices=[(i, str(i)) for i in range(12)], default=0)
    STATUS_CHOICES = [
        ('main', 'Main'),
        ('reserve', 'Reserve'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='main')
