from .repo import RepoUser
import uuid


class UsecaseUser:
    @staticmethod
    def post(request):
        # if "foto_profil" not in request.FILES:
        #     raise ValueError("foto_profil is required")

        reqs = {
            "id_user": uuid.uuid4(),  # Konversi UUID ke string
            "nama": request.data["nama"],
            "email": request.data["email"],
            "nomor_telepon": request.data.get("nomor_telepon"),
            "team_id": request.data.get("team_id"),
            "password": request.data["password"],
            "foto_profil": request.FILES.get("foto_profil"),
            "role": request.data.get("role", "player"),
        }
        dataPost = RepoUser.post(reqs)
        return dataPost

    @staticmethod
    def get(user_id):
        dataUser = RepoUser.get(user_id)
        return dataUser

    @staticmethod
    def get_all():
        return RepoUser.get_all()

    @staticmethod
    def put(request):
        reqs = {
            "id_user": request.data["id_user"],
            "nama": request.data.get("nama"),
            "email": request.data.get("email"),
            "nomor_telepon": request.data.get("nomor_telepon"),
            "password": request.data.get("password"),
            "foto_profil": request.FILES.get("foto_profil"),
            "role": request.data.get("role"),
        }
        updated_user = RepoUser.put(reqs)
        return updated_user

    @staticmethod
    def delete(request):
        reqs = {"id_user": request.data["id_user"]}
        delete_message = RepoUser.delete(reqs)
        return delete_message

    @staticmethod
    def login(request):
        reqs = {"email": request.data["email"], "password": request.data["password"]}
        dataLogin = RepoUser.login(reqs)
        return dataLogin

    @staticmethod
    def delete_account(user_id):
        deleteUser = RepoUser.delete_account(user_id)
        return deleteUser
