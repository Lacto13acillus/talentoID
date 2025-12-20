from .repo import RepoGroup
import uuid

class UsecaseGroup:
    @staticmethod
    def post(request):
        reqs = {
            'id': uuid.uuid4(),  # Generate UUID untuk id
            'nama_group': request.data['nama_group'],
            'team': request.data['team'],  # Sesuai dengan struktur request
            'anggota': request.data['anggota']  # Sesuai dengan struktur request
        }
        dataPost = RepoGroup.post(reqs)
        return dataPost
    
    @staticmethod
    def get(group_id):
        dataGroup = RepoGroup.get(group_id)
        return dataGroup
    
    @staticmethod
    def get_all():
        return RepoGroup.get_all()
    
    @staticmethod
    def put(request):
        reqs = {
            'id': request.data['id'],
            'nama_group': request.data.get('nama_group'),
            'team': request.data.get('team'),  # Sesuai dengan struktur request
            'anggota': request.data.get('anggota')  # Sesuai dengan struktur request
        }
        updated_group = RepoGroup.put(reqs)
        return updated_group
    
    @staticmethod
    def delete(request):
        reqs = {
            'id': request.data['id']
        }
        delete_message = RepoGroup.delete(reqs)
        return delete_message