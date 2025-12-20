# repository/team_report_repository.py
from django.shortcuts import get_object_or_404
from .models import TeamReport
from team.models import team
from schedule.models import schedule

class RepoTeamReport:
    @staticmethod
    def post(req):
        Tim = get_object_or_404(team, team=req['team'])
        Jadwal = get_object_or_404(schedule, schedule=req['schedule'])

        new_team_report = TeamReport.objects.create(
            teamreport=req['teamreport'],
            tim=Tim,
            jadwal=Jadwal,
            hasil_pertandingan=req['hasil_pertandingan'],
            catatan=req['catatan']
        )
        return {
            'teamreport': new_team_report.teamreport,
            'team': {
                'team': Tim.team,
                'nama_team': Tim.nama_team,
                'kategori_team': Tim.kategori_team,
                'logo_team': Tim.logo_team.url if Tim.logo_team else None
            },
            'schedule': {
                'schedule': Jadwal.schedule,
                'tanggal': Jadwal.tanggal,
                'start_time': Jadwal.start_time,
                'end_time': Jadwal.end_time
            },
            'hasil_pertandingan': new_team_report.hasil_pertandingan,
            'catatan': new_team_report.catatan
        }
    
    @staticmethod
    def get(team_report_id):
        team_report_data = get_object_or_404(TeamReport, teamreport=team_report_id)
        return {
            'teamreport': team_report_data.teamreport,
            'team': {
                'team': team_report_data.tim.team,
                'nama_team': team_report_data.tim.nama_team,
                'kategori_team': team_report_data.tim.kategori_team,
                'logo_team': team_report_data.tim.logo_team.url if team_report_data.tim.logo_team else None
            },
            'schedule': {
                'schedule': team_report_data.jadwal.schedule,
                'tanggal': team_report_data.jadwal.tanggal,
                'start_time': team_report_data.jadwal.start_time,
                'end_time': team_report_data.jadwal.end_time
            },
            'hasil_pertandingan': team_report_data.hasil_pertandingan,
            'catatan': team_report_data.catatan
        }
    
    @staticmethod
    def get_all():
        team_reports = TeamReport.objects.all()
        return [{
            'teamreport': report.teamreport,
            'team': {
                'team': report.tim.team,
                'nama_team': report.tim.nama_team,
                'kategori_team': report.tim.kategori_team,
                'logo_team': report.tim.logo_team.url if report.tim.logo_team else None
            },
            'schedule': {
                'schedule': report.jadwal.schedule,
                'tanggal': report.jadwal.tanggal,
                'start_time': report.jadwal.start_time,
                'end_time': report.jadwal.end_time
            },
            'hasil_pertandingan': report.hasil_pertandingan,
            'catatan': report.catatan
        } for report in team_reports]
    
    @staticmethod
    def get_all_team_reports_by_team_id(team_id):
        team_reports = TeamReport.objects.filter(tim=team_id)
        return [{
            'teamreport': report.teamreport,
            'team': {
                'team': report.tim.team,
                'nama_team': report.tim.nama_team,
                'kategori_team': report.tim.kategori_team,
                'logo_team': report.tim.logo_team.url if report.tim.logo_team else None
            },
            'schedule': {
                'schedule': report.jadwal.schedule,
                'tanggal': report.jadwal.tanggal,
                'start_time': report.jadwal.start_time,
                'end_time': report.jadwal.end_time
            },
            'hasil_pertandingan': report.hasil_pertandingan,
            'catatan': report.catatan
        } for report in team_reports]

    @staticmethod
    def put(req):
        TeamReportData = get_object_or_404(TeamReport, teamreport=req['teamreport'])
        Tim = get_object_or_404(team, team=req['team'])
        Jadwal = get_object_or_404(schedule, schedule=req['schedule'])

        TeamReportData.tim = Tim
        TeamReportData.jadwal = Jadwal
        TeamReportData.hasil_pertandingan = req.get('hasil_pertandingan', TeamReportData.hasil_pertandingan)
        TeamReportData.catatan = req.get('catatan', TeamReportData.catatan)
        TeamReportData.save()

        return {
            'teamreport': TeamReportData.teamreport,
            'team': {
                'team': Tim.team,
                'nama_team': Tim.nama_team,
                'kategori_team': Tim.kategori_team,
                'logo_team': Tim.logo_team.url if Tim.logo_team else None
            },
            'schedule': {
                'schedule': Jadwal.schedule,
                'tanggal': Jadwal.tanggal,
                'start_time': Jadwal.start_time,
                'end_time': Jadwal.end_time
            },
            'hasil_pertandingan': TeamReportData.hasil_pertandingan,
            'catatan': TeamReportData.catatan
        }
    
    @staticmethod
    def delete(req):
        TeamReportData = get_object_or_404(TeamReport, teamreport=req['teamreport'])
        TeamReportData.delete()
        return {'message': f"TeamReport with id {req['teamreport']} has been deleted."}