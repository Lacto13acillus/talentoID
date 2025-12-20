# usecases/notif_usecase.py
from .repo import RepoNotif
import uuid

class UsecaseNotif:
    @staticmethod
    def post(request):
        reqs = {
            'id': uuid.uuid4(),  # Generate UUID untuk id
            'penerima': request.data['penerima'],
            'grup': request.data['grup'],
            'status_dibaca': request.data.get('status_dibaca', False)
        }
        dataPost = RepoNotif.post(reqs)
        return dataPost
    
    @staticmethod
    def get(notif_id):
        dataNotif = RepoNotif.get(notif_id)
        return dataNotif
    
    @staticmethod
    def get_all():
        return RepoNotif.get_all()
    
    @staticmethod
    def put(request):
        reqs = {
            'id': request.data['id'],
            'penerima': request.data['penerima'],
            'grup': request.data['grup'],
            'status_dibaca': request.data.get('status_dibaca')
        }
        updated_notif = RepoNotif.put(reqs)
        return updated_notif
    
    @staticmethod
    def delete(request):
        reqs = {
            'id': request.data['id']
        }
        delete_notif = RepoNotif.delete(reqs)
        return delete_notif