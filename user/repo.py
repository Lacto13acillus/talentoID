# user/repo.py
from django.shortcuts import get_object_or_404
from .models import user
from ProfilCoach.models import ProfilCoach
from player.models import player
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from team.models import team


class RepoUser:
    @staticmethod
    def post(req):
        print("RepoUser Post Request:", req)
        allowed_extensions = ["jpg", "jpeg", "png", "gif"]

        foto_profil = req.get("foto_profil")

        # Jika foto_profil None → skip validation
        if foto_profil:
            file_extension = foto_profil.name.split(".")[-1].lower()
            if file_extension not in allowed_extensions:
                raise ValidationError(
                    "Invalid file format. Only JPEG, PNG, and GIF are allowed."
                )
        else:
            # Jika tidak ada file → set None
            foto_profil = None

        team_obj = None
        if req.get("team_id"):
            team_obj = get_object_or_404(team, team=req["team_id"])

        new_user = user.objects.create(
            id_user=req["id_user"],
            nama=req["nama"],
            email=req["email"],
            nomor_telepon=req["nomor_telepon"],
            team=team_obj,
            password=make_password(req["password"]),
            foto_profil=foto_profil,  # aman jika None
            role=req.get("role", "player"),
        )

        refresh = RefreshToken.for_user(new_user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return {
            "id_user": new_user.id_user,
            "nama": new_user.nama,
            "email": new_user.email,
            "nomor_telepon": new_user.nomor_telepon,
            "foto_profil": new_user.foto_profil.url if new_user.foto_profil else None,
            "role": new_user.role,
            # "team": new_user.team.team,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    @staticmethod
    def get(user_id):
        user_data = get_object_or_404(user, id_user=user_id)
        return {
            "id_user": user_data.id_user,
            "nama": user_data.nama,
            "email": user_data.email,
            "team": user_data.team.team if user_data.team else None,
            "nomor_telepon": user_data.nomor_telepon,
            "foto_profil": user_data.foto_profil.url if user_data.foto_profil else None,
            "role": user_data.role,
        }

    @staticmethod
    def get_all():
        users = user.objects.all().order_by("-created_at")
        return [
            {
                "id_user": user_data.id_user,
                "nama": user_data.nama,
                "email": user_data.email,
                "nomor_telepon": user_data.nomor_telepon,
                "foto_profil": (
                    user_data.foto_profil.url if user_data.foto_profil else None
                ),
                "team_id": user_data.team.team if user_data.team else None,
                "team": (
                    {
                        "team": user_data.team.team,
                        "club": user_data.team.club.club,
                        "coach": user_data.team.coach.coach,
                        "nama_team": user_data.team.nama_team,
                        "kategori_team": user_data.team.kategori_team,
                        "logo_team": (
                            user_data.team.logo_team.url
                            if user_data.team.logo_team
                            else None
                        ),
                    }
                    if user_data.team
                    else None
                ),
                "role": user_data.role,
                "is_active": user_data.is_active,
            }
            for user_data in users
        ]

    @staticmethod
    def put(req):
        User = get_object_or_404(user, id_user=req["id_user"])
        User.nama = req.get("nama", User.nama)
        User.email = req.get("email", User.email)
        User.nomor_telepon = req.get("nomor_telepon", User.nomor_telepon)
        if "password" in req and req["password"]:
            User.password = make_password(req["password"])
        User.foto_profil = req.get("foto_profil", User.foto_profil)
        User.role = req.get("role", User.role)
        User.save()
        return {
            "id_user": User.id_user,
            "nama": User.nama,
            "email": User.email,
            "nomor_telepon": User.nomor_telepon,
            "foto_profil": User.foto_profil.url if User.foto_profil else None,
            "role": User.role,
        }

    @staticmethod
    def delete(req):
        User = get_object_or_404(user, id_user=req["id_user"])
        User.delete()
        return {"message": f"User with id {req['id_user']} has been deleted."}

    @staticmethod
    def login(req):
        email = req["email"]
        password = req["password"]

        try:
            user_data = user.objects.get(email=email)
        except user.DoesNotExist:
            raise ValidationError("User not found.")

        # Bandingkan kata sandi secara langsung (plain text)
        if not check_password(password, user_data.password):
            raise ValueError("Password salah")

        if not user_data.is_active:
            raise ValueError("User not found.")

        if user_data.role == "coach":
            first_coach = ProfilCoach.objects.filter(user=user_data).first()
            id_coach = first_coach.coach if first_coach else None
            userId = id_coach
        elif user_data.role == "player":
            first_player = player.objects.filter(user=user_data).first()
            verification_status = (
                first_player.verification_status if first_player else None
            )
            if verification_status != "Verified":
                raise ValueError("please wait until your account is verified")
            id_player = first_player.player if first_player else None
            userId = id_player
        else:
            userId = user_data.id_user

        refresh = RefreshToken.for_user(user_data)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return {
            "id": userId,
            "user": user_data.id_user,
            "nama": user_data.nama,
            "email": user_data.email,
            "nomor_telepon": user_data.nomor_telepon,
            "foto_profil": user_data.foto_profil.url if user_data.foto_profil else None,
            "role": user_data.role,
            "team_id": user_data.team.team if user_data.team else None,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    @staticmethod
    def delete_account(user_id):
        user_data = get_object_or_404(user, id_user=user_id)
        user_data.is_active = False
        user_data.save()
        return {
            "id_user": user_data.id_user,
            "nama": user_data.nama,
            "email": user_data.email,
            "nomor_telepon": user_data.nomor_telepon,
            "foto_profil": user_data.foto_profil.url if user_data.foto_profil else None,
            "role": user_data.role,
            "message": "Akun berhasil dihapus",
            "is_active": user_data.is_active,
        }
