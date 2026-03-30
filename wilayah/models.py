from django.db import models


class Provinsi(models.Model):
    kode = models.CharField(max_length=2, primary_key=True)  # kode Dukcapil
    nama = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nama} ({self.kode})"


class Kabupaten(models.Model):
    kode = models.CharField(max_length=4, primary_key=True)  # kode Dukcapil
    nama = models.CharField(max_length=100)

    provinsi = models.ForeignKey(
        Provinsi, on_delete=models.CASCADE, related_name="kabupaten"
    )

    def __str__(self):
        return f"{self.nama} ({self.kode})"
