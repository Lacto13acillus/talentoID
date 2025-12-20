from django.db import models
import player.models as player
import training.models as training

class iaptraining(models.Model):
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

    iaptraining = models.CharField(primary_key=True, unique=True, default=0, max_length=60)
    training = models.ForeignKey(training.training, on_delete=models.CASCADE)
    player = models.ForeignKey(player.player, on_delete=models.CASCADE, related_name="iaptraining_records")
    category = models.CharField(max_length=20, choices=IAP_CATEGORY_CHOICES)
    type = models.CharField(max_length=50, choices=IAP_TYPE_CHOICES)
    current_achieve = models.IntegerField(default=0)
    target = models.IntegerField(default=0)
