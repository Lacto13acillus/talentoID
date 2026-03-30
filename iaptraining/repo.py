from django.shortcuts import get_object_or_404
from .models import iaptraining
from player.models import player
from training.models import training
from team.models import team
from stadion.models import stadion
from PlayerPerform.repo import RepoPlayerPerform
import uuid


class RepoIAPTraining:
    @staticmethod
    def _get_training_data(training_record):
        """Helper method to construct detailed training data."""
        Team = get_object_or_404(team, team=training_record.tim.team)
        Stadion = get_object_or_404(stadion, stadion=training_record.lokasi.stadion)
        Schedule = training_record.jadwal
        Frequency = training_record.frequency

        schedule_data = None
        if Schedule:
            schedule_data = {
                "schedule": Schedule.schedule,
                "tanggal": Schedule.tanggal,
                "start_time": (
                    Schedule.start_time.strftime("%H:%M")
                    if Schedule.start_time
                    else None
                ),
                "end_time": (
                    Schedule.end_time.strftime("%H:%M") if Schedule.end_time else None
                ),
            }

        frequency_data = None
        if Frequency:
            frequency_data = {
                "frequency": Frequency.frequency,
                "frequency_time": Frequency.get_frequency_time_display(),
            }

        categories_data = [
            {
                "trainingcategory": category.trainingcategory,
                "nama_category": category.nama_category,
            }
            for category in training_record.kategori.all()
        ]

        return {
            "training": training_record.training,
            "nama_latihan": training_record.nama_latihan,
            "team": {
                "team": Team.team,
                "nama_team": Team.nama_team,
                "kategori_team": Team.kategori_team,
                "logo_team": Team.logo_team.url if Team.logo_team else None,
            },
            "schedule": schedule_data,
            "stadion": {
                "stadion": Stadion.stadion,
                "nama_stadion": Stadion.nama_stadion,
                "lokasi": Stadion.lokasi,
            },
            "trainingcategory": categories_data,
            "frequency": frequency_data,
            "date": training_record.date.isoformat(),
            "start_time": training_record.start_time.strftime("%H:%M"),
            "end_time": training_record.end_time.strftime("%H:%M"),
            "deskripsi": training_record.deskripsi,
        }

    @staticmethod
    def post(req):
        Player = get_object_or_404(player, player=req["player"])
        Training = get_object_or_404(training, training=req["training"])
        group_id = uuid.uuid4()  # Virtual group ID for response
        entries = []

        # Process technical category
        for tech in req.get("technical", []):
            unique_iaptraining_id = uuid.uuid4()  # Unique UUID for each record
            new_iaptraining = iaptraining.objects.create(
                iaptraining=unique_iaptraining_id,
                player=Player,
                training=Training,
                category="Technical",
                type=tech["type"],
                current_achieve=tech["current_achieve"],
                target=tech["target"],
            )
            entries.append(
                {
                    "iaptraining": new_iaptraining.iaptraining,
                    "category": new_iaptraining.category,
                    "type": new_iaptraining.type,
                    "current_achieve": new_iaptraining.current_achieve,
                    "target": new_iaptraining.target,
                }
            )

        # Process physical category
        for phys in req.get("physical", []):
            unique_iaptraining_id = uuid.uuid4()
            new_iaptraining = iaptraining.objects.create(
                iaptraining=unique_iaptraining_id,
                player=Player,
                training=Training,
                category="Physical",
                type=phys["type"],
                current_achieve=phys["current_achieve"],
                target=phys["target"],
            )
            entries.append(
                {
                    "iaptraining": new_iaptraining.iaptraining,
                    "category": new_iaptraining.category,
                    "type": new_iaptraining.type,
                    "current_achieve": new_iaptraining.current_achieve,
                    "target": new_iaptraining.target,
                }
            )

        # Process goalkeeper category
        for gk in req.get("goalkeeper", []):
            unique_iaptraining_id = uuid.uuid4()
            new_iaptraining = iaptraining.objects.create(
                iaptraining=unique_iaptraining_id,
                player=Player,
                training=Training,
                category="Goalkeeper",
                type=gk["type"],
                current_achieve=gk["current_achieve"],
                target=gk["target"],
            )
            entries.append(
                {
                    "iaptraining": new_iaptraining.iaptraining,
                    "category": new_iaptraining.category,
                    "type": new_iaptraining.type,
                    "current_achieve": new_iaptraining.current_achieve,
                    "target": new_iaptraining.target,
                }
            )

        # Process social category
        for soc in req.get("social", []):
            unique_iaptraining_id = uuid.uuid4()
            new_iaptraining = iaptraining.objects.create(
                iaptraining=unique_iaptraining_id,
                player=Player,
                training=Training,
                category="Social",
                type=soc["type"],
                current_achieve=soc["current_achieve"],
                target=soc["target"],
            )
            entries.append(
                {
                    "iaptraining": new_iaptraining.iaptraining,
                    "category": new_iaptraining.category,
                    "type": new_iaptraining.type,
                    "current_achieve": new_iaptraining.current_achieve,
                    "target": new_iaptraining.target,
                }
            )

        # Update PlayerPerform
        RepoPlayerPerform.calculate_and_update_performance(Player.player)

        return {
            "iaptraining": group_id,
            "player": {
                "player": Player.player,
                "nama": Player.nama,
                "posisi": Player.posisi,
                "team": {
                    "team": Player.tim.team,
                    "nama_team": Player.tim.nama_team,
                    "kategori_team": Player.tim.kategori_team,
                    "logo_team": (
                        Player.tim.logo_team.url if Player.tim.logo_team else None
                    ),
                },
                "nomor_punggung": Player.nomor_punggung,
                "tinggi_badan": Player.tinggi_badan,
                "berat_badan": Player.berat_badan,
                "tanggal_gabung": Player.tanggal_gabung,
                "kelamin": Player.kelamin,
                "foto_profil": Player.foto_profil.url if Player.foto_profil else None,
            },
            "training": RepoIAPTraining._get_training_data(Training),
            "entries": entries,
        }

    @staticmethod
    def get(iaptraining_id):
        iaptraining_record = get_object_or_404(iaptraining, iaptraining=iaptraining_id)
        entries = [
            {
                "category": iaptraining_record.category,
                "type": iaptraining_record.type,
                "current_achieve": iaptraining_record.current_achieve,
                "target": iaptraining_record.target,
            }
        ]

        return {
            "iaptraining": iaptraining_id,
            "player": {
                "player": iaptraining_record.player.player,
                "nama": iaptraining_record.player.nama,
                "posisi": iaptraining_record.player.posisi,
                "team": {
                    "team": iaptraining_record.player.tim.team,
                    "nama_team": iaptraining_record.player.tim.nama_team,
                    "kategori_team": iaptraining_record.player.tim.kategori_team,
                    "logo_team": (
                        iaptraining_record.player.tim.logo_team.url
                        if iaptraining_record.player.tim.logo_team
                        else None
                    ),
                },
                "nomor_punggung": iaptraining_record.player.nomor_punggung,
                "tinggi_badan": iaptraining_record.player.tinggi_badan,
                "berat_badan": iaptraining_record.player.berat_badan,
                "tanggal_gabung": iaptraining_record.player.tanggal_gabung,
                "kelamin": iaptraining_record.player.kelamin,
                "foto_profil": (
                    iaptraining_record.player.foto_profil.url
                    if iaptraining_record.player.foto_profil
                    else None
                ),
            },
            "training": RepoIAPTraining._get_training_data(iaptraining_record.training),
            "entries": entries,
        }

    @staticmethod
    def get_all():
        players = player.objects.all()
        result = []

        for Player in players:
            iaptraining_records = iaptraining.objects.filter(player=Player)
            if iaptraining_records.exists():
                entries = [
                    {
                        "iaptraining": record.iaptraining,
                        "category": record.category,
                        "type": record.type,
                        "current_achieve": record.current_achieve,
                        "target": record.target,
                    }
                    for record in iaptraining_records
                ]
                # Use the first record to get the training details
                first_record = iaptraining_records.first()
                result.append(
                    {
                        "iaptraining": str(uuid.uuid4()),
                        "player": {
                            "player": Player.player,
                            "nama": Player.nama,
                            "posisi": Player.posisi,
                            "team": {
                                "team": Player.tim.team,
                                "nama_team": Player.tim.nama_team,
                                "kategori_team": Player.tim.kategori_team,
                                "logo_team": (
                                    Player.tim.logo_team.url
                                    if Player.tim.logo_team
                                    else None
                                ),
                            },
                            "nomor_punggung": Player.nomor_punggung,
                            "tinggi_badan": Player.tinggi_badan,
                            "berat_badan": Player.berat_badan,
                            "tanggal_gabung": Player.tanggal_gabung,
                            "kelamin": Player.kelamin,
                            "foto_profil": (
                                Player.foto_profil.url if Player.foto_profil else None
                            ),
                        },
                        "training": RepoIAPTraining._get_training_data(
                            first_record.training
                        ),
                        "entries": entries,
                    }
                )

        return result

    @staticmethod
    def get_by_player_and_training(player_id, training_id):
        Player = get_object_or_404(player, player=player_id)
        Training = get_object_or_404(training, training=training_id)
        iaptraining_records = iaptraining.objects.filter(
            player=Player, training=Training
        )

        if not iaptraining_records.exists():
            return {
                "iaptraining": str(uuid.uuid4()),
                "player": {
                    "player": Player.player,
                    "nama": Player.nama,
                    "posisi": Player.posisi,
                    "team": {
                        "team": Player.tim.team,
                        "nama_team": Player.tim.nama_team,
                        "kategori_team": Player.tim.kategori_team,
                        "logo_team": (
                            Player.tim.logo_team.url if Player.tim.logo_team else None
                        ),
                    },
                    "nomor_punggung": Player.nomor_punggung,
                    "tinggi_badan": Player.tinggi_badan,
                    "berat_badan": Player.berat_badan,
                    "tanggal_gabung": Player.tanggal_gabung,
                    "kelamin": Player.kelamin,
                    "foto_profil": (
                        Player.foto_profil.url if Player.foto_profil else None
                    ),
                },
                "training": RepoIAPTraining._get_training_data(Training),
                "entries": [],
            }

        entries = [
            {
                "iaptraining": record.iaptraining,
                "category": record.category,
                "type": record.type,
                "current_achieve": record.current_achieve,
                "target": record.target,
                "training": record.training.training,  # Include training ID for reference
            }
            for record in iaptraining_records
        ]

        return {
            "iaptraining": str(uuid.uuid4()),
            "player": {
                "player": Player.player,
                "nama": Player.nama,
                "posisi": Player.posisi,
                "team": {
                    "team": Player.tim.team,
                    "nama_team": Player.tim.nama_team,
                    "kategori_team": Player.tim.kategori_team,
                    "logo_team": (
                        Player.tim.logo_team.url if Player.tim.logo_team else None
                    ),
                },
                "nomor_punggung": Player.nomor_punggung,
                "tinggi_badan": Player.tinggi_badan,
                "berat_badan": Player.berat_badan,
                "tanggal_gabung": Player.tanggal_gabung,
                "kelamin": Player.kelamin,
                "foto_profil": Player.foto_profil.url if Player.foto_profil else None,
            },
            "training": RepoIAPTraining._get_training_data(Training),
            "entries": entries,
        }

    @staticmethod
    def put(req):
        iaptraining_record = get_object_or_404(
            iaptraining, iaptraining=req["iaptraining"]
        )
        Player = get_object_or_404(player, player=req["player"])
        Training = (
            get_object_or_404(training, training=req["training"])
            if req.get("training")
            else iaptraining_record.training
        )

        iaptraining_record.player = Player
        iaptraining_record.training = Training
        iaptraining_record.category = req.get("category", iaptraining_record.category)
        iaptraining_record.type = req.get("type", iaptraining_record.type)
        iaptraining_record.current_achieve = req.get(
            "current_achieve", iaptraining_record.current_achieve
        )
        iaptraining_record.target = req.get("target", iaptraining_record.target)
        iaptraining_record.save()

        RepoPlayerPerform.calculate_and_update_performance(Player.player)

        entries = [
            {
                "iaptraining": iaptraining_record.iaptraining,
                "category": iaptraining_record.category,
                "type": iaptraining_record.type,
                "current_achieve": iaptraining_record.current_achieve,
                "target": iaptraining_record.target,
            }
        ]

        return {
            "iaptraining": req["iaptraining"],
            "player": {
                "player": Player.player,
                "nama": Player.nama,
                "posisi": Player.posisi,
                "team": {
                    "team": Player.tim.team,
                    "nama_team": Player.tim.nama_team,
                    "kategori_team": Player.tim.kategori_team,
                    "logo_team": (
                        Player.tim.logo_team.url if Player.tim.logo_team else None
                    ),
                },
                "nomor_punggung": Player.nomor_punggung,
                "tinggi_badan": Player.tinggi_badan,
                "berat_badan": Player.berat_badan,
                "tanggal_gabung": Player.tanggal_gabung,
                "kelamin": Player.kelamin,
                "foto_profil": Player.foto_profil.url if Player.foto_profil else None,
            },
            "training": RepoIAPTraining._get_training_data(iaptraining_record.training),
            "entries": entries,
        }

    @staticmethod
    def delete(req):
        iaptraining_record = get_object_or_404(
            iaptraining, iaptraining=req["iaptraining"]
        )
        player_id = iaptraining_record.player.player
        iaptraining_record.delete()

        RepoPlayerPerform.calculate_and_update_performance(player_id)

        return {
            "message": f"IAPTraining with id {req['iaptraining']} has been deleted."
        }
