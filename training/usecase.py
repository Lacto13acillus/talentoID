from .repo import RepoTraining
import uuid


class UsecaseTraining:
    @staticmethod
    def post(request):
        reqs = {
            "training": uuid.uuid4(),
            "nama_latihan": request.data["nama_latihan"],
            "team": request.data["team"],
            "schedule": request.data.get("schedule"),  # Optional
            "stadion": request.data["stadion"],
            "trainingcategory": request.data["trainingcategory"],  # Single or list
            "frequency": request.data.get("frequency"),  # Optional
            "date": request.data["date"],
            "start_time": request.data["start_time"],
            "end_time": request.data["end_time"],
            "deskripsi": request.data["deskripsi"],
        }
        dataPost = RepoTraining.post(reqs)
        return dataPost

    @staticmethod
    def get(training_id):
        dataTraining = RepoTraining.get(training_id)
        return dataTraining

    @staticmethod
    def get_by_coach(coach_id):
        data = RepoTraining.get_by_coach(coach_id)
        return data

    @staticmethod
    def get_by_player(player_id):
        data = RepoTraining.get_by_player(player_id)
        return data

    @staticmethod
    def get_by_team(team_id):
        data = RepoTraining.get_by_team(team_id)
        return data

    @staticmethod
    def get_all():
        return RepoTraining.get_all()

    @staticmethod
    def put(request):
        reqs = {
            "training": request.data["training"],
            "nama_latihan": request.data.get("nama_latihan"),
            "team": request.data.get("team"),
            "schedule": request.data.get("schedule"),  # Optional
            "stadion": request.data.get("stadion"),
            "trainingcategory": request.data.get("trainingcategory"),  # Single or list
            "frequency": request.data.get("frequency"),  # Optional
            "date": request.data.get("date"),
            "start_time": request.data.get("start_time"),
            "end_time": request.data.get("end_time"),
            "deskripsi": request.data.get("deskripsi"),
        }
        updated_training = RepoTraining.put(reqs)
        return updated_training

    @staticmethod
    def delete(request):
        reqs = {"training": request.data["training"]}
        delete_message = RepoTraining.delete(reqs)
        return delete_message
