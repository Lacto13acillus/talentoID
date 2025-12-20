from .repo import RepoStats
import uuid

class UsecaseStats:
    @staticmethod
    def post(request):
        reqs = {
            'match': request.data['match'],
            'stats_list': request.data['stats_list']
        }
        return RepoStats.post(reqs)

    @staticmethod
    def get(stats_id):
        return RepoStats.get(stats_id)

    @staticmethod
    def get_all():
        return RepoStats.get_all()

    @staticmethod
    def get_by_player(player_id):
        return RepoStats.get_by_player(player_id)

    @staticmethod
    def put(request):
        reqs = {
            'stats': request.data['stats'],
            'match': request.data['match'],
            'player': request.data['player'],
            'position_played': request.data.get('position_played'),
            'minutes_played': request.data.get('minutes_played'),
            'overall_rating': request.data.get('overall_rating')
        }
        return RepoStats.put(reqs)

    @staticmethod
    def delete(request):
        reqs = {
            'stats': request.data['stats']
        }
        return RepoStats.delete(reqs)