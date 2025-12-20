# repository/player_search_repository.py
from django.shortcuts import get_object_or_404
from .models import PlayerSearch
from user.models import user

class RepoPlayerSearch:
    @staticmethod
    def post(req):
        NamaPlayer = get_object_or_404(user, id_user=req['nama_player'])

        new_player_search = PlayerSearch.objects.create(
            id=req['id'],
            nama_player=NamaPlayer,
            kata_kunci=req['kata_kunci']
        )
        return {
            'id': new_player_search.id,
            'nama_player': {
                'id': NamaPlayer.id_user,
                'nama': NamaPlayer.nama,
                'email': NamaPlayer.email
            },
            'kata_kunci': new_player_search.kata_kunci
        }
    
    @staticmethod
    def get(player_search_id):
        player_search_data = get_object_or_404(PlayerSearch, id=player_search_id)
        return {
            'id': player_search_data.id,
            'nama_player': {
                'id': player_search_data.nama_player.id,
                'nama': player_search_data.nama_player.nama,
                'email': player_search_data.nama_player.email
            },
            'kata_kunci': player_search_data.kata_kunci
        }
    
    @staticmethod
    def get_all():
        player_searches = PlayerSearch.objects.all()
        return [{
            'id': search.id,
            'nama_player': {
                'id': search.nama_player.id_user,
                'nama': search.nama_player.nama,
                'email': search.nama_player.email
            },
            'kata_kunci': search.kata_kunci
        } for search in player_searches]

    @staticmethod
    def put(req):
        PlayerSearchData = get_object_or_404(PlayerSearch, id=req['id'])
        NamaPlayer = get_object_or_404(user, id_user=req['nama_player'])

        PlayerSearchData.nama_player = NamaPlayer
        PlayerSearchData.kata_kunci = req.get('kata_kunci', PlayerSearchData.kata_kunci)
        PlayerSearchData.save()

        return {
            'id': PlayerSearchData.id,
            'nama_player': {
                'id': NamaPlayer.id_user,
                'nama': NamaPlayer.nama,
                'email': NamaPlayer.email
            },
            'kata_kunci': PlayerSearchData.kata_kunci
        }
    
    @staticmethod
    def delete(req):
        PlayerSearchData = get_object_or_404(PlayerSearch, id=req['id'])
        PlayerSearchData.delete()
        return {'message': f"PlayerSearch with id {req['id']} has been deleted."}