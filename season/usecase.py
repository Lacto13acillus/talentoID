from .repo import RepoSeason
import uuid

class UsecaseSeason:
    @staticmethod
    def post(request):
        reqs = {
            'season': uuid.uuid4(),
            'nama_season': request.data['nama_season']
        }
        return RepoSeason.post(reqs)
    
    @staticmethod
    def get(season_id):
        return RepoSeason.get(season_id)
    
    @staticmethod
    def get_all():
        return RepoSeason.get_all()
    
    @staticmethod
    def put(request):
        reqs = {
            'season': request.data['season'],
            'nama_season': request.data.get('nama_season')
        }
        return RepoSeason.put(reqs)
    
    @staticmethod
    def delete(request):
        reqs = {
            'season': request.data['season']
        }
        return RepoSeason.delete(reqs)