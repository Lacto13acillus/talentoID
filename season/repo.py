from django.shortcuts import get_object_or_404
from .models import season
from django.core.exceptions import ValidationError

class RepoSeason:
    @staticmethod
    def post(req):
        new_season = season.objects.create(
            season=req['season'],
            nama_season=req['nama_season']
        )
        return {
            'season': new_season.season,
            'nama_season': new_season.nama_season
        }
    
    @staticmethod
    def get(season_id):
        season_data = get_object_or_404(season, season=season_id)
        return {
            'season': season_data.season,
            'nama_season': season_data.nama_season
        }
    
    @staticmethod
    def get_all():
        seasons = season.objects.all()
        result = []
        for season_data in seasons:
            try:
                result.append({
                    'season': season_data.season,
                    'nama_season': season_data.nama_season
                })
            except Exception as e:
                print(f"Error processing season {season_data.season}: {str(e)}")
                continue
        return result
    
    @staticmethod
    def put(req):
        season_data = get_object_or_404(season, season=req['season'])
        
        season_data.nama_season = req.get('nama_season', season_data.nama_season)
        season_data.save()

        return {
            'season': season_data.season,
            'nama_season': season_data.nama_season
        }
    
    @staticmethod
    def delete(req):
        season_data = get_object_or_404(season, season=req['season'])
        season_data.delete()
        return {'message': f"Season with id {req['season']} has been deleted."}