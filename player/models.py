from django.db import models
import team.models as team
import user.models as user
from django.core.validators import FileExtensionValidator
from django.utils.timezone import now


class player(models.Model):
    user = models.ForeignKey(user.user, on_delete=models.CASCADE, default=0)
    player = models.CharField(max_length=60, primary_key=True, unique=True)
    nama = models.CharField(max_length=200)
    posisi = models.CharField(max_length=60)
    kewarganegaraan = models.CharField(max_length=60)
    tim = models.ForeignKey(team.team, on_delete=models.CASCADE)
    nomor_punggung = models.IntegerField(default=0)
    tinggi_badan = models.IntegerField(default=0)
    berat_badan = models.IntegerField(default=0)
    tanggal_gabung = models.DateField(default=now, null=False, blank=False)
    dob = models.DateField(default=now, null=False, blank=False)
    JENIS_KELAMIN_CHOICES = [
        ("L", "Laki-laki"),
        ("P", "Perempuan"),
    ]
    kelamin = models.CharField(
        max_length=1,
        choices=JENIS_KELAMIN_CHOICES,
        default="L",  # Nilai default jika tidak diisi
    )
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Verified", "Verified"),
        ("Cancelled", "Cancelled"),
        ("Rejected", "Rejected"),
    ]
    PAYMENT_CHOICES = [
        ("PENDING", "Pending"),
        ("PAID", "Paid"),
        ("SUCCEEDED", "Succeeded"),  # Biasanya untuk eWallet dan QRIS
        ("EXPIRED", "Expired"),
        ("FAILED", "Failed"),
        ("CANCELED", "Canceled"),
        ("SETTLED", "Settled"),
        ("REFUNDED", "Refunded"),
        ("VOIDED", "Voided"),
    ]

    verification_status = models.CharField(
        max_length=12,
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES[0][0],  # Nilai default jika tidak diisi
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default=PAYMENT_CHOICES[0][0],  # Nilai default jika tidak diisi
    )
    foto_profil = models.ImageField(
        upload_to="player/",  # Direktori penyimpanan gambar
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "gif"])
        ],
        null=True,
        blank=True,
    )

     # ✅ Tambahan field baru
    external_id = models.CharField(max_length=100, null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    invoice_url = models.URLField(null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    payment_method = models.CharField(max_length=100, null=True, blank=True)
    payment_channel = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
