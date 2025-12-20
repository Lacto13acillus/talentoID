from django.shortcuts import get_object_or_404
from .models import DeviceStats
from player.models import player

class RepoDeviceStats:
    @staticmethod
    def post(req):
        Pemain = get_object_or_404(player, player=req['player'])

        new_stats = DeviceStats.objects.create(
            devicestats=req['devicestats'],
            pemain=Pemain,
            jenis_perangkat=req['jenis_perangkat'],
            metric=req['metric'],
            value=req['value'],
            unit=req['unit']
        )
        return {
            'devicestats': new_stats.devicestats,
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
            'jenis_perangkat': new_stats.jenis_perangkat,
            'metric': new_stats.metric,
            'value': new_stats.value,
            'unit': new_stats.unit,
            'created_at': new_stats.created_at,
            'updated_at': new_stats.updated_at
        }
    
    @staticmethod
    def get(devicestats_id):
        stats_data = get_object_or_404(DeviceStats, devicestats=devicestats_id)
        Pemain = stats_data.pemain

        return {
            'devicestats': stats_data.devicestats,
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
            'jenis_perangkat': stats_data.jenis_perangkat,
            'metric': stats_data.metric,
            'value': stats_data.value,
            'unit': stats_data.unit,
            'created_at': stats_data.created_at,
            'updated_at': stats_data.updated_at
        }
    
    @staticmethod
    def get_all():
        stats_list = DeviceStats.objects.all()
        result = []
        
        for stats_data in stats_list:
            Pemain = stats_data.pemain
            result.append({
                'devicestats': stats_data.devicestats,
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
                'jenis_perangkat': stats_data.jenis_perangkat,
                'metric': stats_data.metric,
                'value': stats_data.value,
                'unit': stats_data.unit,
                'created_at': stats_data.created_at,
                'updated_at': stats_data.updated_at
            })
        
        return result


    @staticmethod
    def put(req):
        StatsData = get_object_or_404(DeviceStats, devicestats=req['devicestats'])
        Pemain = get_object_or_404(player, player=req['player'])

        StatsData.jenis_perangkat = req.get('jenis_perangkat', StatsData.jenis_perangkat)
        StatsData.metric = req.get('metric', StatsData.metric)
        StatsData.value = req.get('value', StatsData.value)
        StatsData.unit = req.get('unit', StatsData.unit)
        StatsData.pemain = Pemain
        StatsData.save()

        return {
            'devicestats': StatsData.devicestats,
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
            'jenis_perangkat': StatsData.jenis_perangkat,
            'metric': StatsData.metric,
            'value': StatsData.value,
            'unit': StatsData.unit,
            'created_at': StatsData.created_at,
            'updated_at': StatsData.updated_at
        }
    
    @staticmethod
    def delete(req):
        StatsData = get_object_or_404(DeviceStats, devicestats=req['devicestats'])
        StatsData.delete()
        return {'message': f"DeviceStats with id {req['devicestats']} has been deleted."}