from django.db import models
import team.models as team
import schedule.models as schedule
import stadion.models as stadion
import TrainingCategory.models as TrainingCategory
import frequency.models as frequency

class training(models.Model):
    training = models.CharField(max_length=60, primary_key=True, unique=True)
    nama_latihan = models.CharField(max_length=200)
    tim = models.ForeignKey(team.team, on_delete=models.CASCADE)
    jadwal = models.ForeignKey(schedule.schedule, on_delete=models.CASCADE, null=True, blank=True)
    lokasi = models.ForeignKey(stadion.stadion, on_delete=models.CASCADE)
    kategori = models.ManyToManyField(TrainingCategory.trainingcategory, related_name="trainings")
    deskripsi = models.TextField(max_length=200)
    frequency = models.ForeignKey(frequency.frequency, on_delete=models.CASCADE, default="")
    date = models.DateField(default="2025-01-01")
    start_time = models.TimeField(default="00:00:00")
    end_time = models.TimeField(default="00:00:00")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
