import uuid
from .repo import RepoPlayerPerformance

class UsecasePlayerPerformance:
    @staticmethod
    def get_all():
        return RepoPlayerPerformance.get_all()

    @staticmethod
    def get_by_id(performance_id):
        return RepoPlayerPerformance.get_by_id(performance_id)

    @staticmethod
    def get_by_match_id(match_id):
        return RepoPlayerPerformance.get_by_match_id(match_id)
    @staticmethod
    def get_by_player_id(player_id):
        return RepoPlayerPerformance.get_by_player_id(player_id_target=player_id)

    @staticmethod
    def get_by_player_id_and_match_id(player_id, match_id):
        return RepoPlayerPerformance.get_by_player_id(player_id_target=player_id, match_id_target=match_id)

    @staticmethod
    def get_by_team_id(team_id):
        return RepoPlayerPerformance.get_by_team_id(team_id)
    @staticmethod
    def get_by_match_id_summary(match_id):
        return RepoPlayerPerformance.get_by_match_id_summary(match_id)

    @staticmethod
    def post(player_id, training_id, match_id, metric_id, value):

        return RepoPlayerPerformance.post(
            player_id=player_id,
            training_id=training_id,
            match_id=match_id,
            metric_id=metric_id,
            value=value,
        )

    @staticmethod
    def put(request):
        reqs = {
            "player_performance": request.data["player_performance"],
            "player": request.data["player"],
            "metric": request.data["metric"],
            "value": request.data["value"],
        }

        if request.data.get("match"):
            reqs["match"] = request.data["match"]
            reqs["training"] = None
        elif request.data.get("training"):
            reqs["training"] = request.data["training"]
            reqs["match"] = None

        return RepoPlayerPerformance.put(reqs)

    @staticmethod
    def delete(request):
        return RepoPlayerPerformance.delete(request.data["player_performance"])
