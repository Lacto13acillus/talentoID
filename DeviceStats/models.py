from django.db import models
import player.models as player

class DeviceStats(models.Model):
    devicestats = models.CharField(max_length=60, primary_key=True, unique=True)
    pemain = models.ForeignKey(player.player, on_delete=models.CASCADE)
    jenis_perangkat = models.CharField(max_length=60) #jenis device yang digunakan
    metric = models.CharField(max_length=200) #jenis metrik misal (kecepatan, jarak tempuh, dsb)
    value = models.FloatField(default=0) #nilai metrik
    unit = models.CharField(max_length=60) #satuan pengukuran misal (km/h, meter, dsb)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
