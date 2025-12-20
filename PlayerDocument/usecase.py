# usecases/player_document_usecase.py
from .repo import RepoPlayerDocument
import uuid

class UsecasePlayerDocument:
    @staticmethod
    def post(request):
        reqs = {
            'playerdocument': uuid.uuid4(),
            'player': request.POST.get('player'),
            'jenis_dokumen': request.POST.get('jenis_dokumen'),
            'file_dokumen': request.FILES.get('file_dokumen')
        }
        return RepoPlayerDocument.post(reqs)
    
    @staticmethod
    def get(player_document_id):
        return RepoPlayerDocument.get(player_document_id)
    
    @staticmethod
    def get_all():
        return RepoPlayerDocument.get_all()
    
    @staticmethod
    def get_by_player(player_id):
        return RepoPlayerDocument.get_by_player(player_id)
    
    @staticmethod
    def put(request):
        reqs = {
            'playerdocument': request.POST.get('playerdocument'),
            'player': request.POST.get('player'),
            'jenis_dokumen': request.POST.get('jenis_dokumen'),
            'file_dokumen': request.FILES.get('file_dokumen')
        }
        return RepoPlayerDocument.put(reqs)
    
    @staticmethod
    def delete(request):
        reqs = {
            'playerdocument': request.POST.get('playerdocument')
        }
        return RepoPlayerDocument.delete(reqs)