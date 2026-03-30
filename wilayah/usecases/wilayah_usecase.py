from wilayah.repositories.wilayah_repo import WilayahRepository


class WilayahUsecase:

    @staticmethod
    def get_provinsi():
        data = WilayahRepository.get_all_provinsi()

        return [{"kode": item.kode, "nama": item.nama} for item in data]

    @staticmethod
    def get_kabupaten(kode_provinsi):
        data = WilayahRepository.get_kabupaten_by_provinsi(kode_provinsi)

        return [
            {"kode": item.kode, "nama": item.nama, "provinsi": item.provinsi.kode}
            for item in data
        ]
