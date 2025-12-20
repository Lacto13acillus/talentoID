from .repo import RepoPertandingan
import uuid


class UsecasePertandingan:
    @staticmethod
    def post(request):
        reqs = {
            "match": str(uuid.uuid4()),
            "nama_pertandingan": request.data["nama_pertandingan"],
            "team_home": request.data["team_home"],
            "team_away": request.data["team_away"],
            "formasi": request.data.get("formasi"),
            "schedule": request.data.get("schedule"),
            "stadion": request.data["stadion"],
            "season": request.data["season"],
            "date": request.data["date"],
            "start_time": request.data["start_time"],
            "end_time": request.data["end_time"],
            "starting_players": request.data.get("starting_players", []),
            "reserve_players": request.data.get("reserve_players", []),
        }
        dataPost = RepoPertandingan.post(reqs)
        return dataPost

    @staticmethod
    def get(pertandingan_id):
        dataPertandingan = RepoPertandingan.get(pertandingan_id)
        return dataPertandingan

    @staticmethod
    def get_all():
        dataPertandingan = RepoPertandingan.get_all()
        return dataPertandingan

    @staticmethod
    def get_pertandingan_by_coach(coach_id):
        dataPertandingan = RepoPertandingan.get_pertandingan_by_coach(coach_id)
        return dataPertandingan

    @staticmethod
    def get_pertandingan_by_player(player_id):
        dataPertandingan = RepoPertandingan.get_pertandingan_by_player(player_id)
        return dataPertandingan

    @staticmethod
    def get_pertandingan_by_team(team_id):
        dataPertandingan = RepoPertandingan.get_pertandingan_by_team(team_id)
        return dataPertandingan

    @staticmethod
    def get_stats_by_coach(coach_id):
        data_stats = RepoPertandingan.get_stats_by_coach(coach_id)
        return data_stats

    @staticmethod
    def put(request):
        reqs = {
            "match": request.data["match"],
            "nama_pertandingan": request.data.get("nama_pertandingan"),
            "team_home": request.data.get("team_home"),
            "team_away": request.data.get("team_away"),
            "formasi": request.data.get("formasi"),
            "schedule": request.data.get("schedule"),
            "stadion": request.data.get("stadion"),
            "status": request.data.get("status"),
            "season": request.data.get("season"),
            "date": request.data.get("date"),
            "start_time": request.data.get("start_time"),
            "end_time": request.data.get("end_time"),
        }
        updated_pertandingan = RepoPertandingan.put(reqs)
        return updated_pertandingan

    @staticmethod
    def delete(request):
        reqs = {"match": request.data["match"]}
        delete_message = RepoPertandingan.delete(reqs)
        return delete_message

    @staticmethod
    def set_ready_if_preparing(match_id):
        match = RepoPertandingan.update_status_to_ready(match_id)

        return {
            "message": "Status match berhasil diubah menjadi READY",
            "match_id": str(match.match),
            "new_status": match.status.match_status,
        }
