from django.shortcuts import get_object_or_404
from .models import trainingstats
from player.models import player
from training.models import training


class RepoTrainingStats:
    @staticmethod
    def post(req):
        Player = get_object_or_404(player, player=req["player"])
        Training = get_object_or_404(training, training=req["training"])

        new_stats = trainingstats.objects.create(
            stats=req["stats"],
            training=Training,
            player=Player,
            position_played=req["position_played"],
            minutes_played=req["minutes_played"],
            overall_rating=req["overall_rating"],
        )
        return {
            "stats": new_stats.stats,
            "training": {
                "training": new_stats.training.training,
                "nama_latihan": new_stats.training.nama_latihan,
                "team": {
                    "team": new_stats.training.tim.team,
                    "nama_team": new_stats.training.tim.nama_team,
                    "kategori_team": new_stats.training.tim.kategori_team,
                    "logo_team": (
                        new_stats.training.tim.logo_team.url
                        if new_stats.training.tim.logo_team
                        else None
                    ),
                },
                "schedule": {
                    "schedule": new_stats.training.jadwal.schedule,
                    "tanggal": new_stats.training.jadwal.tanggal,
                    "start_time": new_stats.training.jadwal.start_time,
                    "end_time": new_stats.training.jadwal.end_time,
                },
                "stadion": {
                    "stadion": new_stats.training.lokasi.stadion,
                    "nama_stadion": new_stats.training.lokasi.nama_stadion,
                    "lokasi": new_stats.training.lokasi.lokasi,
                },
                "trainingcategory": {
                    "trainingcategory": new_stats.training.kategori.trainingcategory,
                    "nama_category": new_stats.training.kategori.nama_category,
                },
                "deskripsi": new_stats.training.deskripsi,
            },
            "player": {
                "player": Player.player,
                "nama": Player.nama,
                "posisi": Player.posisi,
                "usia": Player.usia,
                # 'kewarganegaraan': Player.kewarganegaraan,
                "team": {
                    "team": Player.tim.team if Player.tim else None,
                    "nama_team": Player.tim.nama_team if Player.tim else None,
                    "kategori_team": Player.tim.kategori_team if Player.tim else None,
                    "logo_team": (
                        Player.tim.logo_team.url
                        if Player.tim and Player.tim.logo_team
                        else None
                    ),
                },
                "nomor_punggung": Player.nomor_punggung,
                "tinggi_badan": Player.tinggi_badan,
                "berat_badan": Player.berat_badan,
                "tanggal_gabung": Player.tanggal_gabung,
                "kelamin": Player.kelamin,
                "foto_profil": Player.foto_profil.url if Player.foto_profil else None,
            },
            "position_played": new_stats.position_played,
            "minutes_played": new_stats.minutes_played,
            "overall_rating": new_stats.overall_rating,
        }

    @staticmethod
    def get(stats_id):
        stats_data = get_object_or_404(trainingstats, stats=stats_id)
        return {
            "stats": stats_data.stats,
            "training": {
                "training": stats_data.training.training,
                "nama_latihan": stats_data.training.nama_latihan,
                "team": {
                    "team": stats_data.training.tim.team,
                    "nama_team": stats_data.training.tim.nama_team,
                    "kategori_team": stats_data.training.tim.kategori_team,
                    "logo_team": (
                        stats_data.training.tim.logo_team.url
                        if stats_data.training.tim.logo_team
                        else None
                    ),
                },
                "schedule": {
                    "schedule": stats_data.training.jadwal.schedule,
                    "tanggal": stats_data.training.jadwal.tanggal,
                    "start_time": stats_data.training.jadwal.start_time,
                    "end_time": stats_data.training.jadwal.end_time,
                },
                "stadion": {
                    "stadion": stats_data.training.lokasi.stadion,
                    "nama_stadion": stats_data.training.lokasi.nama_stadion,
                    "lokasi": stats_data.training.lokasi.lokasi,
                },
                "trainingcategory": {
                    "trainingcategory": stats_data.training.kategori.trainingcategory,
                    "nama_category": stats_data.training.kategori.nama_category,
                },
                "deskripsi": stats_data.training.deskripsi,
            },
            "player": {
                "player": stats_data.player.player,
                "nama": stats_data.player.nama,
                "posisi": stats_data.player.posisi,
                "usia": stats_data.player.usia,
                # 'kewarganegaraan': stats_data.player.kewarganegaraan,
                "team": {
                    "team": (
                        stats_data.player.tim.team if stats_data.player.tim else None
                    ),
                    "nama_team": (
                        stats_data.player.tim.nama_team
                        if stats_data.player.tim
                        else None
                    ),
                    "kategori_team": (
                        stats_data.player.tim.kategori_team
                        if stats_data.player.tim
                        else None
                    ),
                    "logo_team": (
                        stats_data.player.tim.logo_team.url
                        if stats_data.player.tim and stats_data.player.tim.logo_team
                        else None
                    ),
                },
                "nomor_punggung": stats_data.player.nomor_punggung,
                "tinggi_badan": stats_data.player.tinggi_badan,
                "berat_badan": stats_data.player.berat_badan,
                "tanggal_gabung": stats_data.player.tanggal_gabung,
                "kelamin": stats_data.player.kelamin,
                "foto_profil": (
                    stats_data.player.foto_profil.url
                    if stats_data.player.foto_profil
                    else None
                ),
            },
            "position_played": stats_data.position_played,
            "minutes_played": stats_data.minutes_played,
            "overall_rating": stats_data.overall_rating,
        }

    @staticmethod
    def get_all():
        stats_list = trainingstats.objects.all()
        result = []

        for stats_data in stats_list:
            try:
                result.append(
                    {
                        "stats": stats_data.stats,
                        "training": {
                            "training": stats_data.training.training,
                            "nama_latihan": stats_data.training.nama_latihan,
                            "team": {
                                "team": stats_data.training.tim.team,
                                "nama_team": stats_data.training.tim.nama_team,
                                "kategori_team": stats_data.training.tim.kategori_team,
                                "logo_team": (
                                    stats_data.training.tim.logo_team.url
                                    if stats_data.training.tim.logo_team
                                    else None
                                ),
                            },
                            "schedule": {
                                "schedule": stats_data.training.jadwal.schedule,
                                "tanggal": stats_data.training.jadwal.tanggal,
                                "start_time": stats_data.training.jadwal.start_time,
                                "end_time": stats_data.training.jadwal.end_time,
                            },
                            "stadion": {
                                "stadion": stats_data.training.lokasi.stadion,
                                "nama_stadion": stats_data.training.lokasi.nama_stadion,
                                "lokasi": stats_data.training.lokasi.lokasi,
                            },
                            "trainingcategory": {
                                "trainingcategory": stats_data.training.kategori.trainingcategory,
                                "nama_category": stats_data.training.kategori.nama_category,
                            },
                            "deskripsi": stats_data.training.deskripsi,
                        },
                        "player": {
                            "player": stats_data.player.player,
                            "nama": stats_data.player.nama,
                            "posisi": stats_data.player.posisi,
                            "usia": stats_data.player.usia,
                            # 'kewarganegaraan': stats_data.player.kewarganegaraan,
                            "team": {
                                "team": (
                                    stats_data.player.tim.team
                                    if stats_data.player.tim
                                    else None
                                ),
                                "nama_team": (
                                    stats_data.player.tim.nama_team
                                    if stats_data.player.tim
                                    else None
                                ),
                                "kategori_team": (
                                    stats_data.player.tim.kategori_team
                                    if stats_data.player.tim
                                    else None
                                ),
                                "logo_team": (
                                    stats_data.player.tim.logo_team.url
                                    if stats_data.player.tim
                                    and stats_data.player.tim.logo_team
                                    else None
                                ),
                            },
                            "nomor_punggung": stats_data.player.nomor_punggung,
                            "tinggi_badan": stats_data.player.tinggi_badan,
                            "berat_badan": stats_data.player.berat_badan,
                            "tanggal_gabung": stats_data.player.tanggal_gabung,
                            "kelamin": stats_data.player.kelamin,
                            "foto_profil": (
                                stats_data.player.foto_profil.url
                                if stats_data.player.foto_profil
                                else None
                            ),
                        },
                        "position_played": stats_data.position_played,
                        "minutes_played": stats_data.minutes_played,
                        "overall_rating": stats_data.overall_rating,
                    }
                )
            except Exception as e:
                print(f"Error processing training stats {stats_data.stats}: {str(e)}")
                continue
        return result

    @staticmethod
    def get_by_player(player_id):
        Player = get_object_or_404(player, player=player_id)
        stats_list = trainingstats.objects.filter(player=Player)
        result = []

        for stats_data in stats_list:
            try:
                result.append(
                    {
                        "stats": stats_data.stats,
                        "training": {
                            "training": stats_data.training.training,
                            "nama_latihan": stats_data.training.nama_latihan,
                            "team": {
                                "team": stats_data.training.tim.team,
                                "nama_team": stats_data.training.tim.nama_team,
                                "kategori_team": stats_data.training.tim.kategori_team,
                                "logo_team": (
                                    stats_data.training.tim.logo_team.url
                                    if stats_data.training.tim.logo_team
                                    else None
                                ),
                            },
                            "schedule": {
                                "schedule": stats_data.training.jadwal.schedule,
                                "tanggal": stats_data.training.jadwal.tanggal,
                                "start_time": stats_data.training.jadwal.start_time,
                                "end_time": stats_data.training.jadwal.end_time,
                            },
                            "stadion": {
                                "stadion": stats_data.training.lokasi.stadion,
                                "nama_stadion": stats_data.training.lokasi.nama_stadion,
                                "lokasi": stats_data.training.lokasi.lokasi,
                            },
                            "trainingcategory": {
                                "trainingcategory": stats_data.training.kategori.trainingcategory,
                                "nama_category": stats_data.training.kategori.nama_category,
                            },
                            "deskripsi": stats_data.training.deskripsi,
                        },
                        "player": {
                            "player": stats_data.player.player,
                            "nama": stats_data.player.nama,
                            "posisi": stats_data.player.posisi,
                            "usia": stats_data.player.usia,
                            # 'kewarganegaraan': stats_data.player.kewarganegaraan,
                            "team": {
                                "team": (
                                    stats_data.player.tim.team
                                    if stats_data.player.tim
                                    else None
                                ),
                                "nama_team": (
                                    stats_data.player.tim.nama_team
                                    if stats_data.player.tim
                                    else None
                                ),
                                "kategori_team": (
                                    stats_data.player.tim.kategori_team
                                    if stats_data.player.tim
                                    else None
                                ),
                                "logo_team": (
                                    stats_data.player.tim.logo_team.url
                                    if stats_data.player.tim
                                    and stats_data.player.tim.logo_team
                                    else None
                                ),
                            },
                            "nomor_punggung": stats_data.player.nomor_punggung,
                            "tinggi_badan": stats_data.player.tinggi_badan,
                            "berat_badan": stats_data.player.berat_badan,
                            "tanggal_gabung": stats_data.player.tanggal_gabung,
                            "kelamin": stats_data.player.kelamin,
                            "foto_profil": (
                                stats_data.player.foto_profil.url
                                if stats_data.player.foto_profil
                                else None
                            ),
                        },
                        "position_played": stats_data.position_played,
                        "minutes_played": stats_data.minutes_played,
                        "overall_rating": stats_data.overall_rating,
                    }
                )
            except Exception as e:
                print(f"Error processing training stats {stats_data.stats}: {str(e)}")
                continue
        return result

    @staticmethod
    def put(req):
        StatsData = get_object_or_404(trainingstats, stats=req["stats"])
        Player = get_object_or_404(player, player=req["player"])
        Training = get_object_or_404(training, training=req["training"])

        StatsData.training = Training
        StatsData.player = Player
        StatsData.position_played = req.get(
            "position_played", StatsData.position_played
        )
        StatsData.minutes_played = req.get("minutes_played", StatsData.minutes_played)
        StatsData.overall_rating = req.get("overall_rating", StatsData.overall_rating)
        StatsData.save()

        return {
            "stats": StatsData.stats,
            "training": {
                "training": StatsData.training.training,
                "nama_latihan": StatsData.training.nama_latihan,
                "team": {
                    "team": StatsData.training.tim.team,
                    "nama_team": StatsData.training.tim.nama_team,
                    "kategori_team": StatsData.training.tim.kategori_team,
                    "logo_team": (
                        StatsData.training.tim.logo_team.url
                        if StatsData.training.tim.logo_team
                        else None
                    ),
                },
                "schedule": {
                    "schedule": StatsData.training.jadwal.schedule,
                    "tanggal": StatsData.training.jadwal.tanggal,
                    "start_time": StatsData.training.jadwal.start_time,
                    "end_time": StatsData.training.jadwal.end_time,
                },
                "stadion": {
                    "stadion": StatsData.training.lokasi.stadion,
                    "nama_stadion": StatsData.training.lokasi.nama_stadion,
                    "lokasi": StatsData.training.lokasi.lokasi,
                },
                "trainingcategory": {
                    "trainingcategory": StatsData.training.kategori.trainingcategory,
                    "nama_category": StatsData.training.kategori.nama_category,
                },
                "deskripsi": StatsData.training.deskripsi,
            },
            "player": {
                "player": Player.player,
                "nama": Player.nama,
                "posisi": Player.posisi,
                "usia": Player.usia,
                # 'kewarganegaraan': Player.kewarganegaraan,
                "team": {
                    "team": Player.tim.team if Player.tim else None,
                    "nama_team": Player.tim.nama_team if Player.tim else None,
                    "kategori_team": Player.tim.kategori_team if Player.tim else None,
                    "logo_team": (
                        Player.tim.logo_team.url
                        if Player.tim and Player.tim.logo_team
                        else None
                    ),
                },
                "nomor_punggung": Player.nomor_punggung,
                "tinggi_badan": Player.tinggi_badan,
                "berat_badan": Player.berat_badan,
                "tanggal_gabung": Player.tanggal_gabung,
                "kelamin": Player.kelamin,
                "foto_profil": Player.foto_profil.url if Player.foto_profil else None,
            },
            "position_played": StatsData.position_played,
            "minutes_played": StatsData.minutes_played,
            "overall_rating": StatsData.overall_rating,
        }

    @staticmethod
    def delete(req):
        StatsData = get_object_or_404(trainingstats, stats=req["stats"])
        StatsData.delete()
        return {"message": f"Training stats with id {req['stats']} has been deleted."}
