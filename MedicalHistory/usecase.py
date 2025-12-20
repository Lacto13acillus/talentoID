# usecases/medical_history_usecase.py
from .repo import RepoMedicalHistory
import uuid

class UsecaseMedicalHistory:
    @staticmethod
    def post(request):
        reqs = {
            'medicalhistory': uuid.uuid4(),
            'player': request.POST.get('player'),
            'jenis_pemeriksaan': request.POST.get('jenis_pemeriksaan'),
            'file_dokumen': request.FILES.get('file_dokumen')
        }
        return RepoMedicalHistory.post(reqs)
    
    @staticmethod
    def get(medical_history_id):
        return RepoMedicalHistory.get(medical_history_id)
    
    @staticmethod
    def get_all():
        return RepoMedicalHistory.get_all()
    
    @staticmethod
    def get_by_player(player_id):
        return RepoMedicalHistory.get_by_player(player_id)
    
    @staticmethod
    def put(request):
        reqs = {
            'medicalhistory': request.POST.get('medicalhistory'),
            'player': request.POST.get('player'),
            'jenis_pemeriksaan': request.POST.get('jenis_pemeriksaan'),
            'file_dokumen': request.FILES.get('file_dokumen')
        }
        return RepoMedicalHistory.put(reqs)
    
    @staticmethod
    def delete(request):
        reqs = {
            'medicalhistory': request.POST.get('medicalhistory')
        }
        return RepoMedicalHistory.delete(reqs)