from django.db import models
import formations.models as formations

class MatchFormations(models.Model):
    id_matchformations = models.CharField(max_length=60, primary_key=True, unique=True)
    id_formations = models.ForeignKey(formations.Formation, on_delete=models.CASCADE) 
