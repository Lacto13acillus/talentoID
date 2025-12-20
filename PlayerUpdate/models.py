from django.db import models
import player.models as player

class PlayerUpdate(models.Model):
    playerupdate = models.CharField(max_length=60, primary_key=True, unique=True)
    pemain = models.ForeignKey(player.player, on_delete=models.CASCADE, default='')
    judul_update = models.CharField(max_length=60)
    deskripsi = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
