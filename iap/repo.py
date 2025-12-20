from django.shortcuts import get_object_or_404
from .models import iap
from player.models import player
from pertandingan.models import pertandingan
from team.models import team
from stadion.models import stadion
from status.models import status
from season.models import season
from LineUp.models import LineUp
from PlayerPerform.repo import RepoPlayerPerform
import uuid

class RepoIAP:
    @staticmethod
    def _get_match_data(match):
        """Helper method to construct detailed match data."""
        TeamHome = get_object_or_404(team, team=match.tim_home.team)
        TeamAway = get_object_or_404(team, team=match.tim_away.team)
        Schedule = match.jadwal
        Stadion = get_object_or_404(stadion, stadion=match.lokasi.stadion)
        Status = get_object_or_404(status, status=match.status.status)
        Season = get_object_or_404(season, season=match.season.season)

        # Fetch LineUp data for the match
        lineup_data = LineUp.objects.filter(match=match).values(
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
        if match.formasi:  # Diubah dari formation_team_home
            formasi_data = {
                'id_formasi': match.formasi.id_formasi,
                'formasi': match.formasi.formasi
            }

        schedule_data = None
        if Schedule:
            schedule_data = {
                'schedule': Schedule.schedule,
                'tanggal': Schedule.tanggal.isoformat() if Schedule.tanggal else None,
                'start_time': Schedule.start_time.strftime('%H:%M:%S') if Schedule.start_time else None,
                'end_time': Schedule.end_time.strftime('%H:%M:%S') if Schedule.end_time else None
            }

        return {
            'match': match.match,
            'nama_pertandingan': match.nama_pertandingan,
            'team_home': {
                'team': TeamHome.team,
                'nama_team': TeamHome.nama_team,
                'kategori_team': TeamHome.kategori_team,
                'logo_team': TeamHome.logo_team.url if TeamHome.logo_team else None
            },
            'team_away': {
                'team': TeamAway.team,
                'nama_team': TeamAway.nama_team,
                'kategori_team': TeamAway.kategori_team,
                'logo_team': TeamAway.logo_team.url if TeamAway.logo_team else None
            },
            'formasi': formasi_data,  # Diubah dari formation_team_home
            'lineup': lineup_response,
            'schedule': schedule_data,
            'stadion': {
                'stadion': Stadion.stadion,
                'nama_stadion': Stadion.nama_stadion,
                'lokasi': Stadion.lokasi
            },
            'status': {
                'status': Status.status,
                'match_status': Status.match_status
            },
            'season': {
                'season': Season.season,
                'nama_season': Season.nama_season
            },
            'date': match.date.isoformat(),
            'start_time': match.start_time.strftime('%H:%M'),
            'end_time': match.end_time.strftime('%H:%M')
        }

    @staticmethod
    def post(req):
        Player = get_object_or_404(player, player=req['player'])
        Match = get_object_or_404(pertandingan, match=req['match'])

        iap_list = []
        for item in req['iaps']:
            iap_list.append(iap(
                iap=str(uuid.uuid4()),
                player=Player,
                match=Match,
                category=item['category'],
                type=item['type'],
                current_achieve=item['current_achieve'],
                target=item['target']
            ))

        iap.objects.bulk_create(iap_list)

        # RepoPlayerPerform.calculate_and_update_performance(Player.player)

        return {
            'count': len(iap_list)
        }

    @staticmethod
    def get(iap_id):
        iap_record = get_object_or_404(iap, iap=iap_id)
        entries = [{
            'iap': iap_record.iap,
            'category': iap_record.category,
            'type': iap_record.type,
            'current_achieve': iap_record.current_achieve,
            'target': iap_record.target
        }]

        return {
            'iap': iap_id,
            'player': {
                'player': iap_record.player.player,
                'nama': iap_record.player.nama,
                'posisi': iap_record.player.posisi,
                'kewarganegaraan': iap_record.player.kewarganegaraan,
                'team': {
                    'team': iap_record.player.tim.team,
                    'nama_team': iap_record.player.tim.nama_team,
                    'kategori_team': iap_record.player.tim.kategori_team,
                    'logo_team': iap_record.player.tim.logo_team.url if iap_record.player.tim.logo_team else None
                },
                'nomor_punggung': iap_record.player.nomor_punggung,
                'tinggi_badan': iap_record.player.tinggi_badan,
                'berat_badan': iap_record.player.berat_badan,
                'tanggal_gabung': iap_record.player.tanggal_gabung.isoformat() if iap_record.player.tanggal_gabung else None,
                'kelamin': iap_record.player.kelamin,
                'foto_profil': iap_record.player.foto_profil.url if iap_record.player.foto_profil else None
            },
            'match': RepoIAP._get_match_data(iap_record.match),
            'entries': entries
        }

    @staticmethod
    def get_all():
        players = player.objects.all()
        result = []

        for Player in players:
            iap_records = iap.objects.filter(player=Player)
            if iap_records.exists():
                entries = [
                    {
                        'iap': record.iap,
                        'category': record.category,
                        'type': record.type,
                        'current_achieve': record.current_achieve,
                        'target': record.target
                    }
                    for record in iap_records
                ]
                # Use the first record to get the match details
                first_record = iap_records.first()
                result.append({
                    'iap': str(uuid.uuid4()),
                    'player': {
                        'player': Player.player,
                        'nama': Player.nama,
                        'posisi': Player.posisi,
                        'kewarganegaraan': Player.kewarganegaraan,
                        'team': {
                            'team': Player.tim.team,
                            'nama_team': Player.tim.nama_team,
                            'kategori_team': Player.tim.kategori_team,
                            'logo_team': Player.tim.logo_team.url if Player.tim.logo_team else None
                        },
                        'nomor_punggung': Player.nomor_punggung,
                        'tinggi_badan': Player.tinggi_badan,
                        'berat_badan': Player.berat_badan,
                        'tanggal_gabung': Player.tanggal_gabung.isoformat() if Player.tanggal_gabung else None,
                        'kelamin': Player.kelamin,
                        'foto_profil': Player.foto_profil.url if Player.foto_profil else None
                    },
                    'match': RepoIAP._get_match_data(first_record.match),
                    'entries': entries
                })

        return result

    @staticmethod
    def get_by_player_and_match(player_id, match_id):
        Player = get_object_or_404(player, player=player_id)
        Match = get_object_or_404(pertandingan, match=match_id)
        iap_records = iap.objects.filter(player=Player, match=Match)

        if not iap_records.exists():
            return {
                'iap': str(uuid.uuid4()),
                'player': {
                    'player': Player.player,
                    'nama': Player.nama,
                    'posisi': Player.posisi,
                    'kewarganegaraan': Player.kewarganegaraan,
                    'team': {
                        'team': Player.tim.team,
                        'nama_team': Player.tim.nama_team,
                        'kategori_team': Player.tim.kategori_team,
                        'logo_team': Player.tim.logo_team.url if Player.tim.logo_team else None
                    },
                    'nomor_punggung': Player.nomor_punggung,
                    'tinggi_badan': Player.tinggi_badan,
                    'berat_badan': Player.berat_badan,
                    'tanggal_gabung': Player.tanggal_gabung.isoformat() if Player.tanggal_gabung else None,
                    'kelamin': Player.kelamin,
                    'foto_profil': Player.foto_profil.url if Player.foto_profil else None
                },
                'match': RepoIAP._get_match_data(Match),
                'entries': []
            }

        entries = [
            {
                'iap': record.iap,
                'category': record.category,
                'type': record.type,
                'current_achieve': record.current_achieve,
                'target': record.target
            }
            for record in iap_records
        ]

        return {
            'iap': str(uuid.uuid4()),
            'player': {
                'player': Player.player,
                'nama': Player.nama,
                'posisi': Player.posisi,
                'kewarganegaraan': Player.kewarganegaraan,
                'team': {
                    'team': Player.tim.team,
                    'nama_team': Player.tim.nama_team,
                    'kategori_team': Player.tim.kategori_team,
                    'logo_team': Player.tim.logo_team.url if Player.tim.logo_team else None
                },
                'nomor_punggung': Player.nomor_punggung,
                'tinggi_badan': Player.tinggi_badan,
                'berat_badan': Player.berat_badan,
                'tanggal_gabung': Player.tanggal_gabung.isoformat() if Player.tanggal_gabung else None,
                'kelamin': Player.kelamin,
                'foto_profil': Player.foto_profil.url if Player.foto_profil else None
            },
            'match': RepoIAP._get_match_data(Match),
            'entries': entries
        }

    @staticmethod
    def put(req):
        iapsu = get_object_or_404(iap, iap=req['iap'])
        Player = get_object_or_404(player, player=req['player'])
        Match = get_object_or_404(pertandingan, match=req['match']) if req.get('match') else iapsu.match

        iapsu.player = Player
        iapsu.match = Match
        iapsu.category = req.get('category', iapsu.category)
        iapsu.type = req.get('type', iapsu.type)
        iapsu.current_achieve = req.get('current_achieve', iapsu.current_achieve)
        iapsu.target = req.get('target', iapsu.target)
        iapsu.save()

        RepoPlayerPerform.calculate_and_update_performance(Player.player)

        entries = [{
            'iap': iapsu.iap,
            'category': iapsu.category,
            'type': iapsu.type,
            'current_achieve': iapsu.current_achieve,
            'target': iapsu.target
        }]

        return {
            'iap': req['iap'],
            'player': {
                'player': Player.player,
                'nama': Player.nama,
                'posisi': Player.posisi,
                'kewarganegaraan': Player.kewarganegaraan,
                'team': {
                    'team': Player.tim.team,
                    'nama_team': Player.tim.nama_team,
                    'kategori_team': Player.tim.kategori_team,
                    'logo_team': Player.tim.logo_team.url if Player.tim.logo_team else None
                },
                'nomor_punggung': Player.nomor_punggung,
                'tinggi_badan': Player.tinggi_badan,
                'berat_badan': Player.berat_badan,
                'tanggal_gabung': Player.tanggal_gabung.isoformat() if Player.tanggal_gabung else None,
                'kelamin': Player.kelamin,
                'foto_profil': Player.foto_profil.url if Player.foto_profil else None
            },
            'match': RepoIAP._get_match_data(iapsu.match),
            'entries': entries
        }

    @staticmethod
    def delete(req):
        iapsu = get_object_or_404(iap, iap=req['iap'])
        player_id = iapsu.player.player
        iapsu.delete()

        RepoPlayerPerform.calculate_and_update_performance(player_id)

        return {'message': f"IAP with id {req['iap']} has been deleted."}
