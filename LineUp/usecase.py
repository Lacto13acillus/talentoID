from .repo import RepoLineUp
import uuid

class UsecaseLineUp:
    @staticmethod
    def post(request):
        reqs = {
            'id_lineup': str(uuid.uuid4()),
            'match_id': request.data.get('match_id'),
            'player_id': request.data['player_id'],
            'index': request.data['index'],
            'status': request.data['status']
        }
        data_post = RepoLineUp.post(reqs)
        return data_post

    @staticmethod
    def get(lineup_id):
        data = RepoLineUp.get(lineup_id)
        return data

    @staticmethod
    def get_all():
        data = RepoLineUp.get_all()
        return data

    @staticmethod
    def put(request):
        reqs = {
            'id_lineup': request.data['id_lineup'],
            'match_id': request.data.get('match_id'),
            'player_id': request.data['player_id'],
            'index': request.data['index'],
            'status': request.data['status']
        }
        data_put = RepoLineUp.put(reqs)
        return data_put

    @staticmethod
    def delete(request):
        reqs = {
            'id_lineup': request.data['id_lineup']
        }
        data_delete = RepoLineUp.delete(reqs)
        return data_delete