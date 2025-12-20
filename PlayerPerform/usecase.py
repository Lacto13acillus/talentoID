from .repo import RepoPlayerPerform
import uuid

class UsecasePlayerPerform:
    @staticmethod
    def calculate_and_update_performance(player_id):
        return RepoPlayerPerform.calculate_and_update_performance(player_id)

    @staticmethod
    def post(request):
        reqs = {
            'playerperform': uuid.uuid4(),
            'player': request.data['player'],
            'kick_test': request.data['kick_test'],
            'tactical': request.data['tactical'],
            'shoot_focus': request.data['shoot_focus'],
            'analyst': request.data['analyst'],
            'shoot': request.data['shoot']
        }
        dataPost = RepoPlayerPerform.post(reqs)
        return dataPost
    
    @staticmethod
    def get(player_perform_id):
        dataPlayerPerform = RepoPlayerPerform.get(player_perform_id)
        return dataPlayerPerform
    
    @staticmethod
    def get_all():
        return RepoPlayerPerform.get_all()
    
    @staticmethod
    def put(request):
        reqs = {
            'playerperform': request.data['playerperform'],
            'player': request.data['player'],
            'kick_test': request.data.get('kick_test'),
            'tactical': request.data.get('tactical'),
            'shoot_focus': request.data.get('shoot_focus'),
            'analyst': request.data.get('analyst'),
            'shoot': request.data.get('shoot')
        }
        updated_player_perform = RepoPlayerPerform.put(reqs)
        return updated_player_perform
    
    @staticmethod
    def delete(request):
        reqs = {
            'playerperform': request.data['playerperform']
        }
        delete_player_perform = RepoPlayerPerform.delete(reqs)
        return delete_player_perform