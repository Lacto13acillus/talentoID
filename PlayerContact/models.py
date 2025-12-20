from django.db import models
import player.models as player

class PlayerContact(models.Model):
    playercontact = models.CharField(max_length=60, primary_key=True, unique=True)
    pemain = models.ForeignKey(player.player, on_delete=models.CASCADE, default="")
    nama_panggilan = models.CharField(max_length=20)
    nomor_hp = models.CharField(max_length=12)
    nama_orangtua = models.CharField(max_length=60)
    nomor_orangtua = models.CharField(max_length=12)
    nama_kontak_darurat = models.CharField(max_length=60, default="")
    kontak_darurat = models.CharField(max_length=12)
