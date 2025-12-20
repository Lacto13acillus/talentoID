# ProfilCoach/repo.py
from django.shortcuts import get_object_or_404
from .models import ProfilCoach
from user.models import user
from team.models import team
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.db import transaction


class RepoProfilCoach:
    @staticmethod
    def post(req):
        print(req)
        allowed_extensions = ["jpg", "jpeg", "png", "gif"]

        # Cek apakah file ada dalam request
        # Handle file
        foto_profil = req.get("foto_profil")
        if foto_profil:
            allowed_extensions = ["jpg", "jpeg", "png", "gif"]
            file_extension = foto_profil.name.split(".")[-1].lower()
            if file_extension not in allowed_extensions:
                raise ValidationError(
                    "Invalid file format. Only JPEG, PNG, and GIF are allowed."
                )

        # Gunakan transaction untuk atomic operation
        with transaction.atomic():
            # Buat user
            new_user = user.objects.create_user(
                id_user=req["user_id"],
                nama=req["nama_coach"],
                email=req["email"],
                password=make_password(req["password"]),
                nomor_telepon=req["nomor_telepon"],
                foto_profil=foto_profil,
                role="coach",
            )

            # Buat profil coach
            new_profil_coach = ProfilCoach.objects.create(
                user=new_user,
                coach=req["coach"],
                tanggal_bergabung=req["tanggal_bergabung"],
                tanggal_lahir=req["tanggal_lahir"],
                kewarganegaraan=req["kewarganegaraan"],
                tinggi_badan=req["tinggi_badan"],
                berat_badan=req["berat_badan"],
            )

        teams_dilatih = team.objects.filter(coach=new_profil_coach.coach)

        return {
            "coach": new_profil_coach.coach,
            "user": {
                "user": new_user.id_user,
                "nama": new_user.nama,
                "email": new_user.email,
                "nomor_telepon": new_user.nomor_telepon,
                "foto_profil": (
                    new_user.foto_profil.url if new_user.foto_profil else None
                ),
                "role": new_user.role,
            },
            "profil_coach": {
                "nama_coach": new_user.nama,  # Ambil dari user
                "tanggal_bergabung": new_profil_coach.tanggal_bergabung,
                "tanggal_lahir": new_profil_coach.tanggal_lahir,
                "kewarganegaraan": new_profil_coach.kewarganegaraan,
                "tinggi_badan": new_profil_coach.tinggi_badan,
                "berat_badan": new_profil_coach.berat_badan,
            },
            "teams": [
                {
                    "team": t.team,
                    "nama_team": t.nama_team,
                    "kategori_team": t.kategori_team,
                    "logo_team": t.logo_team.url if t.logo_team else None,
                }
                for t in teams_dilatih
            ],
        }

    @staticmethod
    def get(coach_id):
        profil_coach_data = get_object_or_404(ProfilCoach, coach=coach_id)
        teams_dilatih = team.objects.filter(coach=coach_id)

        return {
            "coach": profil_coach_data.coach,
            "user": {
                "user": profil_coach_data.user.id_user,
                "nama": profil_coach_data.user.nama,
                "email": profil_coach_data.user.email,
                "nomor_telepon": profil_coach_data.user.nomor_telepon,
                "foto_profil": (
                    profil_coach_data.user.foto_profil.url
                    if profil_coach_data.user.foto_profil
                    else None
                ),
                "role": profil_coach_data.user.role,
            },
            "teams": [
                {
                    "team": t.team,
                    "nama_team": t.nama_team,
                    "kategori_team": t.kategori_team,
                    "logo_team": t.logo_team.url if t.logo_team else None,
                }
                for t in teams_dilatih
            ],
            "nama_coach": profil_coach_data.user.nama,
            "tanggal_bergabung": profil_coach_data.tanggal_bergabung,
            "tanggal_lahir": profil_coach_data.tanggal_lahir,
            "kewarganegaraan": profil_coach_data.kewarganegaraan,
            "tinggi_badan": profil_coach_data.tinggi_badan,
            "berat_badan": profil_coach_data.berat_badan,
            "foto_profil": (
                profil_coach_data.user.foto_profil.url
                if profil_coach_data.user.foto_profil
                else None
            ),
        }

    @staticmethod
    def get_all():
        profil_coach_list = ProfilCoach.objects.all().order_by("-created_at")
        result = []

        for profil_coach in profil_coach_list:
            teams_dilatih = team.objects.filter(coach=profil_coach.coach)
            result.append(
                {
                    "coach": profil_coach.coach,
                    "user": {
                        "user": profil_coach.user.id_user,
                        "nama": profil_coach.user.nama,
                        "email": profil_coach.user.email,
                        "nomor_telepon": profil_coach.user.nomor_telepon,
                        "foto_profil": (
                            profil_coach.user.foto_profil.url
                            if profil_coach.user.foto_profil
                            else None
                        ),
                        "role": profil_coach.user.role,
                    },
                    "teams": [
                        {
                            "team": t.team,
                            "nama_team": t.nama_team,
                            "kategori_team": t.kategori_team,
                            "logo_team": t.logo_team.url if t.logo_team else None,
                        }
                        for t in teams_dilatih
                    ],
                    "nama_coach": profil_coach.user.nama,
                    "tanggal_bergabung": profil_coach.tanggal_bergabung,
                    "tanggal_lahir": profil_coach.tanggal_lahir,
                    "kewarganegaraan": profil_coach.kewarganegaraan,
                    "tinggi_badan": profil_coach.tinggi_badan,
                    "berat_badan": profil_coach.berat_badan,
                    "foto_profil": (
                        profil_coach.user.foto_profil.url
                        if profil_coach.user.foto_profil
                        else None
                    ),
                }
            )

        return result

    @staticmethod
    def put(req):
        print(req)
        ProfilCoachData = get_object_or_404(ProfilCoach, coach=req["coach"])
        User = ProfilCoachData.user  # Gunakan user yang sudah terkait

        # Periksa apakah ada field password dalam request
        if "password" in req and req["password"]:
            if len(req["password"]) < 8:
                raise ValidationError(
                    "Kata sandi harus memiliki panjang minimal 8 karakter."
                )
            User.password = req["password"]  # Simpan sebagai plain text
            User.save()

        if "email" in req and req["email"]:
            User.email = req["email"]
        if "nomor_telepon" in req and req["nomor_telepon"]:
            User.nomor_telepon = req["nomor_telepon"]
        if "nomor_telepon" in req and req["nomor_telepon"]:
            pass  # This line does nothing, consider removing or updating as needed

        User.nama = req["nama_coach"]

        # Periksa apakah ada file foto_profil dalam request
        if "foto_profil" in req and req["foto_profil"]:

            # Validasi ekstensi file
            allowed_extensions = ["jpg", "jpeg", "png", "gif"]
            file_extension = req["foto_profil"].name.split(".")[-1].lower()
            if file_extension not in allowed_extensions:
                raise ValidationError(
                    "Format file tidak valid. Hanya JPG, JPEG, PNG, dan GIF yang diizinkan."
                )

            # Hapus foto profil lama jika ada
            if ProfilCoachData.foto_profil:
                ProfilCoachData.foto_profil.delete(save=False)

            # Hapus foto profil lama jika ada
            if User.foto_profil:
                User.foto_profil.delete(save=False)

            # Simpan foto profil baru
            ProfilCoachData.foto_profil = req["foto_profil"]
            User.foto_profil = req["foto_profil"]
        User.save()

        # Update data ProfilCoach
        ProfilCoachData.user.nama = req.get("nama_coach", ProfilCoachData.user.nama)
        ProfilCoachData.tanggal_bergabung = req.get(
            "tanggal_bergabung", ProfilCoachData.tanggal_bergabung
        )
        ProfilCoachData.tanggal_lahir = req.get(
            "tanggal_lahir", ProfilCoachData.tanggal_lahir
        )
        ProfilCoachData.kewarganegaraan = req.get(
            "kewarganegaraan", ProfilCoachData.kewarganegaraan
        )
        ProfilCoachData.tinggi_badan = req.get(
            "tinggi_badan", ProfilCoachData.tinggi_badan
        )
        ProfilCoachData.berat_badan = req.get(
            "berat_badan", ProfilCoachData.berat_badan
        )
        ProfilCoachData.save()

        teams_dilatih = team.objects.filter(coach=ProfilCoachData.coach)

        return {
            "coach": ProfilCoachData.coach,
            "user": {
                "user": User.id_user,
                "nama": User.nama,
                "email": User.email,
                "nomor_telepon": User.nomor_telepon,
                "foto_profil": User.foto_profil.url if User.foto_profil else None,
                "role": User.role,
            },
            "teams": [
                {
                    "team": t.team,
                    "nama_team": t.nama_team,
                    "kategori_team": t.kategori_team,
                    "logo_team": t.logo_team.url if t.logo_team else None,
                }
                for t in teams_dilatih
            ],
            "nama_coach": ProfilCoachData.nama_coach,
            "tanggal_bergabung": ProfilCoachData.tanggal_bergabung,
            "tanggal_lahir": ProfilCoachData.tanggal_lahir,
            "kewarganegaraan": ProfilCoachData.kewarganegaraan,
            "tinggi_badan": ProfilCoachData.tinggi_badan,
            "berat_badan": ProfilCoachData.berat_badan,
            "foto_profil": (
                ProfilCoachData.foto_profil.url if ProfilCoachData.foto_profil else None
            ),
        }

    @staticmethod
    def delete(req):
        ProfilCoachData = get_object_or_404(ProfilCoach, coach=req["coach"])
        if ProfilCoachData.foto_profil:
            ProfilCoachData.foto_profil.delete(save=False)
        ProfilCoachData.delete()
        return {"message": f"ProfilCoach with id {req['coach']} has been deleted."}
