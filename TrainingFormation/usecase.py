from .repo import RepoTrainingFormation
import uuid

class UsecaseTrainingFormation:
    @staticmethod
    def post(request):
        reqs = {
            'id_trainingformation': uuid.uuid4(),
            'id_formations': request.data['id_formations'],
            'id_lineup': request.data['id_lineup']  # Expecting a list of lineup IDs
        }
        data_post = RepoTrainingFormation.post(reqs)
        return data_post

    @staticmethod
    def get(trainingformation_id):
        data = RepoTrainingFormation.get(trainingformation_id)
        return data

    @staticmethod
    def get_all():
        data = RepoTrainingFormation.get_all()
        return data

    @staticmethod
    def put(request):
        reqs = {
            'id_trainingformation': request.data['id_trainingformation'],
            'id_formations': request.data['id_formations'],
            'id_lineup': request.data['id_lineup']  # Expecting a list of lineup IDs
        }
        data_put = RepoTrainingFormation.put(reqs)
        return data_put

    @staticmethod
    def delete(request):
        reqs = {
            'id_trainingformation': request.data['id_trainingformation']
        }
        data_delete = RepoTrainingFormation.delete(reqs)
        return data_delete