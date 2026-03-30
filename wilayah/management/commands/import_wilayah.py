import csv
import os

from django.core.management.base import BaseCommand
from wilayah.models import Provinsi, Kabupaten
from django.conf import settings

BASE_DIR = settings.BASE_DIR

provinsi_file = os.path.join(BASE_DIR, "data", "provinsi.csv")
kabupaten_file = os.path.join(BASE_DIR, "data", "kabupaten.csv")


class Command(BaseCommand):
    help = "Import data wilayah Dukcapil (Provinsi & Kabupaten)"

    def handle(self, *args, **kwargs):
        self.import_provinsi()
        self.import_kabupaten()
        self.stdout.write(self.style.SUCCESS("Import selesai!"))

    def import_provinsi(self):
        with open(provinsi_file, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                Provinsi.objects.update_or_create(
                    kode=row["kode"], defaults={"nama": row["nama"]}
                )
        self.stdout.write(self.style.SUCCESS("Provinsi berhasil diimport"))

    def import_kabupaten(self):
        with open(kabupaten_file, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    provinsi = Provinsi.objects.get(kode=row["kode_provinsi"])

                    Kabupaten.objects.update_or_create(
                        kode=row["kode"],
                        defaults={"nama": row["nama"], "provinsi": provinsi},
                    )

                except Provinsi.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Provinsi tidak ditemukan: {row['kode_provinsi']}"
                        )
                    )

        self.stdout.write(self.style.SUCCESS("Kabupaten berhasil diimport"))
