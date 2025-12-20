from django.db import models
import player.models as player
import pertandingan.models as pertandingan
from django.core.validators import MinValueValidator, MaxValueValidator

class stats (models.Model):
    stats = models.CharField(max_length=60, primary_key=True, unique=True)
    match = models.ForeignKey(pertandingan.pertandingan, on_delete=models.CASCADE, null=False, blank=False)
    player = models.ForeignKey(player.player, on_delete=models.CASCADE)
    position_played = models.CharField(max_length=60)
    minutes_played = models.IntegerField(default=0)
    overall_rating = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])

