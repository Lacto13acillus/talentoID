from django.db import models
import user.models as user

class PlayerSearch(models.Model):
    id = models.CharField(max_length=60, primary_key=True, unique=True)
    nama_player = models.ForeignKey(user.user, on_delete=models.CASCADE )
    kata_kunci = models.CharField(max_length=255)
