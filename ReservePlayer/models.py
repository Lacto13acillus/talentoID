from django.db import models
import player.models as player

class ReservePlayer(models.Model):
    id_reserve_player = models.CharField(max_length=60, primary_key=True, unique=True)
    
    
