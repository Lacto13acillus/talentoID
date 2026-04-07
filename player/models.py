from django.db import models
import team.models as team
import user.models as user
from django.core.validators import FileExtensionValidator
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta
from datetime import timedelta
from wilayah.models import Kabupaten


class player(models.Model):

    user = models.ForeignKey(user.user, on_delete=models.CASCADE, default=0)
    player = models.CharField(max_length=60, primary_key=True, unique=True)

    nama = models.CharField(max_length=200)
    posisi = models.CharField(max_length=60)
    tim = models.ForeignKey(team.team, on_delete=models.CASCADE)

    nomor_punggung = models.IntegerField(default=0)
    tinggi_badan = models.IntegerField(default=0)
    berat_badan = models.IntegerField(default=0)

    tanggal_gabung = models.DateField(default=now)
    dob = models.DateField(default=now)

    JENIS_KELAMIN_CHOICES = [
        ("L", "Laki-laki"),
        ("P", "Perempuan"),
    ]

    kelamin = models.CharField(
        max_length=1,
        choices=JENIS_KELAMIN_CHOICES,
        default="L",
    )

    kabupaten = models.ForeignKey(
        Kabupaten,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="players",
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
        ("SUCCEEDED", "Succeeded"),
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
        default="Pending",
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default="PENDING",
    )

    foto_profil = models.ImageField(
        upload_to="player/",
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "gif"])
        ],
        null=True,
        blank=True,
    )

    # 🔹 Payment Fields
    external_id = models.CharField(max_length=100, null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    invoice_url = models.URLField(null=True, blank=True)

    paid_at = models.DateTimeField(null=True, blank=True)
    payment_method = models.CharField(max_length=100, null=True, blank=True)
    payment_channel = models.CharField(max_length=100, null=True, blank=True)

    # 🔹 Membership Expiry
    end_date = models.DateTimeField(null=True, blank=True)

    # 🔹 Track if this is first payment or renewal
    is_first_payment = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 🔥 SAVE LOGIC (SIMPLER VERSION)
    def save(self, *args, **kwargs):
        current_time = now()

        is_paid = self.payment_status in ["PAID", "SUCCEEDED", "SETTLED"]

        # =========================
        # CASE 1: NEW OBJECT
        # =========================
        if not self.pk:
            if is_paid and self.paid_at:
                self.end_date = self.paid_at + relativedelta(months=1)

        # =========================
        # CASE 2: UPDATE OBJECT
        # =========================
        else:
            try:
                old_instance = player.objects.get(pk=self.pk)

                old_payment_status = old_instance.payment_status
                old_payment_not_paid = old_payment_status not in [
                    "PAID",
                    "SUCCEEDED",
                    "SETTLED",
                ]

                new_payment_is_paid = is_paid

                if old_payment_not_paid and new_payment_is_paid and self.paid_at:

                    # expired / new
                    if not self.end_date or self.end_date <= current_time:
                        self.end_date = self.paid_at + relativedelta(months=1)

                    # renewal
                    elif self.end_date > current_time:
                        self.end_date = self.end_date + relativedelta(months=1)

            except player.DoesNotExist:
                pass

        super().save(*args, **kwargs)

    # 🔥 REALTIME MEMBERSHIP STATUS
    @property
    def membership_status(self):

        if not self.end_date:
            return "EXPIRED"

        current_time = now()

        if current_time <= self.end_date:
            return "ACTIVE"
        elif current_time <= self.end_date + timedelta(days=7):
            return "GRACE"
        return "EXPIRED"

    # =========================
    # 🔥 WILAYAH HELPERS
    # =========================

    @property
    def kabupaten_kode(self):
        if self.kabupaten:
            return self.kabupaten.kode
        if self.tim and self.tim.kabupaten:
            return self.tim.kabupaten.kode
        return None

    @property
    def kabupaten_name(self):
        if self.kabupaten:
            return self.kabupaten.nama
        if self.tim and self.tim.kabupaten:
            return self.tim.kabupaten.nama
        return None

    @property
    def provinsi_kode(self):
        if self.kabupaten and self.kabupaten.provinsi:
            return self.kabupaten.provinsi.kode
        if self.tim and self.tim.kabupaten and self.tim.kabupaten.provinsi:
            return self.tim.kabupaten.provinsi.kode
        return None

    @property
    def provinsi_name(self):
        if self.kabupaten and self.kabupaten.provinsi:
            return self.kabupaten.provinsi.nama
        if self.tim and self.tim.kabupaten and self.tim.kabupaten.provinsi:
            return self.tim.kabupaten.provinsi.nama
        return None

    def __str__(self):
        return f"{self.nama} ({self.player})"
