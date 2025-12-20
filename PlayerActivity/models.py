# PlayerActivity/models.py
from django.db import models
import player.models as player

class PlayerActivity(models.Model):
    player = models.OneToOneField(
        player.player,
        on_delete=models.CASCADE,
        related_name="player_activities",
        primary_key=True
    )
    total_training_present = models.IntegerField(default=0)
    total_training_absent = models.IntegerField(default=0)
    total_training_unknown = models.IntegerField(default=0)
    total_match_present = models.IntegerField(default=0)
    total_match_absent = models.IntegerField(default=0)
    total_match_unknown = models.IntegerField(default=0)
    performance = models.CharField(max_length=50, blank=True)

    def calculate_performance(self):
        # Hitung total present, absent, dan unknown untuk semua aktivitas (training + match)
        total_present = self.total_training_present + self.total_match_present
        total_absent = self.total_training_absent + self.total_match_absent
        total_unknown = self.total_training_unknown + self.total_match_unknown

        # Tentukan performa berdasarkan aturan
        if total_present > (total_absent + total_unknown):
            self.performance = "Quite Good!"
        else:
            self.performance = "Keep Improving yourself!"
        self.save()