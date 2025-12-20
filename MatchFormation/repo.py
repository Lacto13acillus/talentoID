from django.shortcuts import get_object_or_404
from .models import MatchFormations
from formations.models import Formation

class RepoMatchFormations:
    @staticmethod
    def post(req):
        formation = get_object_or_404(Formation, id_formasi=req['id_formations'])
        new_matchformation = MatchFormations.objects.create(
            id_matchformations=req['id_matchformations'],
            id_formations=formation
        )
        return {
            'id_matchformations': new_matchformation.id_matchformations,
            'formation': {
                'id_formasi': formation.id_formasi,
                'formasi': formation.formasi,
            }
        }

    @staticmethod
    def get(matchformation_id):
        matchformation = get_object_or_404(MatchFormations, id_matchformations=matchformation_id)
        return {
            'id_matchformations': matchformation.id_matchformations,
            'formation': {
                'id_formasi': matchformation.id_formations.id_formasi,
                'formasi': matchformation.id_formations.formasi,
            }
        }

    @staticmethod
    def get_all():
        matchformations = MatchFormations.objects.all()
        return [
            {
                'id_matchformations': mf.id_matchformations,
                'formation': {
                    'id_formasi': mf.id_formations.id_formasi,
                    'formasi': mf.id_formations.formasi,
                }
            } for mf in matchformations
        ]

    @staticmethod
    def put(req):
        matchformation = get_object_or_404(MatchFormations, id_matchformations=req['id_matchformations'])
        formation = get_object_or_404(Formation, id_formasi=req['id_formations'])
        matchformation.id_formations = formation
        matchformation.save()
        return {
            'id_matchformations': matchformation.id_matchformations,
            'formation': {
                'id_formasi': formation.id_formasi,
                'formasi': formation.formasi,
            }
        }

    @staticmethod
    def delete(req):
        matchformation = get_object_or_404(MatchFormations, id_matchformations=req['id_matchformations'])
        matchformation.delete()
        return {'message': f"MatchFormation with id {req['id_matchformations']} has been deleted."}