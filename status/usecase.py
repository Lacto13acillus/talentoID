from .repo import RepoStatus
import uuid

class UsecaseStatus:
    @staticmethod
    def post(request):
        reqs = {
            'status': uuid.uuid4(),  
            'match_status': request.data['match_status']
        }
        dataPost = RepoStatus.post(reqs)
        return dataPost
    
    @staticmethod
    def get(status_id):
        dataStatus = RepoStatus.get(status_id)
        return dataStatus
    
    @staticmethod
    def get_all():
        return RepoStatus.get_all()
    
    def put(self, request): 
        reqs = {
            'status': request.data['status'],
            'match_status': request.data.get('match_status', '')
        }
        updated_status = RepoStatus.put(reqs)
        return updated_status
    
    def delete(self, request):  
        reqs = {
            'status': request.data['status']
        }
        delete_message = RepoStatus.delete(reqs)
        return delete_message