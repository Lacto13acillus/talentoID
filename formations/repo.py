from django.shortcuts import get_object_or_404
from .models import Formation

class RepoFormation:
    @staticmethod
    def post(req):
        new_formation = Formation.objects.create(
            id_formasi=req['id_formasi'],
            formasi=req['formasi']
        )
        return {
            'id_formasi': new_formation.id_formasi,
            'formasi': new_formation.formasi
        }
    
    @staticmethod
    def get_by_id(id_formasi):
        formation = get_object_or_404(Formation, id_formasi=id_formasi)

        return {
            'id_formasi': formation.id_formasi,
            'formasi': formation.formasi,
        }

    @staticmethod
    def get_all():
        formations = Formation.objects.all()
        result = []
        
        for formation in formations:
            formation_data = {
                'id_formasi': formation.id_formasi,
                'formasi': formation.formasi,
            }
            result.append(formation_data)
        
        return result

    @staticmethod
    def put(req):
        formation = get_object_or_404(Formation, id_formasi=req['id_formasi'])
        formation.formasi = req['formasi']
        formation.save()
        return {
            'id_formasi': formation.id_formasi,
            'formasi': formation.formasi,
        }

    @staticmethod
    def delete(req):
        formation = get_object_or_404(Formation, id_formasi=req['id_formasi'])
        formation.delete()
        return {'message': f"Formation with id {req['id_formasi']} has been deleted."}