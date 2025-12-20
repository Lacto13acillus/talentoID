from django.shortcuts import get_object_or_404
from .models import stats
from player.models import player
from pertandingan.models import pertandingan
from team.models import team
from schedule.models import schedule
from stadion.models import stadion
from status.models import status
from formations.models import Formation
from season.models import season
from LineUp.models import LineUp
import uuid

class RepoStats:
    @staticmethod
    def _get_match_data(match_instance):
        """Helper method to construct detailed match data consistent with RepoPertandingan."""
        if not match_instance:
            return None

        # Fetch LineUp data for the match
        lineup_data = LineUp.objects.filter(match=match_instance).values(
            'id_lineup',
            'player__player',
            'player__nama',
            'player__posisi',
            'player__nomor_punggung',
            'player__foto_profil',
            'index',
            'status'
        )
        lineup_response = [{
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
        } for item in lineup_data]

        formasi_data = None
        if match_instance.formasi:
            formasi_data = {
                'id_formasi': match_instance.formasi.id_formasi,
                'formasi': match_instance.formasi.formasi
            }

        schedule_data = None
        if match_instance.jadwal:
            schedule_data = {
                'schedule': match_instance.jadwal.schedule,
                'tanggal': match_instance.jadwal.tanggal.isoformat() if match_instance.jadwal.tanggal else None,
                'start_time': match_instance.jadwal.start_time.strftime('%H:%M:%S') if match_instance.jadwal.start_time else None,
                'end_time': match_instance.jadwal.end_time.strftime('%H:%M:%S') if match_instance.jadwal.end_time else None
            }

        return {
            'match': match_instance.match,
            'nama_pertandingan': match_instance.nama_pertandingan,
            'team_home': {
                'team': match_instance.tim_home.team,
                'nama_team': match_instance.tim_home.nama_team,
                'kategori_team': match_instance.tim_home.kategori_team,
                'logo_team': match_instance.tim_home.logo_team.url if match_instance.tim_home.logo_team else None
            },
            'team_away': {
                'team': match_instance.tim_away.team,
                'nama_team': match_instance.tim_away.nama_team,
                'kategori_team': match_instance.tim_away.kategori_team,
                'logo_team': match_instance.tim_away.logo_team.url if match_instance.tim_away.logo_team else None
            },
            'formasi': formasi_data,
            'lineup': lineup_response,
            'schedule': schedule_data,
            'stadion': {
                'stadion': match_instance.lokasi.stadion,
                'nama_stadion': match_instance.lokasi.nama_stadion,
                'lokasi': match_instance.lokasi.lokasi
            },
            'status': {
                'status': match_instance.status.status,
                'match_status': match_instance.status.match_status
            },
            'season': {
                'season': match_instance.season.season,
                'nama_season': match_instance.season.nama_season
            },
            'date': match_instance.date.isoformat(),
            'start_time': match_instance.start_time.strftime('%H:%M'),
            'end_time': match_instance.end_time.strftime('%H:%M')
        }

    @staticmethod
    def post(req):
        Match = get_object_or_404(pertandingan, match=req['match'])
        stats_list = []

        for stats_data in req['stats_list']:
            Player = get_object_or_404(player, player=stats_data['player'])
            stats_id = str(uuid.uuid4())

            new_stats = stats.objects.create(
                stats=stats_id,
                match=Match,
                player=Player,
                position_played=stats_data['position_played'],
                minutes_played=stats_data['minutes_played'],
                overall_rating=stats_data['overall_rating']
            )

            stats_list.append({
                'stats': new_stats.stats,
                'match': RepoStats._get_match_data(new_stats.match),
                'player': {
                    'player': new_stats.player.player,
                    'nama': new_stats.player.nama,
                    'posisi': new_stats.player.posisi,
                    'usia': new_stats.player.usia,
                    'kewarganegaraan': new_stats.player.kewarganegaraan,
                    'team': {
                        'team': new_stats.player.tim.team if new_stats.player.tim else None,
                        'nama_team': new_stats.player.tim.nama_team if new_stats.player.tim else None,
                        'kategori_team': new_stats.player.tim.kategori_team if new_stats.player.tim else None,
                        'logo_team': new_stats.player.tim.logo_team.url if new_stats.player.tim and new_stats.player.tim.logo_team else None
                    },
                    'nomor_punggung': new_stats.player.nomor_punggung,
                    'tinggi_badan': new_stats.player.tinggi_badan,
                    'berat_badan': new_stats.player.berat_badan,
                    'tanggal_gabung': new_stats.player.tanggal_gabung.isoformat() if new_stats.player.tanggal_gabung else None,
                    'kelamin': new_stats.player.kelamin,
                    'foto_profil': new_stats.player.foto_profil.url if new_stats.player.foto_profil else None
                },
                'position_played': new_stats.position_played,
                'minutes_played': new_stats.minutes_played,
                'overall_rating': new_stats.overall_rating
            })

        return stats_list

    @staticmethod
    def get(stats_id):
        stats_data = get_object_or_404(stats, stats=stats_id)
        return {
            'stats': stats_data.stats,
            'match': RepoStats._get_match_data(stats_data.match),
            'player': {
                'player': stats_data.player.player,
                'nama': stats_data.player.nama,
                'posisi': stats_data.player.posisi,
                'usia': stats_data.player.usia,
                'kewarganegaraan': stats_data.player.kewarganegaraan,
                'team': {
                    'team': stats_data.player.tim.team if stats_data.player.tim else None,
                    'nama_team': stats_data.player.tim.nama_team if stats_data.player.tim else None,
                    'kategori_team': stats_data.player.tim.kategori_team if stats_data.player.tim else None,
                    'logo_team': stats_data.player.tim.logo_team.url if stats_data.player.tim and stats_data.player.tim.logo_team else None
                },
                'nomor_punggung': stats_data.player.nomor_punggung,
                'tinggi_badan': stats_data.player.tinggi_badan,
                'berat_badan': stats_data.player.berat_badan,
                'tanggal_gabung': stats_data.player.tanggal_gabung.isoformat() if stats_data.player.tanggal_gabung else None,
                'kelamin': stats_data.player.kelamin,
                'foto_profil': stats_data.player.foto_profil.url if stats_data.player.foto_profil else None
            },
            'position_played': stats_data.position_played,
            'minutes_played': stats_data.minutes_played,
            'overall_rating': stats_data.overall_rating
        }

    @staticmethod
    def get_all():
        stats_list = stats.objects.all()
        result = []
        for stats_data in stats_list:
            result.append({
                'stats': stats_data.stats,
                'match': RepoStats._get_match_data(stats_data.match),
                'player': {
                    'player': stats_data.player.player,
                    'nama': stats_data.player.nama,
                    'posisi': stats_data.player.posisi,
                    'usia': stats_data.player.usia,
                    'kewarganegaraan': stats_data.player.kewarganegaraan,
                    'team': {
                        'team': stats_data.player.tim.team if stats_data.player.tim else None,
                        'nama_team': stats_data.player.tim.nama_team if stats_data.player.tim else None,
                        'kategori_team': stats_data.player.tim.kategori_team if stats_data.player.tim else None,
                        'logo_team': stats_data.player.tim.logo_team.url if stats_data.player.tim and stats_data.player.tim.logo_team else None
                    },
                    'nomor_punggung': stats_data.player.nomor_punggung,
                    'tinggi_badan': stats_data.player.tinggi_badan,
                    'berat_badan': stats_data.player.berat_badan,
                    'tanggal_gabung': stats_data.player.tanggal_gabung.isoformat() if stats_data.player.tanggal_gabung else None,
                    'kelamin': stats_data.player.kelamin,
                    'foto_profil': stats_data.player.foto_profil.url if stats_data.player.foto_profil else None
                },
                'position_played': stats_data.position_played,
                'minutes_played': stats_data.minutes_played,
                'overall_rating': stats_data.overall_rating
            })
        return result

    @staticmethod
    def get_by_player(player_id):
        Player = get_object_or_404(player, player=player_id)
        stats_list = stats.objects.filter(player=Player)
        result = []
        for stats_data in stats_list:
            result.append({
                'stats': stats_data.stats,
                'match': RepoStats._get_match_data(stats_data.match),
                'player': {
                    'player': stats_data.player.player,
                    'nama': stats_data.player.nama,
                    'posisi': stats_data.player.posisi,
                    'usia': stats_data.player.usia,
                    'kewarganegaraan': stats_data.player.kewarganegaraan,
                    'team': {
                        'team': stats_data.player.tim.team if stats_data.player.tim else None,
                        'nama_team': stats_data.player.tim.nama_team if stats_data.player.tim else None,
                        'kategori_team': stats_data.player.tim.kategori_team if stats_data.player.tim else None,
                        'logo_team': stats_data.player.tim.logo_team.url if stats_data.player.tim and stats_data.player.tim.logo_team else None
                    },
                    'nomor_punggung': stats_data.player.nomor_punggung,
                    'tinggi_badan': stats_data.player.tinggi_badan,
                    'berat_badan': stats_data.player.berat_badan,
                    'tanggal_gabung': stats_data.player.tanggal_gabung.isoformat() if stats_data.player.tanggal_gabung else None,
                    'kelamin': stats_data.player.kelamin,
                    'foto_profil': stats_data.player.foto_profil.url if stats_data.player.foto_profil else None
                },
                'position_played': stats_data.position_played,
                'minutes_played': stats_data.minutes_played,
                'overall_rating': stats_data.overall_rating
            })
        return result

    @staticmethod
    def put(req):
        StatsData = get_object_or_404(stats, stats=req['stats'])
        Player = get_object_or_404(player, player=req['player'])
        Match = get_object_or_404(pertandingan, match=req['match'])

        StatsData.match = Match
        StatsData.player = Player
        StatsData.position_played = req.get('position_played', StatsData.position_played)
        StatsData.minutes_played = req.get('minutes_played', StatsData.minutes_played)
        StatsData.overall_rating = req.get('overall_rating', StatsData.overall_rating)
        StatsData.save()

        return {
            'stats': StatsData.stats,
            'match': RepoStats._get_match_data(StatsData.match),
            'player': {
                'player': StatsData.player.player,
                'nama': StatsData.player.nama,
                'posisi': StatsData.player.posisi,
                'usia': StatsData.player.usia,
                'kewarganegaraan': StatsData.player.kewarganegaraan,
                'team': {
                    'team': StatsData.player.tim.team if StatsData.player.tim else None,
                    'nama_team': StatsData.player.tim.nama_team if StatsData.player.tim else None,
                    'kategori_team': StatsData.player.tim.kategori_team if StatsData.player.tim else None,
                    'logo_team': StatsData.player.tim.logo_team.url if StatsData.player.tim and StatsData.player.tim.logo_team else None
                },
                'nomor_punggung': StatsData.player.nomor_punggung,
                'tinggi_badan': StatsData.player.tinggi_badan,
                'berat_badan': StatsData.player.berat_badan,
                'tanggal_gabung': StatsData.player.tanggal_gabung.isoformat() if StatsData.player.tanggal_gabung else None,
                'kelamin': StatsData.player.kelamin,
                'foto_profil': StatsData.player.foto_profil.url if StatsData.player.foto_profil else None
            },
            'position_played': StatsData.position_played,
            'minutes_played': StatsData.minutes_played,
            'overall_rating': StatsData.overall_rating
        }

    @staticmethod
    def delete(req):
        StatsData = get_object_or_404(stats, stats=req['stats'])
        stats_id = StatsData.stats
        StatsData.delete()
        return {'message': f"Stats with id {stats_id} has been deleted."}