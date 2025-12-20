from .repo import RepoStadion
import uuid

class UsecaseStadion:
    @staticmethod
    def post(request):
        reqs = {
            'stadion': uuid.uuid4(),
            'nama_stadion': request.data['nama_stadion'],
            'lokasi': request.data['lokasi']
        }
        dataPost = RepoStadion.post(reqs)
        return dataPost
    
    @staticmethod
    def get(stadion_id):
        dataStadion = RepoStadion.get(stadion_id)
        return dataStadion
    
    @staticmethod
    def get_all():
        return RepoStadion.get_all()
    
    def put(request):
        reqs = {
            'stadion': request.data['stadion'],
            'nama_stadion': request.data.get('nama_stadion'),
            'lokasi' : request.data.get('lokasi'),
        }
        updated_stadion = RepoStadion.put(reqs)
        return updated_stadion
    
    def delete(request):
        reqs = {
            'stadion': request.data['stadion']
        }
        delete_message = RepoStadion.delete(reqs)
        return delete_message