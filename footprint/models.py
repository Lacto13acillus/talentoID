from django.db import models
import training.models as training
from django.core.validators import FileExtensionValidator

class footprint(models.Model):
    footprint = models.CharField(max_length=60, primary_key=True, unique=True)
    training = models.ForeignKey(training.training, on_delete=models.CASCADE)
    media = models.FileField(
        upload_to='footprint/',  # Direktori penyimpanan gambar
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'mp4', 'avi', 'mov', 'mkv'])],
        blank=True,
        default=""
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
