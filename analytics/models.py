from django.db import models
import team.models as tm

class analytics(models.Model):
    analytics = models.CharField(max_length=60, primary_key=True, unique=True, default=0)
    tim = models.ForeignKey(tm.team, on_delete=models.CASCADE )
    kick_test = models.FloatField()  # Menyimpan skor Kick Test (misal: 20.5)
    tactical = models.FloatField()   # Menyimpan nilai Tactical (misal: 50.0)
    shoot_focus = models.FloatField()  # Menyimpan nilai Shoot Focus (misal: 30.5)
    analyst = models.FloatField()    # Menyimpan nilai Analyst (misal: 25.0)
