from django.shortcuts import get_object_or_404
from .models import trainingformation
from formations.models import Formation
from LineUp.models import LineUp

class RepoTrainingFormation:
    @staticmethod
    def post(req):
        formations = get_object_or_404(Formation, id_formasi=req['id_formations'])
        new_trainingformation = trainingformation.objects.create(
            id_trainingformation=req['id_trainingformation'],
            id_formations=formations
        )
        # Add multiple LineUp entries using the array of id_lineup
        lineup_ids = req['id_lineup']  # Expecting a list of lineup IDs
        for lineup_id in lineup_ids:
            Lineup = get_object_or_404(LineUp, id_lineup=lineup_id)
            new_trainingformation.id_lineup.add(Lineup)

        # Fetch the lineup entries for the response
        lineup_entries = new_trainingformation.id_lineup.all()
        lineup_data = [
            {
                'id_lineup': lineup.id_lineup,
                'player': {
                    'player': lineup.player.player,
                    'nama': lineup.player.nama,
                    'posisi': lineup.player.posisi,
                    'nomor_punggung': lineup.player.nomor_punggung,
                    'foto_profil': lineup.player.foto_profil.url if lineup.player.foto_profil else None
                },
                'index': lineup.index,
                'status': lineup.status
            } for lineup in lineup_entries
        ]

        return {
            'id_trainingformation': new_trainingformation.id_trainingformation,
            'formation': {
                'id_formasi': formations.id_formasi,
                'formasi': formations.formasi,
                'team': {
                    'team': formations.team.team,
                    'nama_team': formations.team.nama_team,
                    'kategori_team': formations.team.kategori_team,
                    'logo_team': formations.team.logo_team.url if formations.team.logo_team else None
                }
            },
            'lineup': lineup_data
        }

    @staticmethod
    def get(trainingformation_id):
        trainingformation_obj = get_object_or_404(trainingformation, id_trainingformation=trainingformation_id)
        lineup_entries = trainingformation_obj.id_lineup.all()
        lineup_data = [
            {
                'id_lineup': lineup.id_lineup,
                'player': {
                    'player': lineup.player.player,
                    'nama': lineup.player.nama,
                    'posisi': lineup.player.posisi,
                    'nomor_punggung': lineup.player.nomor_punggung,
                    'foto_profil': lineup.player.foto_profil.url if lineup.player.foto_profil else None
                },
                'index': lineup.index,
                'status': lineup.status
            } for lineup in lineup_entries
        ]

        return {
            'id_trainingformation': trainingformation_obj.id_trainingformation,
            'formation': {
                'id_formasi': trainingformation_obj.id_formations.id_formasi,
                'formasi': trainingformation_obj.id_formations.formasi,
                'team': {
                    'team': trainingformation_obj.id_formations.team.team,
                    'nama_team': trainingformation_obj.id_formations.team.nama_team,
                    'kategori_team': trainingformation_obj.id_formations.team.kategori_team,
                    'logo_team': trainingformation_obj.id_formations.team.logo_team.url if trainingformation_obj.id_formations.team.logo_team else None
                }
            },
            'lineup': lineup_data
        }

    @staticmethod
    def get_all():
        trainingformations = trainingformation.objects.all()
        return [
            {
                'id_trainingformation': tf.id_trainingformation,
                'formation': {
                    'id_formasi': tf.id_formations.id_formasi,
                    'formasi': tf.id_formations.formasi,
                    'team': {
                        'team': tf.id_formations.team.team,
                        'nama_team': tf.id_formations.team.nama_team,
                        'kategori_team': tf.id_formations.team.kategori_team,
                        'logo_team': tf.id_formations.team.logo_team.url if tf.id_formations.team.logo_team else None
                    }
                },
                'lineup': [
                    {
                        'id_lineup': lineup.id_lineup,
                        'player': {
                            'player': lineup.player.player,
                            'nama': lineup.player.nama,
                            'posisi': lineup.player.posisi,
                            'nomor_punggung': lineup.player.nomor_punggung,
                            'foto_profil': lineup.player.foto_profil.url if lineup.player.foto_profil else None
                        },
                        'index': lineup.index,
                        'status': lineup.status
                    } for lineup in tf.id_lineup.all()
                ]
            } for tf in trainingformations
        ]

    @staticmethod
    def put(req):
        trainingformation_obj = get_object_or_404(trainingformation, id_trainingformation=req['id_trainingformation'])
        formations = get_object_or_404(Formation, id_formasi=req['id_formations'])
        trainingformation_obj.id_formations = formations
        # Clear existing lineup entries and add new ones
        trainingformation_obj.id_lineup.clear()
        lineup_ids = req['id_lineup']
        for lineup_id in lineup_ids:
            Lineup = get_object_or_404(LineUp, id_lineup=lineup_id)
            trainingformation_obj.id_lineup.add(Lineup)

        lineup_entries = trainingformation_obj.id_lineup.all()
        lineup_data = [
            {
                'id_lineup': lineup.id_lineup,
                'player': {
                    'player': lineup.player.player,
                    'nama': lineup.player.nama,
                    'posisi': lineup.player.posisi,
                    'nomor_punggung': lineup.player.nomor_punggung,
                    'foto_profil': lineup.player.foto_profil.url if lineup.player.foto_profil else None
                },
                'index': lineup.index,
                'status': lineup.status
            } for lineup in lineup_entries
        ]

        return {
            'id_trainingformation': trainingformation_obj.id_trainingformation,
            'formation': {
                'id_formasi': formations.id_formasi,
                'formasi': formations.formasi,
                'team': {
                    'team': formations.team.team,
                    'nama_team': formations.team.nama_team,
                    'kategori_team': formations.team.kategori_team,
                    'logo_team': formations.team.logo_team.url if formations.team.logo_team else None
                }
            },
            'lineup': lineup_data
        }

    @staticmethod
    def delete(req):
        trainingformation_obj = get_object_or_404(trainingformation, id_trainingformation=req['id_trainingformation'])
        trainingformation_obj.delete()
        return {'message': f"TrainingFormation with id {req['id_trainingformation']} has been deleted."}