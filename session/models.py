from django.db import models
import player.models as player

class session (models.Model):
    session = models.CharField(primary_key=True, unique=True, max_length=255)
    player = models.ForeignKey(player.player, on_delete=models.CASCADE)
    session_type = models.CharField(max_length=60)
    minutes_date = models.DateField(default=0)
    notes = models.TextField(max_length=60)
