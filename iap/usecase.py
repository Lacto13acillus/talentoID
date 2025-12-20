from .repo import RepoIAP
import uuid

class UsecaseIAP:
    @staticmethod
    def post(request):
        reqs = {
            'player': request.data['player'],
            'match': request.data['match'],
            'iaps': request.data['iaps']
        }
        return RepoIAP.post(reqs)

    @staticmethod
    def get(iap_id):
        return RepoIAP.get(iap_id)

    @staticmethod
    def get_all():
        return RepoIAP.get_all()

    @staticmethod
    def get_by_player_and_match(player_id, match_id):
        return RepoIAP.get_by_player_and_match(player_id, match_id)

    @staticmethod
    def put(request):
        reqs = {
            'iap': request.data['iap'],
            'player': request.data['player'],
            'match': request.data.get('match'),
            'category': request.data.get('category'),
            'type': request.data.get('type'),
            'current_achieve': request.data.get('current_achieve'),
            'target': request.data.get('target')
        }
        return RepoIAP.put(reqs)

    @staticmethod
    def delete(request):
        reqs = {
            'iap': request.data['iap']
        }
        return RepoIAP.delete(reqs)
