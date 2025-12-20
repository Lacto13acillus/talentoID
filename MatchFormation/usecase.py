from .repo import RepoMatchFormations
import uuid

class UsecaseMatchFormations:
    @staticmethod
    def post(request):
        reqs = {
            'id_matchformations': str(uuid.uuid4()),
            'id_formations': request.data['id_formations'],
        }
        data_post = RepoMatchFormations.post(reqs)
        return data_post

    @staticmethod
    def get(matchformation_id):
        data = RepoMatchFormations.get(matchformation_id)
        return data

    @staticmethod
    def get_all():
        data = RepoMatchFormations.get_all()
        return data

    @staticmethod
    def put(request):
        reqs = {
            'id_matchformations': request.data['id_matchformations'],
            'id_formations': request.data['id_formations'],
        }
        data_put = RepoMatchFormations.put(reqs)
        return data_put

    @staticmethod
    def delete(request):
        reqs = {
            'id_matchformations': request.data['id_matchformations']
        }
        data_delete = RepoMatchFormations.delete(reqs)
        return data_delete