from django.shortcuts import get_object_or_404
from .models import stadion

class RepoStadion:
    @staticmethod
    def post(req):
        new_stadion = stadion.objects.create(
            stadion= req['stadion'], 
            nama_stadion= req['nama_stadion'],
            lokasi= req['lokasi'] 
        )
        return {
            'stadion': new_stadion.stadion,
            'nama_stadion': new_stadion.nama_stadion,
            'lokasi': new_stadion.lokasi
        }
    
    @staticmethod
    def get(stadion_id):
        stadion_update = get_object_or_404(stadion, stadion=stadion_id)
        
        return {
            'stadion': stadion_update.stadion,
            'nama_stadion': stadion_update.nama_stadion,
            'lokasi': stadion_update.lokasi
        }
    
    @staticmethod
    def get_all():
        stadiums = stadion.objects.all()
        return [{
            'stadion': stadion_data.stadion,
            'nama_stadion': stadion_data.nama_stadion,
            'lokasi': stadion_data.lokasi
        } for stadion_data in stadiums]
    

    def put(req):
        Stadion = get_object_or_404(stadion, stadion=req['stadion'])
        Stadion.nama_stadion = req.get('nama_stadion', stadion.nama_stadion)
        Stadion.lokasi = req.get('lokasi', stadion.lokasi)
        Stadion.save()
        return{
            'stadion': Stadion.stadion,
            'nama_stadion': Stadion.nama_stadion,
            'lokasi' : Stadion.lokasi
        }
    
    def delete(req):
        Stadion = get_object_or_404(stadion, stadion=req['stadion'])
        Stadion.delete()
        return {'message': f"User with id {req['stadion']} has been deleted."}