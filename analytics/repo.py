# repository/analytics_repository.py
from django.shortcuts import get_object_or_404
from .models import analytics
from team.models import team

class RepoAnalytics:
    @staticmethod
    def post(req):
        Tim = get_object_or_404(team, team=req['team'])

        new_analytics = analytics.objects.create(
            analytics=req['analytics'],
            tim=Tim,
            kick_test=req['kick_test'],
            tactical=req['tactical'],
            shoot_focus=req['shoot_focus'],
            analyst=req['analyst']
        )
        return {
            'analytics': new_analytics.analytics,
            'team': {
                'id': Tim.team,
                'nama_team': Tim.nama_team,
                'kategori_team': Tim.kategori_team
            },
            'kick_test': new_analytics.kick_test,
            'tactical': new_analytics.tactical,
            'shoot_focus': new_analytics.shoot_focus,
            'analyst': new_analytics.analyst
        }
    
    @staticmethod
    def get(analytics_id):
        analytics_data = get_object_or_404(analytics, analytics=analytics_id)
        return {
            'analytics': analytics_data.analytics,
            'team': {
                'team': analytics_data.tim.team,
                'nama_team': analytics_data.tim.nama_team,
                'kategori_team': analytics_data.tim.kategori_team
            },
            'kick_test': analytics_data.kick_test,
            'tactical': analytics_data.tactical,
            'shoot_focus': analytics_data.shoot_focus,
            'analyst': analytics_data.analyst
        }
    
    @staticmethod
    def get_all():
        analytics_records = analytics.objects.all()
        return [{
            'analytics': record.analytics,
            'team': {
                'team': record.tim.team,
                'nama_team': record.tim.nama_team,
                'kategori_team': record.tim.kategori_team
            },
            'kick_test': record.kick_test,
            'tactical': record.tactical,
            'shoot_focus': record.shoot_focus,
            'analyst': record.analyst
        } for record in analytics_records]

    @staticmethod
    def put(req):
        AnalyticsData = get_object_or_404(analytics, analytics=req['analytics'])
        Tim = get_object_or_404(team, team=req['team'])

        AnalyticsData.tim = Tim
        AnalyticsData.kick_test = req.get('kick_test', AnalyticsData.kick_test)
        AnalyticsData.tactical = req.get('tactical', AnalyticsData.tactical)
        AnalyticsData.shoot_focus = req.get('shoot_focus', AnalyticsData.shoot_focus)
        AnalyticsData.analyst = req.get('analyst', AnalyticsData.analyst)
        AnalyticsData.save()

        return {
            'analytics': AnalyticsData.analytics,
            'team': {
                'team': Tim.team,
                'nama_team': Tim.nama_team,
                'kategori_team': Tim.kategori_team
            },
            'kick_test': AnalyticsData.kick_test,
            'tactical': AnalyticsData.tactical,
            'shoot_focus': AnalyticsData.shoot_focus,
            'analyst': AnalyticsData.analyst
        }
    
    @staticmethod
    def delete(req):
        AnalyticsData = get_object_or_404(analytics, analytics=req['analytics'])
        AnalyticsData.delete()
        return {'message': f"Analytics with id {req['analytics']} has been deleted."}