from .repo import RepoPlayerUpdate
import uuid

class UsecasePlayerUpdate:
    @staticmethod
    def post(request):
        reqs = {
            'playerupdate': uuid.uuid4(),  # Generate UUID untuk playerupdate
            'player': request.data['player'],
            'judul_update': request.data['judul_update'],
            'deskripsi': request.data['deskripsi']
        }
        dataPost = RepoPlayerUpdate.post(reqs)
        return dataPost
    
    @staticmethod
    def get(playerupdate_id):
        dataUpdate = RepoPlayerUpdate.get(playerupdate_id)
        return dataUpdate
    
    @staticmethod
    def get_all():
        dataUpdate = RepoPlayerUpdate.get_all()
        return dataUpdate
    
    @staticmethod
    def put(request):
        reqs = {
            'playerupdate': request.data['playerupdate'],
            'player': request.data['player'],
            'judul_update': request.data.get('judul_update'),
            'deskripsi': request.data.get('deskripsi')
        }
        updated_update = RepoPlayerUpdate.put(reqs)
        return updated_update
    
    @staticmethod
    def delete(request):
        reqs = {
            'playerupdate': request.data['playerupdate']
        }
        delete_message = RepoPlayerUpdate.delete(reqs)
        return delete_message