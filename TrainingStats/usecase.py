from .repo import RepoTrainingStats
import uuid

class UsecaseTrainingStats:
    @staticmethod
    def post(request):
        reqs = {
            'stats': uuid.uuid4(),
            'training': request.data['training'],
            'player': request.data['player'],
            'position_played': request.data['position_played'],
            'minutes_played': request.data['minutes_played'],
            'overall_rating': request.data['overall_rating']
        }
        return RepoTrainingStats.post(reqs)
    
    @staticmethod
    def get(stats_id):
        return RepoTrainingStats.get(stats_id)
    
    @staticmethod
    def get_all():
        return RepoTrainingStats.get_all()
    
    @staticmethod
    def get_by_player(player_id):
        return RepoTrainingStats.get_by_player(player_id)
    
    @staticmethod
    def put(request):
        reqs = {
            'stats': request.data['stats'],
            'training': request.data['training'],
            'player': request.data['player'],
            'position_played': request.data.get('position_played'),
            'minutes_played': request.data.get('minutes_played'),
            'overall_rating': request.data.get('overall_rating')
        }
        return RepoTrainingStats.put(reqs)
    
    @staticmethod
    def delete(request):
        reqs = {
            'stats': request.data['stats']
        }
        return RepoTrainingStats.delete(reqs)