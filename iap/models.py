from django.db import models
import player.models as player
import pertandingan.models as pertandingan

class iap(models.Model):
    IAP_CATEGORY_CHOICES = [
        ('Technical', 'Technical'),
        ('Physical', 'Physical'),
        ('Goalkeeper', 'goalkeeper'),
        ('Social', 'social')
    ]

    IAP_TYPE_CHOICES = [
        ('Passing', 'Passing'),
        ('Dribbling', 'Dribbling'),
        ('Heading', 'Heading'),
        ('Ball Control', 'Ball Control'),
        ('Tackling', 'Tackling'),
        ('Shooting', 'Shooting'),
    ]

    iap = models.CharField(primary_key=True, unique=True, default=0, max_length=255)
    match = models.ForeignKey(pertandingan.pertandingan, on_delete=models.CASCADE, default="")
    player = models.ForeignKey(player.player, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=IAP_CATEGORY_CHOICES)
    type = models.CharField(max_length=50, choices=IAP_TYPE_CHOICES)
    current_achieve = models.IntegerField(default=0)
    target = models.IntegerField(default=0)
