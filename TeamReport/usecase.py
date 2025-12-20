# usecases/team_report_usecase.py
from .repo import RepoTeamReport
import uuid

class UsecaseTeamReport:
    @staticmethod
    def post(request):
        reqs = {
            'teamreport': uuid.uuid4(),  # Generate UUID untuk teamreport
            'team': request.data['team'],
            'jadwal': request.data['schedule'],
            'hasil_pertandingan': request.data['hasil_pertandingan'],
            'catatan': request.data['catatan']
        }
        dataPost = RepoTeamReport.post(reqs)
        return dataPost
    
    @staticmethod
    def get(team_report_id):
        dataTeamReport = RepoTeamReport.get(team_report_id)
        return dataTeamReport
    
    @staticmethod
    def get_all():
        return RepoTeamReport.get_all()
    
    @staticmethod
    def get_all_team_reports_by_team_id(team_id):
        return RepoTeamReport.get_all_team_reports_by_team_id(team_id)
    
    @staticmethod
    def put(request):
        reqs = {
            'teamreport': request.data['teamreport'],
            'team': request.data['team'],
            'schedule': request.data['schedule'],
            'hasil_pertandingan': request.data.get('hasil_pertandingan'),
            'catatan': request.data.get('catatan')
        }
        updated_team_report = RepoTeamReport.put(reqs)
        return updated_team_report
    
    @staticmethod
    def delete(request):
        reqs = {
            'teamreport': request.data['teamreport']
        }
        delete_team_report = RepoTeamReport.delete(reqs)
        return delete_team_report