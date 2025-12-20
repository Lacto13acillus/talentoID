from .repo import RepoSession
import uuid

class UsecaseSession:
    @staticmethod
    def post(request):
        reqs = {
            'session': uuid.uuid4(),  # Generate UUID untuk session
            'player': request.data['player'],
            'session_type': request.data['session_type'],
            'minutes_date': request.data['minutes_date'],
            'notes': request.data['notes']
        }
        dataPost = RepoSession.post(reqs)
        return dataPost
    
    @staticmethod
    def get(session_id):
        dataSession = RepoSession.get(session_id)
        return dataSession
    
    @staticmethod
    def get_all():
        dataSession = RepoSession.get_all()
        return dataSession
    
    @staticmethod
    def put(request):
        reqs = {
            'session': request.data['session'],
            'player': request.data.get('player'),
            'session_type': request.data.get('session_type'),
            'minutes_date': request.data.get('minutes_date'),
            'notes': request.data.get('notes')
        }
        updated_session = RepoSession.put(reqs)
        return updated_session
    
    @staticmethod
    def delete(request):
        reqs = {
            'session': request.data['session']
        }
        delete_message = RepoSession.delete(reqs)
        return delete_message