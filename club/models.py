from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.

class club(models.Model):
	club = models.CharField(max_length=50,primary_key=True, unique=True)
	club_name = models.CharField(max_length=255, unique=True)
	club_logo = models.ImageField(
        upload_to='club/',  # Direktori penyimpanan gambar
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])],
        blank=True,
        default=""
    )
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
