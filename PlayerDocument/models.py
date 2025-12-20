from django.db import models
import player.models as player
from django.core.validators import FileExtensionValidator

class PlayerDocument(models.Model):
    playerdocument = models.CharField(max_length=60, primary_key=True, unique=True)
    pemain = models.ForeignKey(player.player, on_delete=models.CASCADE, default="")
    jenis_dokumen = models.CharField(max_length=60)
    file_dokumen = models.FileField(
        upload_to='PlayerDocument/',  # Direktori penyimpanan gambar
        validators=[FileExtensionValidator(allowed_extensions=['jpeg','png', 'pdf', 'doc'])],
        blank=True, 
        default=""     
    )