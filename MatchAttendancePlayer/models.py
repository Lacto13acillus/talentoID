from django.db import models
import player.models as player
import pertandingan.models as pertandingan


class MatchAttendancePlayer(models.Model):
    attendance_id = models.CharField(max_length=60, primary_key=True, unique=True)
    player = models.ForeignKey(
        player.player,
        on_delete=models.CASCADE,
        related_name="player_attendances"
    )
    match = models.ForeignKey(
        pertandingan.pertandingan,
        on_delete=models.CASCADE,
        related_name="player_attendances",
        null=True,
        blank=True
    )
    status = models.BooleanField(
        default=True,
        help_text="True if the player is present, False if absent."
    )
    reason_absent = models.TextField(
        null=True,
        blank=True,
        help_text="Reason for absence, mandatory if the player is absent."
    )
