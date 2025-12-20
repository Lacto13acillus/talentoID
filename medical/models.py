from django.db import models
import player.models as player
import MedicalHistory.models as MedicalHistory
import session.models as session

class medical (models.Model):
    medical = models.CharField(primary_key=True, unique=True, max_length=255)
    player = models.ForeignKey(player.player, on_delete=models.CASCADE)
    medical_history = models.ForeignKey(MedicalHistory.MedicalHistory, on_delete=models.CASCADE)
    session = models.ForeignKey(session.session, on_delete=models.CASCADE)
