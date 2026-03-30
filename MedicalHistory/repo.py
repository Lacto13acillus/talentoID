# repository/medical_history_repository.py
from django.shortcuts import get_object_or_404
from .models import MedicalHistory
from player.models import player
from django.core.exceptions import ValidationError


class RepoMedicalHistory:
    @staticmethod
    def post(req):
        Pemain = get_object_or_404(player, player=req["player"])

        # Validasi file
        if "file_dokumen" in req and req["file_dokumen"]:
            file_dokumen = req["file_dokumen"]
            if file_dokumen.name.split(".")[-1].lower() not in ["pdf", "doc"]:
                raise ValidationError(
                    "Invalid file format. Only PDF and DOC are allowed."
                )

        new_medical_history = MedicalHistory.objects.create(
            medicalhistory=req["medicalhistory"],
            pemain=Pemain,
            jenis_pemeriksaan=req["jenis_pemeriksaan"],
            file_dokumen=req.get("file_dokumen", None),
        )
        return {
            "medicalhistory": new_medical_history.medicalhistory,
            "player": {
                "player": Pemain.player,
                "nama": Pemain.nama,
                "posisi": Pemain.posisi,
                "usia": Pemain.usia,
                "team": {
                    "team": Pemain.tim.team if Pemain.tim else None,
                    "nama_team": Pemain.tim.nama_team if Pemain.tim else None,
                    "kategori_team": Pemain.tim.kategori_team if Pemain.tim else None,
                    "logo_team": (
                        Pemain.tim.logo_team.url
                        if Pemain.tim and Pemain.tim.logo_team
                        else None
                    ),
                },
                "nomor_punggung": Pemain.nomor_punggung,
                "tinggi_badan": Pemain.tinggi_badan,
                "berat_badan": Pemain.berat_badan,
                "tanggal_gabung": Pemain.tanggal_gabung,
                "kelamin": Pemain.kelamin,
                "foto_profil": Pemain.foto_profil.url if Pemain.foto_profil else None,
            },
            "jenis_pemeriksaan": new_medical_history.jenis_pemeriksaan,
            "file_dokumen": (
                new_medical_history.file_dokumen.url
                if new_medical_history.file_dokumen
                else None
            ),
        }

    @staticmethod
    def get(medical_history_id):
        medical_history_data = get_object_or_404(
            MedicalHistory, medicalhistory=medical_history_id
        )
        return {
            "medicalhistory": medical_history_data.medicalhistory,
            "player": {
                "player": medical_history_data.pemain.player,
                "nama": medical_history_data.pemain.nama,
                "posisi": medical_history_data.pemain.posisi,
                "usia": medical_history_data.pemain.usia,
                "team": {
                    "team": (
                        medical_history_data.pemain.tim.team
                        if medical_history_data.pemain.tim
                        else None
                    ),
                    "nama_team": (
                        medical_history_data.pemain.tim.nama_team
                        if medical_history_data.pemain.tim
                        else None
                    ),
                    "kategori_team": (
                        medical_history_data.pemain.tim.kategori_team
                        if medical_history_data.pemain.tim
                        else None
                    ),
                    "logo_team": (
                        medical_history_data.pemain.tim.logo_team.url
                        if medical_history_data.pemain.tim
                        and medical_history_data.pemain.tim.logo_team
                        else None
                    ),
                },
                "nomor_punggung": medical_history_data.pemain.nomor_punggung,
                "tinggi_badan": medical_history_data.pemain.tinggi_badan,
                "berat_badan": medical_history_data.pemain.berat_badan,
                "tanggal_gabung": medical_history_data.pemain.tanggal_gabung,
                "kelamin": medical_history_data.pemain.kelamin,
                "foto_profil": (
                    medical_history_data.pemain.foto_profil.url
                    if medical_history_data.pemain.foto_profil
                    else None
                ),
            },
            "jenis_pemeriksaan": medical_history_data.jenis_pemeriksaan,
            "file_dokumen": (
                medical_history_data.file_dokumen.url
                if medical_history_data.file_dokumen
                else None
            ),
        }

    @staticmethod
    def get_all():
        medical_histories = MedicalHistory.objects.all()
        return [
            {
                "medicalhistory": history.medicalhistory,
                "player": {
                    "player": history.pemain.player,
                    "nama": history.pemain.nama,
                    "posisi": history.pemain.posisi,
                    "usia": history.pemain.usia,
                    "kewarganegaraan": history.pemain.kewarganegaraan,
                    "team": {
                        "team": history.pemain.tim.team if history.pemain.tim else None,
                        "nama_team": (
                            history.pemain.tim.nama_team if history.pemain.tim else None
                        ),
                        "kategori_team": (
                            history.pemain.tim.kategori_team
                            if history.pemain.tim
                            else None
                        ),
                        "logo_team": (
                            history.pemain.tim.logo_team.url
                            if history.pemain.tim and history.pemain.tim.logo_team
                            else None
                        ),
                    },
                    "nomor_punggung": history.pemain.nomor_punggung,
                    "tinggi_badan": history.pemain.tinggi_badan,
                    "berat_badan": history.pemain.berat_badan,
                    "tanggal_gabung": history.pemain.tanggal_gabung,
                    "kelamin": history.pemain.kelamin,
                    "foto_profil": (
                        history.pemain.foto_profil.url
                        if history.pemain.foto_profil
                        else None
                    ),
                },
                "jenis_pemeriksaan": history.jenis_pemeriksaan,
                "file_dokumen": (
                    history.file_dokumen.url if history.file_dokumen else None
                ),
            }
            for history in medical_histories
        ]

    @staticmethod
    def get_by_player(player_id):
        Pemain = get_object_or_404(player, player=player_id)
        medical_histories = MedicalHistory.objects.filter(pemain=Pemain)
        result = []
        for history in medical_histories:
            try:
                result.append(
                    {
                        "medicalhistory": history.medicalhistory,
                        "player": {
                            "player": history.pemain.player,
                            "nama": history.pemain.nama,
                            "posisi": history.pemain.posisi,
                            "usia": history.pemain.usia,
                            "kewarganegaraan": history.pemain.kewarganegaraan,
                            "team": {
                                "team": (
                                    history.pemain.tim.team
                                    if history.pemain.tim
                                    else None
                                ),
                                "nama_team": (
                                    history.pemain.tim.nama_team
                                    if history.pemain.tim
                                    else None
                                ),
                                "kategori_team": (
                                    history.pemain.tim.kategori_team
                                    if history.pemain.tim
                                    else None
                                ),
                                "logo_team": (
                                    history.pemain.tim.logo_team.url
                                    if history.pemain.tim
                                    and history.pemain.tim.logo_team
                                    else None
                                ),
                            },
                            "nomor_punggung": history.pemain.nomor_punggung,
                            "tinggi_badan": history.pemain.tinggi_badan,
                            "berat_badan": history.pemain.berat_badan,
                            "tanggal_gabung": history.pemain.tanggal_gabung,
                            "kelamin": history.pemain.kelamin,
                            "foto_profil": (
                                history.pemain.foto_profil.url
                                if history.pemain.foto_profil
                                else None
                            ),
                        },
                        "jenis_pemeriksaan": history.jenis_pemeriksaan,
                        "file_dokumen": (
                            history.file_dokumen.url if history.file_dokumen else None
                        ),
                    }
                )
            except Exception as e:
                print(
                    f"Error processing medical history {history.medicalhistory}: {str(e)}"
                )
                continue
        return result

    @staticmethod
    def put(req):
        MedicalHistoryData = get_object_or_404(
            MedicalHistory, medicalhistory=req["medicalhistory"]
        )
        Pemain = get_object_or_404(player, player=req["player"])

        MedicalHistoryData.pemain = Pemain
        MedicalHistoryData.jenis_pemeriksaan = req.get(
            "jenis_pemeriksaan", MedicalHistoryData.jenis_pemeriksaan
        )

        if "file_dokumen" in req and req["file_dokumen"]:
            file_dokumen = req["file_dokumen"]
            if file_dokumen.name.split(".")[-1].lower() not in ["pdf", "doc"]:
                raise ValidationError(
                    "Invalid file format. Only PDF and DOC are allowed."
                )
            MedicalHistoryData.file_dokumen = file_dokumen

        MedicalHistoryData.save()

        return {
            "medicalhistory": MedicalHistoryData.medicalhistory,
            "player": {
                "player": Pemain.player,
                "nama": Pemain.nama,
                "posisi": Pemain.posisi,
                "usia": Pemain.usia,
                "kewarganegaraan": Pemain.kewarganegaraan,
                "team": {
                    "team": Pemain.tim.team if Pemain.tim else None,
                    "nama_team": Pemain.tim.nama_team if Pemain.tim else None,
                    "kategori_team": Pemain.tim.kategori_team if Pemain.tim else None,
                    "logo_team": (
                        Pemain.tim.logo_team.url
                        if Pemain.tim and Pemain.tim.logo_team
                        else None
                    ),
                },
                "nomor_punggung": Pemain.nomor_punggung,
                "tinggi_badan": Pemain.tinggi_badan,
                "berat_badan": Pemain.berat_badan,
                "tanggal_gabung": Pemain.tanggal_gabung,
                "kelamin": Pemain.kelamin,
                "foto_profil": Pemain.foto_profil.url if Pemain.foto_profil else None,
            },
            "jenis_pemeriksaan": MedicalHistoryData.jenis_pemeriksaan,
            "file_dokumen": (
                MedicalHistoryData.file_dokumen.url
                if MedicalHistoryData.file_dokumen
                else None
            ),
        }

    @staticmethod
    def delete(req):
        MedicalHistoryData = get_object_or_404(
            MedicalHistory, medicalhistory=req["medicalhistory"]
        )
        MedicalHistoryData.delete()
        return {
            "message": f"MedicalHistory with id {req['medicalhistory']} has been deleted."
        }
