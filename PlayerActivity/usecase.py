# PlayerActivity/usecase.py
from .repo import RepoPlayerActivity

class UsecasePlayerActivity:
    @staticmethod
    def calculate_activity(player_id):
        return RepoPlayerActivity.calculate_activity(player_id)