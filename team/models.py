from django.db import models
from django.core.validators import FileExtensionValidator
from wilayah.models import Kabupaten

# import ProfilCoach.models as ProfilCoach
# import club.models as club


class team(models.Model):
    team = models.CharField(max_length=60, primary_key=True, unique=True)
    nama_team = models.CharField(max_length=60, unique=True)
    coach = models.ForeignKey(
        "ProfilCoach.ProfilCoach", on_delete=models.CASCADE, default=""
    )
    # club = models.ForeignKey(
    #     "club.club",
    #     on_delete=models.CASCADE,
    #     null=True,  # izinkan NULL di database
    #     blank=True,  # izinkan kosong di form/admin
    #     default=True,  # default-nya adalah None (null))
    # )
    kategori_team = models.CharField(max_length=60)

    kabupaten = models.ForeignKey(
        Kabupaten,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="teams",
    )

    logo_team = models.ImageField(
        upload_to="team/",  # Direktori penyimpanan gambar
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "gif"])
        ],
        blank=True,
        default="",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
