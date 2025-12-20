from django.db import models
import player.models as player

class PlayerPerform(models.Model):
    playerperform = models.CharField(max_length=60, primary_key=True, unique=True)
    player = models.ForeignKey(player.player, on_delete=models.CASCADE, default='')
    kick_test = models.FloatField(default=0.0)  # Menyimpan skor Kick Test (misal: 20.5)
    tactical = models.FloatField(default=0.0)   # Menyimpan nilai Tactical (misal: 50.0)
    shoot_focus = models.FloatField(default=0.0)  # Menyimpan nilai Shoot Focus (misal: 30.5)
    analyst = models.FloatField(default=0.0)    # Menyimpan nilai Analyst (misal: 25.0)
    shoot = models.FloatField(default=0.0)

class Meta:
        unique_together = ('player',)  # Pastikan hanya ada satu PlayerPerform per pemain