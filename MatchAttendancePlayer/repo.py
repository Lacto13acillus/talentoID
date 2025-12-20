from django.shortcuts import get_object_or_404
from .models import MatchAttendancePlayer
from player.models import player
from pertandingan.models import pertandingan
from team.models import team
from stadion.models import stadion
from status.models import status
from season.models import season
from LineUp.models import LineUp

class RepoMatchAttendancePlayer:
    @staticmethod
    def _get_match_data(match):
        """Helper method to construct detailed match data."""
        if not match:
            return None

        team_home_data = {
            'team': match.tim_home.team,
            'nama_team': match.tim_home.nama_team,
            'kategori_team': match.tim_home.kategori_team,
            'logo_team': match.tim_home.logo_team.url if match.tim_home.logo_team else None
        }
        team_away_data = {
            'team': match.tim_away.team,
            'nama_team': match.tim_away.nama_team,
            'kategori_team': match.tim_away.kategori_team,
            'logo_team': match.tim_away.logo_team.url if match.tim_away.logo_team else None
        }
        schedule_data = None
        if match.jadwal:
            schedule_data = {
                'schedule': match.jadwal.schedule,
                'tanggal': match.jadwal.tanggal.isoformat() if match.jadwal.tanggal else None,
                'start_time': match.jadwal.start_time.strftime('%H:%M:%S') if match.jadwal.start_time else None,
                'end_time': match.jadwal.end_time.strftime('%H:%M:%S') if match.jadwal.end_time else None
            }
        stadion_data = None
        if match.lokasi:
            stadion_data = {
                'stadion': match.lokasi.stadion,
                'nama_stadion': match.lokasi.nama_stadion,
                'lokasi': match.lokasi.lokasi
            }
        status_data = None
        if match.status:
            status_data = {
                'status': match.status.status,
                'match_status': match.status.match_status
            }
        season_data = None
        if match.season:
            season_data = {
                'season': match.season.season,
                'nama_season': match.season.nama_season
            }
        formasi_data = None
        if match.formasi:  # Updated to use 'formasi' instead of 'formation_team_home'
            formasi_data = {
                'id_formasi': match.formasi.id_formasi,
                'formasi': match.formasi.formasi
            }

        return {
            'match': match.match,
            'nama_pertandingan': match.nama_pertandingan,
            'team_home': team_home_data,
            'team_away': team_away_data,
            'formasi': formasi_data,  # Updated to use 'formasi'
            'schedule': schedule_data,
            'stadion': stadion_data,
            'status': status_data,
            'season': season_data,
            'date': match.date.isoformat() if match.date else None,
            'start_time': match.start_time.strftime('%H:%M') if match.start_time else None,
            'end_time': match.end_time.strftime('%H:%M') if match.end_time else None
        }

    @staticmethod
    def post_match_attendance_player(req):
        Player = get_object_or_404(player, player=req['player'])
        Match = get_object_or_404(pertandingan, match=req['match']) if req.get('match') else None

        # Validate reason_absent if status is False
        status = req['status']
        reason_absent = req.get('reason_absent', '').strip()
        if not status and not reason_absent:
            raise ValueError("reason_absent is required and cannot be empty when the player is absent")

        new_attendance = MatchAttendancePlayer.objects.create(
            attendance_id=req['attendance_id'],
            player=Player,
            match=Match,
            status=status,
            reason_absent=reason_absent if reason_absent else None
        )

        return {
            'attendance_id': new_attendance.attendance_id,
            'player': {
                'player': new_attendance.player.player,
                'nama': new_attendance.player.nama,
                'posisi': new_attendance.player.posisi,
                'usia': new_attendance.player.usia,
                'kewarganegaraan': new_attendance.player.kewarganegaraan,
                'team': {
                    'team': new_attendance.player.tim.team,
                    'nama_team': new_attendance.player.tim.nama_team,
                    'kategori_team': new_attendance.player.tim.kategori_team,
                    'logo_team': new_attendance.player.tim.logo_team.url if new_attendance.player.tim.logo_team else None
                },
                'nomor_punggung': new_attendance.player.nomor_punggung,
                'tinggi_badan': new_attendance.player.tinggi_badan,
                'berat_badan': new_attendance.player.berat_badan,
                'tanggal_gabung': new_attendance.player.tanggal_gabung.isoformat() if new_attendance.player.tanggal_gabung else None,
                'kelamin': new_attendance.player.kelamin,
                'foto_profil': new_attendance.player.foto_profil.url if new_attendance.player.foto_profil else None
            },
            'match': RepoMatchAttendancePlayer._get_match_data(new_attendance.match),
            'status': new_attendance.status,
            'reason_absent': new_attendance.reason_absent
        }

    @staticmethod
    def get_match_attendance_player(attendance_id):
        attendance_data = get_object_or_404(MatchAttendancePlayer, attendance_id=attendance_id)

        return {
            'attendance_id': attendance_data.attendance_id,
            'player': {
                'player': attendance_data.player.player,
                'nama': attendance_data.player.nama,
                'posisi': attendance_data.player.posisi,
                'usia': attendance_data.player.usia,
                'kewarganegaraan': attendance_data.player.kewarganegaraan,
                'team': {
                    'team': attendance_data.player.tim.team,
                    'nama_team': attendance_data.player.tim.nama_team,
                    'kategori_team': attendance_data.player.tim.kategori_team,
                    'logo_team': attendance_data.player.tim.logo_team.url if attendance_data.player.tim.logo_team else None
                },
                'nomor_punggung': attendance_data.player.nomor_punggung,
                'tinggi_badan': attendance_data.player.tinggi_badan,
                'berat_badan': attendance_data.player.berat_badan,
                'tanggal_gabung': attendance_data.player.tanggal_gabung.isoformat() if attendance_data.player.tanggal_gabung else None,
                'kelamin': attendance_data.player.kelamin,
                'foto_profil': attendance_data.player.foto_profil.url if attendance_data.player.foto_profil else None
            },
            'match': RepoMatchAttendancePlayer._get_match_data(attendance_data.match),
            'status': attendance_data.status,
            'reason_absent': attendance_data.reason_absent
        }

    @staticmethod
    def get_all_match_attendance_player():
        attendance_list = MatchAttendancePlayer.objects.all()

        result = []
        for data in attendance_list:
            result.append({
                'attendance_id': data.attendance_id,
                'player': {
                    'player': data.player.player,
                    'nama': data.player.nama,
                    'posisi': data.player.posisi,
                    'usia': data.player.usia,
                    'kewarganegaraan': data.player.kewarganegaraan,
                    'team': {
                        'team': data.player.tim.team,
                        'nama_team': data.player.tim.nama_team,
                        'kategori_team': data.player.tim.kategori_team,
                        'logo_team': data.player.tim.logo_team.url if data.player.tim.logo_team else None
                    },
                    'nomor_punggung': data.player.nomor_punggung,
                    'tinggi_badan': data.player.tinggi_badan,
                    'berat_badan': data.player.berat_badan,
                    'tanggal_gabung': data.player.tanggal_gabung.isoformat() if data.player.tanggal_gabung else None,
                    'kelamin': data.player.kelamin,
                    'foto_profil': data.player.foto_profil.url if data.player.foto_profil else None
                },
                'match': RepoMatchAttendancePlayer._get_match_data(data.match),
                'status': data.status,
                'reason_absent': data.reason_absent
            })
        return result

    @staticmethod
    def get_by_player(player_id):
        Player = get_object_or_404(player, player=player_id)
        attendance_list = MatchAttendancePlayer.objects.filter(player=Player)

        result = []
        for data in attendance_list:
            result.append({
                'attendance_id': data.attendance_id,
                'player': {
                    'player': data.player.player,
                    'nama': data.player.nama,
                    'posisi': data.player.posisi,
                    'usia': data.player.usia,
                    'kewarganegaraan': data.player.kewarganegaraan,
                    'team': {
                        'team': data.player.tim.team,
                        'nama_team': data.player.tim.nama_team,
                        'kategori_team': data.player.tim.kategori_team,
                        'logo_team': data.player.tim.logo_team.url if data.player.tim.logo_team else None
                    },
                    'nomor_punggung': data.player.nomor_punggung,
                    'tinggi_badan': data.player.tinggi_badan,
                    'berat_badan': data.player.berat_badan,
                    'tanggal_gabung': data.player.tanggal_gabung.isoformat() if data.player.tanggal_gabung else None,
                    'kelamin': data.player.kelamin,
                    'foto_profil': data.player.foto_profil.url if data.player.foto_profil else None
                },
                'match': RepoMatchAttendancePlayer._get_match_data(data.match),
                'status': data.status,
                'reason_absent': data.reason_absent
            })
        return result
    
    @staticmethod
    def put_match_attendance_player(req):
        AttendanceData = get_object_or_404(MatchAttendancePlayer, attendance_id=req['attendance_id'])
        Player = get_object_or_404(player, player=req['player'])
        Match = get_object_or_404(pertandingan, match=req['match']) if req.get('match') else AttendanceData.match

        # Update fields
        AttendanceData.player = Player
        AttendanceData.match = Match
        AttendanceData.status = req.get('status', AttendanceData.status)
        AttendanceData.reason_absent = req.get('reason_absent', AttendanceData.reason_absent)

        # Validate reason_absent if status is False
        if not AttendanceData.status:
            reason_absent = AttendanceData.reason_absent.strip() if AttendanceData.reason_absent else ''
            if not reason_absent:
                raise ValueError("reason_absent is required and cannot be empty when the player is absent")

        AttendanceData.save()

        return {
            'attendance_id': AttendanceData.attendance_id,
            'player': {
                'player': AttendanceData.player.player,
                'nama': AttendanceData.player.nama,
                'posisi': AttendanceData.player.posisi,
                'usia': AttendanceData.player.usia,
                'kewarganegaraan': AttendanceData.player.kewarganegaraan,
                'team': {
                    'team': AttendanceData.player.tim.team,
                    'nama_team': AttendanceData.player.tim.nama_team,
                    'kategori_team': AttendanceData.player.tim.kategori_team,
                    'logo_team': AttendanceData.player.tim.logo_team.url if AttendanceData.player.tim.logo_team else None
                },
                'nomor_punggung': AttendanceData.player.nomor_punggung,
                'tinggi_badan': AttendanceData.player.tinggi_badan,
                'berat_badan': AttendanceData.player.berat_badan,
                'tanggal_gabung': AttendanceData.player.tanggal_gabung.isoformat() if AttendanceData.player.tanggal_gabung else None,
                'kelamin': AttendanceData.player.kelamin,
                'foto_profil': AttendanceData.player.foto_profil.url if AttendanceData.player.foto_profil else None
            },
            'match': RepoMatchAttendancePlayer._get_match_data(AttendanceData.match),
            'status': AttendanceData.status,
            'reason_absent': AttendanceData.reason_absent
        }

    @staticmethod
    def delete_match_attendance_player(req):
        AttendanceData = get_object_or_404(MatchAttendancePlayer, attendance_id=req['attendance_id'])
        attendance_id = AttendanceData.attendance_id
        AttendanceData.delete()
        return {'message': f"Match attendance player with id {attendance_id} has been deleted."}

    @staticmethod
    def get_by_match_id(match_id):
        """
        Retrieve player data for a specific match, including total players,
        total starting players ('main'), and total reserve players ('reserve') with their details,
        along with detailed match data.
        """
        # Get the match object
        Match = get_object_or_404(pertandingan, match=match_id)
        
        # Fetch LineUp data for the match
        lineup_data = LineUp.objects.filter(match=Match).values(
            'id_lineup',
            'player__player',
            'player__nama',
            'player__posisi',
            'player__nomor_punggung',
            'player__foto_profil',
            'index',
            'status'
        )
        
        # Separate starting and reserve players
        starting_players = [
            {
                'id_lineup': item['id_lineup'],
                'player': {
                    'player_id': item['player__player'],
                    'nama': item['player__nama'],
                    'posisi': item['player__posisi'],
                    'nomor_punggung': item['player__nomor_punggung'],
                    'foto_profil': item['player__foto_profil']
                },
                'index': item['index'],
                'status': item['status']
            }
            for item in lineup_data if item['status'] == 'main'
        ]
        
        reserve_players = [
            {
                'id_lineup': item['id_lineup'],
                'player': {
                    'player_id': item['player__player'],
                    'nama': item['player__nama'],
                    'posisi': item['player__posisi'],
                    'nomor_punggung': item['player__nomor_punggung'],
                    'foto_profil': item['player__foto_profil']
                },
                'index': item['index'],
                'status': item['status']
            }
            for item in lineup_data if item['status'] == 'reserve'
        ]
        
        # Calculate totals
        total_players = len(lineup_data)
        total_starting = len(starting_players)
        total_reserve = len(reserve_players)
        
        # Get detailed match data
        match_data = RepoMatchAttendancePlayer._get_match_data(Match)
        
        return {
            'match_id': match_id,
            'match_data': match_data,
            'total_players': total_players,
            'total_starting_players': total_starting,
            'starting_players': starting_players,
            'total_reserve_players': total_reserve,
            'reserve_players': reserve_players
        }