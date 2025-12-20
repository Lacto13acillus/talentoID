# usecases/player_search_usecase.py
from .repo import RepoPlayerSearch
import uuid

class UsecasePlayerSearch:
    @staticmethod
    def post(request):
        reqs = {
            'id': uuid.uuid4(),  # Generate UUID untuk id
            'nama_player': request.data['nama_player'],
            'kata_kunci': request.data['kata_kunci']
        }
        dataPost = RepoPlayerSearch.post(reqs)
        return dataPost
    
    @staticmethod
    def get(player_search_id):
        dataPlayerSearch = RepoPlayerSearch.get(player_search_id)
        return dataPlayerSearch
    
    @staticmethod
    def get_all():
        return RepoPlayerSearch.get_all()


    
    @staticmethod
    def put(request):
        reqs = {
            'id': request.data['id'],
            'nama_player': request.data['nama_player'],
            'kata_kunci': request.data.get('kata_kunci')
        }
        updated_player_search = RepoPlayerSearch.put(reqs)
        return updated_player_search
    
    @staticmethod
    def delete(request):
        reqs = {
            'id': request.data['id']
        }
        delete_player_search = RepoPlayerSearch.delete(reqs)
        return delete_player_search