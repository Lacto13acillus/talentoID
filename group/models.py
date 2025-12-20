from django.db import models
import team.models as team
import user.models as user

class group(models.Model):
    id = models.CharField(max_length=60, primary_key=True, unique=True)
    nama_group = models.CharField(max_length=60)
    tim = models.ForeignKey(team.team, on_delete=models.CASCADE)
    anggota = models.ForeignKey(user.user, on_delete=models.CASCADE)
