from django.shortcuts import get_object_or_404
from .models import trainingcategory

class RepoTrainingCategory:
    @staticmethod
    def post(req):
        new_TrainingCategory = trainingcategory.objects.create(
            trainingcategory= req['trainingcategory'], 
            nama_category= req['nama_category'] 
        )
        return {
            'trainingcategory': new_TrainingCategory.trainingcategory,
            'nama_category': new_TrainingCategory.nama_category
        }
    
    @staticmethod
    def get(trainingcategory_id):
        trainingcategory_update = get_object_or_404(trainingcategory, trainingcategory=trainingcategory_id)
        
        return {
            'trainingcategory': trainingcategory_update.trainingcategory,
            'nama_category': trainingcategory_update.nama_category
        }
    
    @staticmethod
    def get_all():
        categories = trainingcategory.objects.all()
        return [{
            'trainingcategory': category.trainingcategory,
            'nama_category': category.nama_category
        } for category in categories]

    def put(req):
        TG = get_object_or_404(trainingcategory, trainingcategory=req['trainingcategory'])
        TG.nama_category = req.get('nama_category', trainingcategory.nama_category)
        TG.save()
        return{
            'trainingcategory': TG.trainingcategory,
            'nama_category': TG.nama_category
        }
    
    def delete(req):
        TG = get_object_or_404(trainingcategory, trainingcategory=req['trainingcategory'])
        TG.delete()
        return {'message': f"User with id {req['trainingcategory']} has been deleted."}