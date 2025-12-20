from .repo import RepoFormation
import uuid

class UsecaseFormation:
    @staticmethod
    def post(request):
        reqs = {
            'id_formasi': uuid.uuid4(),
            'formasi': request.data['formasi']
        }
        data_post = RepoFormation.post(reqs)
        return data_post
    
    @staticmethod
    def get_by_id(id_formasi):
        data = RepoFormation.get_by_id(id_formasi)
        return data

    @staticmethod
    def get_all():
        data = RepoFormation.get_all()
        return data

    @staticmethod
    def put(request):
        reqs = {
            'id_formasi': request.data['id_formasi'],
            'formasi': request.data['formasi']
        }
        data_put = RepoFormation.put(reqs)
        return data_put

    @staticmethod
    def delete(request):
        reqs = {
            'id_formasi': request.data['id_formasi']
        }
        data_delete = RepoFormation.delete(reqs)
        return data_delete