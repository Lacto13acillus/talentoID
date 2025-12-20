from .repo import RepoTrainingCategory
import uuid

class UsecaseTrainingCategory:
    @staticmethod
    def post(request):
        reqs = {
            'trainingcategory': uuid.uuid4(),
            'nama_category': request.data['nama_category']
        }
        dataPost = RepoTrainingCategory.post(reqs)
        return dataPost
    
    @staticmethod
    def get(trainingcategory_id):
        dataTrainingCategory = RepoTrainingCategory.get(trainingcategory_id)
        return dataTrainingCategory
    
    @staticmethod
    def get_all():
        return RepoTrainingCategory.get_all()
    
    def put(request):
        reqs = {
            'trainingcategory': request.data['trainingcategory'],
            'nama_category': request.data.get('nama_category')
        }
        updated_trainingcategory = RepoTrainingCategory.put(reqs)
        return updated_trainingcategory
    
    def delete(request):
        reqs = {
            'trainingcategory': request.data['trainingcategory']
        }
        delete_message = RepoTrainingCategory.delete(reqs)
        return delete_message