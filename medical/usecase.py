# usecases/medical_usecase.py
from .repo import RepoMedical
import uuid

class UsecaseMedical:
    @staticmethod
    def post(request):
        reqs = {
            'medical': uuid.uuid4(),  # Generate UUID untuk medical
            'player': request.data['player'],
            'medical_history': request.data['medical_history'],
            'session': request.data['session']
        }
        dataPost = RepoMedical.post(reqs)
        return dataPost
    
    @staticmethod
    def get(medical_id):
        dataMedical = RepoMedical.get(medical_id)
        return dataMedical
    
    @staticmethod
    def get_all():
        dataMedical = RepoMedical.get_all()
        return dataMedical
    
    @staticmethod
    def put(request):
        reqs = {
            'medical': request.data['medical'],
            'player': request.data['player'],
            'medical_history': request.data['medical_history'],
            'session': request.data['session']
        }
        updated_medical = RepoMedical.put(reqs)
        return updated_medical
    
    @staticmethod
    def delete(request):
        reqs = {
            'medical': request.data['medical']
        }
        delete_medical = RepoMedical.delete(reqs)
        return delete_medical