# usecases/message_usecase.py
from .repo import RepoMessage
import uuid

class UsecaseMessage:
    @staticmethod
    def post(request):
        reqs = {
            'id': uuid.uuid4(),  
            'pengirim': request.data['pengirim'],
            'penerima': request.data['penerima'],
            'grup': request.data['grup'],
            'isi_pesan': request.data['isi_pesan'],
            'status_dibaca': request.data.get('status_dibaca', False)
        }
        dataPost = RepoMessage.post(reqs)
        return dataPost
    
    @staticmethod
    def get(message_id):
        dataMessage = RepoMessage.get(message_id)
        return dataMessage
    
    @staticmethod
    def get_all():
        return RepoMessage.get_all()
    
    @staticmethod
    def put(request):
        reqs = {
            'id': request.data['id'],
            'pengirim': request.data['pengirim'],
            'penerima': request.data['penerima'],
            'grup': request.data['grup'],
            'isi_pesan': request.data.get('isi_pesan'),
            'status_dibaca': request.data.get('status_dibaca')
        }
        updated_message = RepoMessage.put(reqs)
        return updated_message
    
    @staticmethod
    def delete(request):
        reqs = {
            'id': request.data['id']
        }
        delete_message = RepoMessage.delete(reqs)
        return delete_message