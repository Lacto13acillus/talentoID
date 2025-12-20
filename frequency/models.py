from django.db import models


class frequency(models.Model):
    frequency = models.CharField(max_length=60, primary_key=True, unique=True)
    STATUS_CHOICES = [
        ("One Time", "One Time"),
        ("Daily", "Daily"),
        ("Weekly", "Weekly"),
        ("Monthly", "Monthly"),
    ]
    frequency_time = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="Unknown"
    )
