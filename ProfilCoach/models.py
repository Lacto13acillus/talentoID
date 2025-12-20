from django.db import models
import user.models as user


class ProfilCoach(models.Model):
    user = models.OneToOneField(user.user, on_delete=models.CASCADE)
    coach = models.CharField(max_length=60, primary_key=True, unique=True)
    # nama_coach = models.CharField(max_length=60, default="")
    tanggal_bergabung = models.DateField()
    tanggal_lahir = models.DateField()
    kewarganegaraan = models.CharField(max_length=60)
    tinggi_badan = models.IntegerField(default=0)
    berat_badan = models.IntegerField(default=0)
    # foto_profil = models.ImageField(
    #     upload_to="profilcoach/",  # Direktori penyimpanan gambar
    #     validators=[
    #         FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "gif"])
    #     ],
    #     blank=True,
    #     default="",
    # )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
