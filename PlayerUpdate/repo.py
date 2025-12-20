from django.shortcuts import get_object_or_404
from .models import PlayerUpdate
from player.models import player

class RepoPlayerUpdate:
    @staticmethod
    def post(req):
        Pemain = get_object_or_404(player, player=req['player'])

        new_update = PlayerUpdate.objects.create(
            playerupdate=req['playerupdate'],
            pemain=Pemain,
            judul_update=req['judul_update'],
            deskripsi=req['deskripsi']
        )
        return {
            'playerupdate': new_update.playerupdate,
            'player': {
                'player': Pemain.player,
                'nama': Pemain.nama,
                'posisi': Pemain.posisi,
                'usia': Pemain.usia,
                'kewarganegaraan': Pemain.kewarganegaraan,
                'team': {
                    'team': Pemain.tim.team,
                    'nama_team': Pemain.tim.nama_team,
                    'kategori_team': Pemain.tim.kategori_team,
                    'logo_team': Pemain.tim.logo_team.url if Pemain.tim.logo_team else None
                },
                'nomor_punggung': Pemain.nomor_punggung,
                'tinggi_badan': Pemain.tinggi_badan,
                'berat_badan': Pemain.berat_badan,
                'tanggal_gabung': Pemain.tanggal_gabung,
                'kelamin': Pemain.kelamin,
                'foto_profil': Pemain.foto_profil.url if Pemain.foto_profil else None
            },
            'judul_update': new_update.judul_update,
            'deskripsi': new_update.deskripsi,
            'created_at': new_update.created_at,
            'updated_at': new_update.updated_at
        }
    
    @staticmethod
    def get(playerupdate_id):
        update_data = get_object_or_404(PlayerUpdate, playerupdate=playerupdate_id)
        Pemain = update_data.pemain

        return {
            'playerupdate': update_data.playerupdate,
            'player': {
                'player': Pemain.player,
                'nama': Pemain.nama,
                'posisi': Pemain.posisi,
                'usia': Pemain.usia,
                'kewarganegaraan': Pemain.kewarganegaraan,
                'team': {
                    'team': Pemain.tim.team,
                    'nama_team': Pemain.tim.nama_team,
                    'kategori_team': Pemain.tim.kategori_team,
                    'logo_team': Pemain.tim.logo_team.url if Pemain.tim.logo_team else None
                },
                'nomor_punggung': Pemain.nomor_punggung,
                'tinggi_badan': Pemain.tinggi_badan,
                'berat_badan': Pemain.berat_badan,
                'tanggal_gabung': Pemain.tanggal_gabung,
                'kelamin': Pemain.kelamin,
                'foto_profil': Pemain.foto_profil.url if Pemain.foto_profil else None
            },
            'judul_update': update_data.judul_update,
            'deskripsi': update_data.deskripsi,
            'created_at': update_data.created_at,
            'updated_at': update_data.updated_at
        }
    
    def get_all():
        update_list = PlayerUpdate.objects.all()
        result = []
        
        for update_data in update_list:
            Pemain = update_data.pemain
            result.append({
                'playerupdate': update_data.playerupdate,
                'player': {
                    'player': Pemain.player,
                    'nama': Pemain.nama,
                    'posisi': Pemain.posisi,
                    'usia': Pemain.usia,
                    'kewarganegaraan': Pemain.kewarganegaraan,
                    'team': {
                        'team': Pemain.tim.team,
                        'nama_team': Pemain.tim.nama_team,
                        'kategori_team': Pemain.tim.kategori_team,
                        'logo_team': Pemain.tim.logo_team.url if Pemain.tim.logo_team else None
                    },
                    'nomor_punggung': Pemain.nomor_punggung,
                    'tinggi_badan': Pemain.tinggi_badan,
                    'berat_badan': Pemain.berat_badan,
                    'tanggal_gabung': Pemain.tanggal_gabung,
                    'kelamin': Pemain.kelamin,
                    'foto_profil': Pemain.foto_profil.url if Pemain.foto_profil else None
                },
                'judul_update': update_data.judul_update,
                'deskripsi': update_data.deskripsi,
                'created_at': update_data.created_at,
                'updated_at': update_data.updated_at
            })
        
        return result

    @staticmethod
    def put(req):
        UpdateData = get_object_or_404(PlayerUpdate, playerupdate=req['playerupdate'])
        Pemain = get_object_or_404(player, player=req['player'])

        UpdateData.judul_update = req.get('judul_update', UpdateData.judul_update)
        UpdateData.deskripsi = req.get('deskripsi', UpdateData.deskripsi)
        UpdateData.pemain = Pemain
        UpdateData.save()

        return {
            'playerupdate': UpdateData.playerupdate,
            'player': {
                'player': Pemain.player,
                'nama': Pemain.nama,
                'posisi': Pemain.posisi,
                'usia': Pemain.usia,
                'kewarganegaraan': Pemain.kewarganegaraan,
                'team': {
                    'team': Pemain.tim.team,
                    'nama_team': Pemain.tim.nama_team,
                    'kategori_team': Pemain.tim.kategori_team,
                    'logo_team': Pemain.tim.logo_team.url if Pemain.tim.logo_team else None
                },
                'nomor_punggung': Pemain.nomor_punggung,
                'tinggi_badan': Pemain.tinggi_badan,
                'berat_badan': Pemain.berat_badan,
                'tanggal_gabung': Pemain.tanggal_gabung,
                'kelamin': Pemain.kelamin,
                'foto_profil': Pemain.foto_profil.url if Pemain.foto_profil else None
            },
            'judul_update': UpdateData.judul_update,
            'deskripsi': UpdateData.deskripsi,
            'created_at': UpdateData.created_at,
            'updated_at': UpdateData.updated_at
        }
    
    @staticmethod
    def delete(req):
        UpdateData = get_object_or_404(PlayerUpdate, playerupdate=req['playerupdate'])
        UpdateData.delete()
        return {'message': f"PlayerUpdate with id {req['playerupdate']} has been deleted."}