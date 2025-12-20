from django.shortcuts import get_object_or_404
from .models import schedule

class RepoSchedule:
    @staticmethod
    def post(req):
        new_schedule = schedule.objects.create(
            schedule= req['schedule'], 
            tanggal= req['tanggal'],
            start_time= req['start_time'], 
            end_time= req['end_time']
        )
        return {
            'schedule': new_schedule.schedule,
            'tanggal': new_schedule.tanggal,
            'start_time': new_schedule.start_time,
            'end_time': new_schedule.end_time,
        }
    
    @staticmethod
    def get(schedule_id):
        schedule_update = get_object_or_404(schedule, schedule=schedule_id)
        
        return {
            'schedule': schedule_update.schedule,
            'tanggal': schedule_update.tanggal,
            'start_time': schedule_update.start_time,
            'end_time': schedule_update.end_time,
        }
    
    @staticmethod
    def get_all():
        schedules = schedule.objects.all()
        return [{
            'schedule': sched.schedule,
            'tanggal': sched.tanggal,
            'start_time': sched.start_time,
            'end_time': sched.end_time
        } for sched in schedules]

    def put(req):
        Schedule = get_object_or_404(schedule, schedule=req['schedule'])
        Schedule.tanggal = req.get('tanggal', schedule.tanggal)
        Schedule.start_time = req.get('start_time', schedule.start_time)
        Schedule.end_time = req.get('end_time', schedule.end_time)
        Schedule.save()
        return{
            'schedule': Schedule.schedule,
            'tanggal': Schedule.tanggal,
            'start_time' : Schedule.start_time,
            'end_time' : Schedule.end_time
        }
    
    def delete(req):
        Schedule = get_object_or_404(schedule, schedule=req['schedule'])
        Schedule.delete()
        return {'message': f"User with id {req['schedule']} has been deleted."}