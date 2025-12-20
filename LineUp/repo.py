from django.shortcuts import get_object_or_404
from .models import LineUp
from player.models import player
from pertandingan.models import pertandingan

class RepoLineUp:
    @staticmethod
    def post(req):
        Player = get_object_or_404(player, player=req['player_id'])
        Match = get_object_or_404(pertandingan, match=req['match_id']) if req.get('match_id') else None
        new_lineup = LineUp.objects.create(
            id_lineup=req['id_lineup'],
            match=Match,
            player=Player,
            index=req['index'],
            status=req['status']
        )
        return {
            'id_lineup': new_lineup.id_lineup,
            'match': {
                'match_id': new_lineup.match.match,
                'nama_pertandingan': new_lineup.match.nama_pertandingan
            } if new_lineup.match else None,
            'player': {
                'player_id': Player.player,
                'nama': Player.nama,
                'posisi': Player.posisi,
                'nomor_punggung': Player.nomor_punggung,
                'foto_profil': Player.foto_profil.url if Player.foto_profil else None
            },
            'index': new_lineup.index,
            'status': new_lineup.status
        }

    @staticmethod
    def get(lineup_id):
        lineup = get_object_or_404(LineUp, id_lineup=lineup_id)
        return {
            'id_lineup': lineup.id_lineup,
            'match': {
                'match_id': lineup.match.match,
                'nama_pertandingan': lineup.match.nama_pertandingan
            } if lineup.match else None,
            'player': {
                'player_id': lineup.player.player,
                'nama': lineup.player.nama,
                'posisi': lineup.player.posisi,
                'nomor_punggung': lineup.player.nomor_punggung,
                'foto_profil': lineup.player.foto_profil.url if lineup.player.foto_profil else None
            },
            'index': lineup.index,
            'status': lineup.status
        }

    @staticmethod
    def get_all():
        lineups = LineUp.objects.all()
        return [{
            'id_lineup': lineup.id_lineup,
            'match': {
                'match_id': lineup.match.match,
                'nama_pertandingan': lineup.match.nama_pertandingan
            } if lineup.match else None,
            'player': {
                'player_id': lineup.player.player,
                'nama': lineup.player.nama,
                'posisi': lineup.player.posisi,
                'nomor_punggung': lineup.player.nomor_punggung,
                'foto_profil': lineup.player.foto_profil.url if lineup.player.foto_profil else None
            },
            'index': lineup.index,
            'status': lineup.status
        } for lineup in lineups]

    @staticmethod
    def put(req):
        lineup = get_object_or_404(LineUp, id_lineup=req['id_lineup'])
        Player = get_object_or_404(player, player=req['player_id'])
        Match = get_object_or_404(pertandingan, match=req['match_id']) if req.get('match_id') else None
        lineup.match = Match
        lineup.player = Player
        lineup.index = req['index']
        lineup.status = req['status']
        lineup.save()
        return {
            'id_lineup': lineup.id_lineup,
            'match': {
                'match_id': lineup.match.match,
                'nama_pertandingan': lineup.match.nama_pertandingan
            } if lineup.match else None,
            'player': {
                'player_id': lineup.player.player,
                'nama': lineup.player.nama,
                'posisi': lineup.player.posisi,
                'nomor_punggung': lineup.player.nomor_punggung,
                'foto_profil': lineup.player.foto_profil.url if lineup.player.foto_profil else None
            },
            'index': lineup.index,
            'status': lineup.status
        }

    @staticmethod
    def delete(req):
        lineup = get_object_or_404(LineUp, id_lineup=req['id_lineup'])
        lineup.delete()
        return {'message': f"LineUp with id {req['id_lineup']} has been deleted."}