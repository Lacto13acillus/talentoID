# usecases/analytics_usecase.py
from .repo import RepoAnalytics
import uuid

class UsecaseAnalytics:
    @staticmethod
    def post(request):
        reqs = {
            'analytics': uuid.uuid4(),  # Generate UUID untuk analytics
            'team': request.data['team'],
            'kick_test': request.data['kick_test'],
            'tactical': request.data['tactical'],
            'shoot_focus': request.data['shoot_focus'],
            'analyst': request.data['analyst']
        }
        dataPost = RepoAnalytics.post(reqs)
        return dataPost
    
    @staticmethod
    def get(analytics_id):
        dataAnalytics = RepoAnalytics.get(analytics_id)
        return dataAnalytics
    
    @staticmethod
    def get_all():
        return RepoAnalytics.get_all()
    
    @staticmethod
    def put(request):
        reqs = {
            'analytics': request.data['analytics'],
            'team': request.data['team'],
            'kick_test': request.data.get('kick_test'),
            'tactical': request.data.get('tactical'),
            'shoot_focus': request.data.get('shoot_focus'),
            'analyst': request.data.get('analyst')
        }
        updated_analytics = RepoAnalytics.put(reqs)
        return updated_analytics
    
    @staticmethod
    def delete(request):
        reqs = {
            'analytics': request.data['analytics']
        }
        delete_analytics = RepoAnalytics.delete(reqs)
        return delete_analytics