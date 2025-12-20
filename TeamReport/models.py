from django.db import models
import team.models as team
import schedule.models as schedule 

class TeamReport(models.Model):
    teamreport = models.CharField(max_length=60, primary_key=True, unique=True)
    tim = models.ForeignKey(team.team, on_delete=models.CASCADE)
    jadwal = models.ForeignKey(schedule.schedule, on_delete=models.CASCADE)
    hasil_pertandingan = models.CharField(max_length=60)
    catatan = models.TextField(max_length=200)
