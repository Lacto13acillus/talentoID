# MatchAttendance/models.py
from django.db import models
import player.models as player
import pertandingan.models as pertandingan

class MatchAttendance(models.Model):
    match_attendance = models.CharField(max_length=60, primary_key=True, unique=True)
    player = models.ForeignKey(
        player.player,
        on_delete=models.CASCADE,
        related_name="match_attendances"
    )
    match = models.ForeignKey(
        pertandingan.pertandingan,
        on_delete=models.CASCADE,
        related_name="match_attendances",
        null=True,
        blank=True 
    )
    STATUS_CHOICES = [
        ('Present', 'present'),
        ('Absent', 'absent'),
        ('Unknown', 'unknown'),
    ]
    attendance_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Unknown'
    )
    notes = models.TextField(null=True, blank=True)