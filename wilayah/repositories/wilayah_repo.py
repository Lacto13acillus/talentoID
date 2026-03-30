from wilayah.models import Provinsi, Kabupaten


class WilayahRepository:

    @staticmethod
    def get_all_provinsi():
        return Provinsi.objects.all().order_by("nama")

    @staticmethod
    def get_kabupaten_by_provinsi(kode_provinsi):
        return Kabupaten.objects.filter(provinsi_id=kode_provinsi).order_by("nama")
