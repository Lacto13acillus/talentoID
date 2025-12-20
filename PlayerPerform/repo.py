from django.shortcuts import get_object_or_404
from .models import PlayerPerform
from player.models import player
from iap.models import iap
import uuid

class RepoPlayerPerform:
    @staticmethod
    def calculate_and_update_performance(player_id):
        # Ambil data IAP untuk pemain
        iaps = iap.objects.filter(player=player_id)

        # Inisialisasi dictionary untuk menyimpan nilai indikator
        performance = {
            'kick_test': 0.0,
            'tactical': 0.0,
            'analyst': 0.0,
            'shoot_focus': 0.0,
            'shoot': 0.0
        }

        # Pemetaan IAP ke indikator Player Performance
        iap_mapping = {
            'Ball Control': 'kick_test',
            'Tackling': 'tactical',
            'Passing': 'analyst',
            'Heading': 'shoot_focus',
            'Shooting': 'shoot'
        }

        # Hitung persentase untuk setiap indikator
        for iap_data in iaps:
            if iap_data.type in iap_mapping:
                target = iap_data.target if iap_data.target != 0 else 1  # Hindari pembagian dengan nol
                percentage = (iap_data.current_achieve / target) * 100
                performance[iap_mapping[iap_data.type]] = round(min(percentage, 100), 2)  # Batasi maksimum 100%

        # Cek apakah record PlayerPerform sudah ada untuk pemain ini
        try:
            player_perform = PlayerPerform.objects.get(player=player_id)
            # Update record yang sudah ada
            player_perform.kick_test = performance['kick_test']
            player_perform.tactical = performance['tactical']
            player_perform.analyst = performance['analyst']
            player_perform.shoot_focus = performance['shoot_focus']
            player_perform.shoot = performance['shoot']
            player_perform.save()
        except PlayerPerform.DoesNotExist:
            # Buat record baru jika belum ada
            Player = get_object_or_404(player, player=player_id)
            player_perform = PlayerPerform.objects.create(
                playerperform=str(uuid.uuid4()),  # Generate UUID untuk playerperform
                player=Player,
                kick_test=performance['kick_test'],
                tactical=performance['tactical'],
                shoot_focus=performance['shoot_focus'],
                analyst=performance['analyst'],
                shoot=performance['shoot']
            )

        return {
            'playerperform': player_perform.playerperform,
            'player': {
                'id': player_perform.player.player,
                'nama': player_perform.player.nama,
                'posisi': player_perform.player.posisi,
                'usia': player_perform.player.usia,
                'kewarganegaraan': player_perform.player.kewarganegaraan,
                'team': {
                    'id': player_perform.player.tim.team,
                    'nama_team': player_perform.player.tim.nama_team,
                    'kategori_team': player_perform.player.tim.kategori_team,
                    'logo_team': player_perform.player.tim.logo_team.url if player_perform.player.tim.logo_team else None
                },
                'nomor_punggung': player_perform.player.nomor_punggung,
                'tinggi_badan': player_perform.player.tinggi_badan,
                'berat_badan': player_perform.player.berat_badan,
                'tanggal_gabung': player_perform.player.tanggal_gabung,
                'kelamin': player_perform.player.kelamin,
                'foto_profil': player_perform.player.foto_profil.url if player_perform.player.foto_profil else None
            },
            'kick_test': player_perform.kick_test,
            'tactical': player_perform.tactical,
            'shoot_focus': player_perform.shoot_focus,
            'analyst': player_perform.analyst,
            'shoot': player_perform.shoot
        }

    @staticmethod
    def post(req):
        Player = get_object_or_404(player, player=req['player'])

        new_player_perform = PlayerPerform.objects.create(
            playerperform=req['playerperform'],
            player=Player,
            kick_test=req['kick_test'],
            tactical=req['tactical'],
            shoot_focus=req['shoot_focus'],
            analyst=req['analyst'],
            shoot=req['shoot']  # Tambahkan field shoot
        )
        return {
            'playerperform': new_player_perform.playerperform,
            'player': {
                'id': Player.player,
                'nama': Player.nama,
                'posisi': Player.posisi,
                'usia': Player.usia,
                'kewarganegaraan': Player.kewarganegaraan,
                'team': {
                    'id': Player.tim.team,
                    'nama_team': Player.tim.nama_team,
                    'kategori_team': Player.tim.kategori_team,
                    'logo_team': Player.tim.logo_team.url if Player.tim.logo_team else None
                },
                'nomor_punggung': Player.nomor_punggung,
                'tinggi_badan': Player.tinggi_badan,
                'berat_badan': Player.berat_badan,
                'tanggal_gabung': Player.tanggal_gabung,
                'kelamin': Player.kelamin,
                'foto_profil': Player.foto_profil.url if Player.foto_profil else None
            },
            'kick_test': new_player_perform.kick_test,
            'tactical': new_player_perform.tactical,
            'shoot_focus': new_player_perform.shoot_focus,
            'analyst': new_player_perform.analyst,
            'shoot': new_player_perform.shoot
        }
    
    @staticmethod
    def get(player_perform_id):
        player_perform_data = get_object_or_404(PlayerPerform, playerperform=player_perform_id)
        return {
            'playerperform': player_perform_data.playerperform,
            'player': {
                'id': player_perform_data.player.player,
                'nama': player_perform_data.player.nama,
                'posisi': player_perform_data.player.posisi,
                'usia': player_perform_data.player.usia,
                'kewarganegaraan': player_perform_data.player.kewarganegaraan,
                'team': {
                    'id': player_perform_data.player.tim.team,
                    'nama_team': player_perform_data.player.tim.nama_team,
                    'kategori_team': player_perform_data.player.tim.kategori_team,
                    'logo_team': player_perform_data.player.tim.logo_team.url if player_perform_data.player.tim.logo_team else None
                },
                'nomor_punggung': player_perform_data.player.nomor_punggung,
                'tinggi_badan': player_perform_data.player.tinggi_badan,
                'berat_badan': player_perform_data.player.berat_badan,
                'tanggal_gabung': player_perform_data.player.tanggal_gabung,
                'kelamin': player_perform_data.player.kelamin,
                'foto_profil': player_perform_data.player.foto_profil.url if player_perform_data.player.foto_profil else None
            },
            'kick_test': player_perform_data.kick_test,
            'tactical': player_perform_data.tactical,
            'shoot_focus': player_perform_data.shoot_focus,
            'analyst': player_perform_data.analyst,
            'shoot': player_perform_data.shoot
        }
    
    @staticmethod
    def get_all():
        player_performs = PlayerPerform.objects.all()
        return [{
            'playerperform': perform.playerperform,
            'player': {
                'id': perform.player.player,
                'nama': perform.player.nama,
                'posisi': perform.player.posisi,
                'usia': perform.player.usia,
                'kewarganegaraan': perform.player.kewarganegaraan,
                'team': {
                    'id': perform.player.tim.team,
                    'nama_team': perform.player.tim.nama_team,
                    'kategori_team': perform.player.tim.kategori_team,
                    'logo_team': perform.player.tim.logo_team.url if perform.player.tim.logo_team else None
                },
                'nomor_punggung': perform.player.nomor_punggung,
                'tinggi_badan': perform.player.tinggi_badan,
                'berat_badan': perform.player.berat_badan,
                'tanggal_gabung': perform.player.tanggal_gabung,
                'kelamin': perform.player.kelamin,
                'foto_profil': perform.player.foto_profil.url if perform.player.foto_profil else None
            },
            'kick_test': perform.kick_test,
            'tactical': perform.tactical,
            'shoot_focus': perform.shoot_focus,
            'analyst': perform.analyst,
            'shoot': perform.shoot
        } for perform in player_performs]

    @staticmethod
    def put(req):
        PlayerPerformData = get_object_or_404(PlayerPerform, playerperform=req['playerperform'])
        Player = get_object_or_404(player, player=req['player'])

        PlayerPerformData.player = Player
        PlayerPerformData.kick_test = req.get('kick_test', PlayerPerformData.kick_test)
        PlayerPerformData.tactical = req.get('tactical', PlayerPerformData.tactical)
        PlayerPerformData.shoot_focus = req.get('shoot_focus', PlayerPerformData.shoot_focus)
        PlayerPerformData.analyst = req.get('analyst', PlayerPerformData.analyst)
        PlayerPerformData.shoot = req.get('shoot', PlayerPerformData.shoot)
        PlayerPerformData.save()

        return {
            'playerperform': PlayerPerformData.playerperform,
            'player': {
                'id': Player.player,
                'nama': Player.nama,
                'posisi': Player.posisi,
                'usia': Player.usia,
                'kewarganegaraan': Player.kewarganegaraan,
                'team': {
                    'id': Player.tim.team,
                    'nama_team': Player.tim.nama_team,
                    'kategori_team': Player.tim.kategori_team,
                    'logo_team': Player.tim.logo_team.url if Player.tim.logo_team else None
                },
                'nomor_punggung': Player.nomor_punggung,
                'tinggi_badan': Player.tinggi_badan,
                'berat_badan': Player.berat_badan,
                'tanggal_gabung': Player.tanggal_gabung,
                'kelamin': Player.kelamin,
                'foto_profil': Player.foto_profil.url if Player.foto_profil else None
            },
            'kick_test': PlayerPerformData.kick_test,
            'tactical': PlayerPerformData.tactical,
            'shoot_focus': PlayerPerformData.shoot_focus,
            'analyst': PlayerPerformData.analyst,
            'shoot': PlayerPerformData.shoot
        }
    
    @staticmethod
    def delete(req):
        PlayerPerformData = get_object_or_404(PlayerPerform, playerperform=req['playerperform'])
        PlayerPerformData.delete()
        return {'message': f"PlayerPerform with id {req['playerperform']} has been deleted."}