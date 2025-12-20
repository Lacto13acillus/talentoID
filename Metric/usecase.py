from .repo import RepoMetric
from django.core.exceptions import ValidationError
import uuid


class UsecaseMetric:
    @staticmethod
    def get_all():
        return RepoMetric.get_all()

    @staticmethod
    def get(metric_id):
        return RepoMetric.get(metric_id)

    @staticmethod
    def post(request):
        reqs = {
            'metric': uuid.uuid4(),
            'metric_category': request.data['metric_category'],
            'name': request.data['name'],
            'description': request.data.get('description', '')
        }
        return RepoMetric.post(reqs)

    @staticmethod
    def put(request):
        reqs = {
            'metric': request.data['metric'],
            'metric_category': request.data.get('metric_category'),
            'name': request.data.get('name'),
            'description': request.data.get('description'),
        }

        return RepoMetric.put(reqs)

    @staticmethod
    def delete(request):
        metric = request.data.get('metric')

        return RepoMetric.delete(metric)
