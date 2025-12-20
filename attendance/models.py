from django.db import models
import training.models as training
import player.models as player

class attendance(models.Model):
    attendance = models.CharField(max_length=60, primary_key=True, unique=True)
    player = models.ForeignKey(player.player, on_delete=models.CASCADE, related_name="training_attendances")
    training = models.ForeignKey(
        training.training,
        on_delete=models.CASCADE,
        related_name="attendances",
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
