from django.db import models
import training.models as training
from django.core.validators import FileExtensionValidator


class FootprintCategory(models.Model):
    category = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.category


class footprint(models.Model):
    footprint = models.CharField(max_length=60, primary_key=True, unique=True)

    training = models.ForeignKey(training.training, on_delete=models.CASCADE)

    category = models.ForeignKey("FootprintCategory", on_delete=models.CASCADE)

    # 🔥 hanya video
    media = models.FileField(
        upload_to="footprint/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "mp4",
                    "avi",
                    "mov",
                    "mkv",
                ]
            )
        ],
        blank=True,
        null=True,
        default=None,
    )

    # 🔥 URL hasil proses (misalnya setelah upload / processing)
    media_after = models.URLField(max_length=500, blank=True, null=True)

    # 🔥 nullable boolean
    hasJerseyNumber = models.BooleanField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
