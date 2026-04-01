# usecases/player_usecase.py
from .repo import RepoPlayer
import uuid
from rest_framework import status as http_status
from rest_framework.response import Response


class UsecasePlayer:
    @staticmethod
    def post(request):
        foto_profil = request.FILES.get("foto_profil")
        if not foto_profil:
            return Response(
                {"code": 400, "message": "File is required."},
                status=http_status.HTTP_400_BAD_REQUEST,
            )

        reqs = {
            "email": request.data["email"],
            "password": request.data["password"],
            "nomor_telepon": request.data["nomor_telepon"],
            "player": uuid.uuid4(),  # Generate UUID untuk player
            "nama": request.data["nama"],
            "posisi": request.data["posisi"],
            "kode_kabupaten": request.data["kode_kabupaten"],
            "team": request.data["team"],
            "nomor_punggung": request.data["nomor_punggung"],
            "tinggi_badan": request.data["tinggi_badan"],
            "berat_badan": request.data["berat_badan"],
            "kelamin": request.data["kelamin"],
            "dob": request.data["dob"],
            "tanggal_gabung": request.data["tanggal_gabung"],
            "payment_channel": request.data["payment_channel"],
            "payment_method": request.data["payment_method"],
            "foto_profil": request.FILES.get("foto_profil"),
        }

        dataPost = RepoPlayer.post(reqs)
        return dataPost

    @staticmethod
    def renew(request):

        reqs = {
            "player": request.data["player"],
            "payment_channel": request.data["payment_channel"],
            "payment_method": request.data["payment_method"],
        }
        dataPost = RepoPlayer.renew(reqs)
        return dataPost

    @staticmethod
    def get(player_id):
        dataPlayer = RepoPlayer.get(player_id)
        return dataPlayer

    @staticmethod
    def get_all():
        return RepoPlayer.get_all()

    @staticmethod
    def get_all_players_by_team_id(team_id):
        return RepoPlayer.get_all_players_by_team_id(team_id)

    @staticmethod
    def put(request):
        reqs = {
            "user": request.data.get("user"),
            "player": request.data["player"],
            "nama": request.data.get("nama"),
            "posisi": request.data.get("posisi"),
            # "kewarganegaraan": request.data.get("kewarganegaraan"),
            "kode_kabupaten": request.data.get("kode_kabupaten"),
            "team": request.data.get("team"),
            "nomor_punggung": request.data.get("nomor_punggung"),
            "tinggi_badan": request.data.get("tinggi_badan"),
            "berat_badan": request.data.get("berat_badan"),
            "tanggal_gabung": request.data.get("tanggal_gabung"),
            "end_date": request.data.get("end_date"),
            "kelamin": request.data.get("kelamin"),
            "dob": request.data["dob"],
            "verification_status": request.data["verification_status"],
            "payment_status": request.data["payment_status"],
        }
        if request.FILES.get("foto_profil") is not None:
            reqs["foto_profil"] = request.FILES.get("foto_profil")

        updated_player = RepoPlayer.put(reqs)
        return updated_player

    @staticmethod
    def delete(request):
        reqs = {"player": request.data["player"]}
        delete_player = RepoPlayer.delete(reqs)
        return delete_player
