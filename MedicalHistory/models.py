from django.db import models
import player.models as player
from django.core.validators import FileExtensionValidator

class MedicalHistory(models.Model):
    medicalhistory = models.CharField(max_length=60, primary_key=True, unique=True)
    pemain = models.ForeignKey(player.player, on_delete=models.CASCADE)
    jenis_pemeriksaan = models.CharField(max_length=60)
    file_dokumen = models.FileField(
        upload_to='MedicalHistory/',  # Direktori penyimpanan gambar
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc'])],
        blank=True, 
        default=""     
    )
