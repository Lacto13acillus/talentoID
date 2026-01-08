# repository/player_repository.py
from django.shortcuts import get_object_or_404
from .models import player
from team.models import team
from user.models import user
from django.core.exceptions import ValidationError
import uuid
from rest_framework import status as http_status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
import xendit
from xendit.apis import InvoiceApi
from xendit.invoice.model.create_invoice_request import CreateInvoiceRequest

# See configuration.py for a list of all supported configuration parameters.
xendit.set_api_key(
    "xnd_development_aj3dzlFih33YWSC24U6eLukOxX8uXU5tecRqd0IXtjmsbBTrs2HjxcvVWLoBZ5"
)


class RepoPlayer:
    @staticmethod
    def post(req):

        # generate unique external_id
        email = req["email"]
        external_id = f"register_{uuid.uuid4().hex[:6]}_{email}"

        # Enter a context with an instance of the API client
        api_client = xendit.ApiClient()

        # Create an instance of the API class
        api_instance = InvoiceApi(api_client)

        amount = float(100000)
        create_invoice_request = CreateInvoiceRequest(
            external_id=external_id,
            payer_email=email,
            description="Pendaftaran Pemain",
            amount=amount,
        )

        try:
            # Panggil API Xendit untuk membuat invoice
            api_response = api_instance.create_invoice(create_invoice_request)
            print("api_response", api_response)

            allowed_extensions = ["jpg", "jpeg", "png", "gif"]

            # Cek apakah file ada dalam request
            if "foto_profil" not in req:
                return Response(
                    {"code": 400, "message": "RepoPlayer File is required."},
                    status=http_status.HTTP_400_BAD_REQUEST,
                )

            foto_profil = req["foto_profil"]
            file_extension = foto_profil.name.split(".")[
                -1
            ].lower()  # Ambil ekstensi file

            # Validasi ekstensi file
            if file_extension not in allowed_extensions:
                return Response(
                    {
                        "code": 400,
                        "message": "Invalid file format. Only JPEG, PNG, and GIF are allowed.",
                    },
                    status=http_status.HTTP_400_BAD_REQUEST,
                )
                # raise ValidationError("Invalid file format. Only JPEG, PNG, and GIF are allowed.")

            Tim = get_object_or_404(team, team=req["team"])

            new_user = user.objects.create(
                id_user=uuid.uuid4(),
                nama=req["nama"],
                email=req["email"],
                nomor_telepon=req["nomor_telepon"],
                password=make_password(req["password"]),
                foto_profil=req.get("foto_profil", None),
                role=req.get("role", "player"),
            )

            new_player = player.objects.create(
                user=new_user,
                player=req["player"],
                nama=req["nama"],
                posisi=req["posisi"],
                kewarganegaraan=req["kewarganegaraan"],
                tim=Tim,
                nomor_punggung=req["nomor_punggung"],
                tinggi_badan=req["tinggi_badan"],
                berat_badan=req["berat_badan"],
                tanggal_gabung=req["tanggal_gabung"],
                dob=req["dob"],
                kelamin=req["kelamin"],
                foto_profil=req.get("foto_profil", None),
                external_id=external_id,
                amount=amount,
                expiry_date=api_response.expiry_date,
                invoice_url=api_response.invoice_url,
            )
            return {
                "user": {
                    "user": new_user.id_user,
                    "nama": new_user.nama,
                    "email": new_user.email,
                    "nomor_telepon": new_user.nomor_telepon,
                    "foto_profil": (
                        new_user.foto_profil.url if user.foto_profil else None
                    ),
                    "role": new_user.role,
                },
                "player": new_player.player,
                "nama": new_player.nama,
                "posisi": new_player.posisi,
                "kewarganegaraan": new_player.kewarganegaraan,
                "team_id": Tim.team,
                "team": {
                    "team": Tim.team,
                    # "club": Tim.club.club,
                    "coach": Tim.coach.coach,
                    "nama_team": Tim.nama_team,
                    "kategori_team": Tim.kategori_team,
                    "logo_team": Tim.logo_team.url if Tim.logo_team else None,
                },
                "nomor_punggung": new_player.nomor_punggung,
                "tinggi_badan": new_player.tinggi_badan,
                "berat_badan": new_player.berat_badan,
                "tanggal_gabung": new_player.tanggal_gabung,
                "dob": new_player.dob,
                "kelamin": new_player.kelamin,
                "verification_status": new_player.verification_status,
                "payment_status": new_player.payment_status,
                "foto_profil": (
                    new_user.foto_profil.url if new_user.foto_profil else None
                ),
                "external_id": new_player.external_id,
                "amount": new_player.amount,
                "expiry_date": new_player.expiry_date,
                "invoice_url": new_player.invoice_url,
            }

        except xendit.XenditSdkException as e:
            print("Exception when calling InvoiceApi->create_invoice:", e)

            return {"code": 500, "message": "Failed to create invoice", "error": str(e)}

    @staticmethod
    def get(player_id):
        player_data = get_object_or_404(player, player=player_id)
        return {
            "user": {
                "user": player_data.user.id_user,
                "nama": player_data.user.nama,
                "email": player_data.user.email,
                "nomor_telepon": player_data.user.nomor_telepon,
                "foto_profil": (
                    player_data.user.foto_profil.url if user.foto_profil else None
                ),
                "role": player_data.user.role,
            },
            "player": player_data.player,
            "nama": player_data.nama,
            "posisi": player_data.posisi,
            "kewarganegaraan": player_data.kewarganegaraan,
            "team_id": player_data.tim.team,
            "team": {
                "team": player_data.tim.team,
                # "club": player_data.tim.club.club,
                "coach": player_data.tim.coach.coach,
                "nama_team": player_data.tim.nama_team,
                "kategori_team": player_data.tim.kategori_team,
                "logo_team": (
                    player_data.tim.logo_team.url if player_data.tim.logo_team else None
                ),
            },
            "nomor_punggung": player_data.nomor_punggung,
            "tinggi_badan": player_data.tinggi_badan,
            "berat_badan": player_data.berat_badan,
            "tanggal_gabung": player_data.tanggal_gabung,
            "kelamin": player_data.kelamin,
            "dob": player_data.dob,
            "verification_status": player_data.verification_status,
            "payment_status": player_data.payment_status,
            "foto_profil": (
                player_data.foto_profil.url if player_data.foto_profil else None
            ),
        }

    @staticmethod
    def get_all():
        players = player.objects.all().order_by("-created_at")
        return [
            {
                "user": {
                    "user": p.user.id_user,
                    "nama": p.user.nama,
                    "email": p.user.email,
                    "nomor_telepon": p.user.nomor_telepon,
                    "foto_profil": (
                        p.user.foto_profil.url if p.user.foto_profil else None
                    ),
                    "role": p.user.role,
                },
                "player": p.player,
                "nama": p.nama,
                "posisi": p.posisi,
                "kewarganegaraan": p.kewarganegaraan,
                "team_id": p.tim.team,
                "team": {
                    "team": p.tim.team,
                    # "club": p.tim.club.club,
                    "coach": p.tim.coach.coach,
                    "nama_team": p.tim.nama_team,
                    "kategori_team": p.tim.kategori_team,
                    "logo_team": p.tim.logo_team.url if p.tim.logo_team else None,
                },
                "nomor_punggung": p.nomor_punggung,
                "tinggi_badan": p.tinggi_badan,
                "berat_badan": p.berat_badan,
                "tanggal_gabung": p.tanggal_gabung,
                "kelamin": p.kelamin,
                "dob": p.dob,
                "verification_status": p.verification_status,
                "payment_status": p.payment_status,
                "foto_profil": p.foto_profil.url if p.foto_profil else None,
            }
            for p in players
        ]

    @staticmethod
    def get_all_players_by_team_id(team_id):
        players = player.objects.filter(tim=team_id)
        return [
            {
                "user": {
                    "user": p.user.id_user,
                    "nama": p.user.nama,
                    "email": p.user.email,
                    "nomor_telepon": p.user.nomor_telepon,
                    "foto_profil": (
                        p.user.foto_profil.url if p.user.foto_profil else None
                    ),
                    "role": p.user.role,
                },
                "player": p.player,
                "nama": p.nama,
                "posisi": p.posisi,
                "kewarganegaraan": p.kewarganegaraan,
                "team_id": p.tim.team,
                "team": {
                    "team": p.tim.team,
                    # "club": p.tim.club.club,
                    "coach": p.tim.coach.coach,
                    "nama_team": p.tim.nama_team,
                    "kategori_team": p.tim.kategori_team,
                    "logo_team": p.tim.logo_team.url if p.tim.logo_team else None,
                },
                "nomor_punggung": p.nomor_punggung,
                "tinggi_badan": p.tinggi_badan,
                "berat_badan": p.berat_badan,
                "tanggal_gabung": p.tanggal_gabung,
                "kelamin": p.kelamin,
                "dob": p.dob,
                "verification_status": p.verification_status,
                "payment_status": p.payment_status,
                "foto_profil": p.foto_profil.url if p.foto_profil else None,
            }
            for p in players
        ]

    @staticmethod
    def put(req):
        allowed_extensions = ["jpg", "jpeg", "png", "gif"]

        PlayerData = get_object_or_404(player, player=req["player"])
        Tim = get_object_or_404(team, team=req["team"])
        # User = get_object_or_404(user, id=req['user'])

        # PlayerData.user = User
        PlayerData.nama = req.get("nama", PlayerData.nama)
        PlayerData.posisi = req.get("posisi", PlayerData.posisi)
        PlayerData.kewarganegaraan = req.get(
            "kewarganegaraan", PlayerData.kewarganegaraan
        )
        PlayerData.tim = Tim
        PlayerData.nomor_punggung = req.get("nomor_punggung", PlayerData.nomor_punggung)
        PlayerData.tinggi_badan = req.get("tinggi_badan", PlayerData.tinggi_badan)
        PlayerData.berat_badan = req.get("berat_badan", PlayerData.berat_badan)
        PlayerData.tanggal_gabung = req.get("tanggal_gabung", PlayerData.tanggal_gabung)
        PlayerData.kelamin = req.get("kelamin", PlayerData.kelamin)
        PlayerData.dob = req.get("dob", PlayerData.dob)
        PlayerData.verification_status = req.get(
            "verification_status", PlayerData.verification_status
        )
        PlayerData.payment_status = req.get("payment_status", PlayerData.payment_status)
        PlayerData.foto_profil = req.get("foto_profil", PlayerData.foto_profil)

        if "foto_profil" in req and req["foto_profil"] is not None:
            foto_profil = req["foto_profil"]
            file_extension = foto_profil.name.split(".")[
                -1
            ].lower()  # Ambil ekstensi file

            # Validasi ekstensi file
            if file_extension not in allowed_extensions:
                raise ValidationError(
                    "Invalid file format. Only JPEG, PNG, and GIF are allowed."
                )

            # Update logo_team
            PlayerData.foto_profil = foto_profil

        PlayerData.save()

        return {
            "user": {
                "user": PlayerData.user.id_user,
                "nama": PlayerData.user.nama,
                "email": PlayerData.user.email,
                "nomor_telepon": PlayerData.user.nomor_telepon,
                "foto_profil": (
                    PlayerData.user.foto_profil.url if user.foto_profil else None
                ),
                "role": PlayerData.user.role,
            },
            "player": PlayerData.player,
            "nama": PlayerData.nama,
            "posisi": PlayerData.posisi,
            "kewarganegaraan": PlayerData.kewarganegaraan,
            "team_id": PlayerData.tim.team,
            "team": {
                "team": Tim.team,
                # "club": Tim.club.club,
                "coach": Tim.coach.coach,
                "nama_team": Tim.nama_team,
                "kategori_team": Tim.kategori_team,
                "logo_team": Tim.logo_team.url if Tim.logo_team else None,
            },
            "nomor_punggung": PlayerData.nomor_punggung,
            "tinggi_badan": PlayerData.tinggi_badan,
            "berat_badan": PlayerData.berat_badan,
            "tanggal_gabung": PlayerData.tanggal_gabung,
            "kelamin": PlayerData.kelamin,
            "dob": PlayerData.dob,
            "verification_status": PlayerData.verification_status,
            "payment_status": PlayerData.payment_status,
            "foto_profil": (
                PlayerData.foto_profil.url if PlayerData.foto_profil else None
            ),
        }

    @staticmethod
    def delete(req):
        PlayerData = get_object_or_404(player, player=req["player"])
        PlayerData.delete()
        return {"message": f"Player with id {req['player']} has been deleted."}
