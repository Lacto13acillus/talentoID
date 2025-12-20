from .repo import RepoFootprint
import uuid
from django.core.exceptions import ValidationError

class UsecaseFootprint:
    @staticmethod
    def post(request_data):
        return RepoFootprint.post(request_data)

    @staticmethod
    def get(training_id):
        return RepoFootprint.get(training_id)

    @staticmethod
    def get_all():
        return RepoFootprint.get_all()

    @staticmethod
    def put(request):
        reqs = {
            'footprint': request.data['footprint'],
            'training': request.data['training'],
            'media': request.FILES.get('media')  # Media is optional for PUT
        }
        return RepoFootprint.put(reqs)

    @staticmethod
    def delete(request):
        reqs = {
            'footprint': request.data['footprint']
        }
        return RepoFootprint.delete(reqs)
