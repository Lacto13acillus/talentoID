from .repo import RepoFrequency
import uuid

class UsecaseFrequency:
    @staticmethod
    def post(request):
        reqs = {
            'frequency': uuid.uuid4(),
            'frequency_time': request.data['frequency_time']
        }
        data_post = RepoFrequency.post(reqs)
        return data_post

    @staticmethod
    def get(frequency_id):
        data_frequency = RepoFrequency.get(frequency_id)
        return data_frequency

    @staticmethod
    def get_all():
        data_frequencies = RepoFrequency.get_all()
        return data_frequencies

    @staticmethod
    def put(request):
        reqs = {
            'frequency': request.data['frequency'],
            'frequency_time': request.data.get('frequency_time')
        }
        updated_frequency = RepoFrequency.put(reqs)
        return updated_frequency

    @staticmethod
    def delete(request):
        reqs = {
            'frequency': request.data['frequency']
        }
        delete_message = RepoFrequency.delete(reqs)
        return delete_message