import uuid
from .repo import RepoMetricCategory

class UsecaseMetricCategory:
    @staticmethod
    def get_all():
        return RepoMetricCategory.get_all()

    @staticmethod
    def get(metric_category_id):
        return RepoMetricCategory.get(metric_category_id)

    @staticmethod
    def post(request):
        reqs = {
            'metric_category': uuid.uuid4(),
            'name': request.data['name'],
            'description': request.data.get('description', '')
        }
        return RepoMetricCategory.post(reqs)

    @staticmethod
    def put(request):
        reqs = {
            'metric_category': request.data['metric_category'],
            'name': request.data['name'],
            'description': request.data.get('description', '')
        }
        return RepoMetricCategory.put(reqs)

    @staticmethod
    def delete(request):
        reqs = {
            'metric_category': request.data['metric_category']
        }
        return RepoMetricCategory.delete(reqs)
