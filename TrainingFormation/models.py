from django.db import models
import formations.models as formations
import LineUp.models as lineup

class trainingformation(models.Model):
    id_trainingformation = models.CharField(max_length=60, primary_key=True, unique=True)
    id_formations = models.ForeignKey(formations.Formation, on_delete=models.CASCADE)
    id_lineup = models.ManyToManyField(lineup.LineUp,) 
