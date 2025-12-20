# ProfilCoach/usecase.py
from .repo import RepoProfilCoach
import uuid


class UsecaseProfilCoach:
    @staticmethod
    def post(request):
        if "foto_profil" not in request.FILES:
            raise ValueError("File is required.")

        reqs = {
            "email": request.data["email"],
            "password": request.data["password"],
            "nomor_telepon": request.data["nomor_telepon"],
            "coach": uuid.uuid4(),
            "user_id": uuid.uuid4(),
            "nama_coach": request.data["nama_coach"],
            "tanggal_bergabung": request.data["tanggal_bergabung"],
            "tanggal_lahir": request.data["tanggal_lahir"],
            "kewarganegaraan": request.data["kewarganegaraan"],
            "tinggi_badan": request.data["tinggi_badan"],
            "berat_badan": request.data["berat_badan"],
            "foto_profil": request.FILES.get(
                "foto_profil"
            ),  # Ambil foto_profil dari request.FILES
        }
        dataPost = RepoProfilCoach.post(reqs)
        return dataPost

    @staticmethod
    def get(coach_id):
        dataProfilCoach = RepoProfilCoach.get(coach_id)
        return dataProfilCoach

    @staticmethod
    def get_all():
        dataProfilCoach = RepoProfilCoach.get_all()
        return dataProfilCoach

    @staticmethod
    def put(request):
        reqs = {
            "coach": request.data["coach"],
            # 'user': request.data['user'],
            "nama_coach": request.data.get("nama_coach"),
            "tanggal_lahir": request.data.get("tanggal_lahir"),
            "kewarganegaraan": request.data.get("kewarganegaraan"),
            "tinggi_badan": request.data.get("tinggi_badan"),
            "berat_badan": request.data.get("berat_badan"),
            "tanggal_bergabung": request.data.get("tanggal_bergabung"),
        }
        if request.data.get("email") is not None:
            reqs["email"] = request.data.get("email")
        if request.data.get("nomor_telepon") is not None:
            reqs["nomor_telepon"] = request.data.get("nomor_telepon")
        if request.data.get("password") is not None:
            reqs["password"] = request.data.get("password")
        if request.FILES.get("foto_profil") is not None:
            reqs["foto_profil"] = request.FILES.get("foto_profil")

        updated_profil_coach = RepoProfilCoach.put(reqs)
        return updated_profil_coach

    @staticmethod
    def delete(request):
        reqs = {"coach": request.data["coach"]}
        delete_profil_coach = RepoProfilCoach.delete(reqs)
        return delete_profil_coach
