from .repo import RepoSchedule
import uuid

class UsecaseSchedule:
    @staticmethod
    def post(request):
        reqs = {
            'schedule': uuid.uuid4(),
            'tanggal': request.data['tanggal'],
            'start_time': request.data['start_time'],
            'end_time': request.data['end_time']
        }
        dataPost = RepoSchedule.post(reqs)
        return dataPost
    
    @staticmethod
    def get(schedule_id):
        dataSchedule = RepoSchedule.get(schedule_id)
        return dataSchedule
    
    @staticmethod
    def get_all():
        return RepoSchedule.get_all()
    
    def put(request):
        reqs = {
            'schedule': request.data['schedule'],
            'tanggal': request.data.get('tanggal'),
            'start_time' : request.data.get('start_time'),
            'end_time' : request.data.get('end_time')
        }
        updated_schedule = RepoSchedule.put(reqs)
        return updated_schedule
    
    def delete(request):
        reqs = {
            'schedule': request.data['schedule']
        }
        delete_message = RepoSchedule.delete(reqs)
        return delete_message
    
   