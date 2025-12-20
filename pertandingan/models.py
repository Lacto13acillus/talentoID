from django.db import models
import team.models as team
import schedule.models as schedule
import stadion.models as stadion
import status.models as status
import formations.models as formations
import season.models as season
from django.core.exceptions import ObjectDoesNotExist

def get_default_status():
    try:
        return status.status.objects.get(match_status='Preparing')
    except ObjectDoesNotExist:
        return None

class pertandingan(models.Model):
    match = models.CharField(max_length=60, primary_key=True, unique=True)
    nama_pertandingan = models.CharField(max_length=200)
    tim_home = models.ForeignKey(team.team, on_delete=models.CASCADE, related_name="home_team")
    tim_away = models.ForeignKey(team.team, on_delete=models.CASCADE, related_name="away_team")
    formasi = models.ForeignKey(formations.Formation, on_delete=models.CASCADE, related_name="home_formation", null=True, blank=True)
    jadwal = models.ForeignKey(schedule.schedule, on_delete=models.CASCADE, null=True, blank=True)
    lokasi = models.ForeignKey(stadion.stadion, on_delete=models.CASCADE)
    status = models.ForeignKey(status.status, on_delete=models.CASCADE, default=get_default_status)
    season = models.ForeignKey(season.season, on_delete=models.CASCADE, default="")
    date = models.DateField(default="2025-01-01")
    start_time = models.TimeField(default="00:00:00")
    end_time = models.TimeField(default="00:00:00")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
