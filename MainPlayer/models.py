from django.db import models
import player.models as player

class MainPlayer(models.Model):
    id_main_player = models.CharField(max_length=60, primary_key=True, unique=True)
    
    
