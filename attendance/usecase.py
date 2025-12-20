from .repo import RepoAttendance
import uuid

class UsecaseAttendance:
    @staticmethod
    def post_training(request):
        reqs = {
            'training': request.data.get('training'),
            'attendances': request.data['attendances']
        }
        return RepoAttendance.post_training(reqs)

    @staticmethod
    def get_training(attendance_id):
        return RepoAttendance.get_training(attendance_id)

    @staticmethod
    def get_all_training():
        return RepoAttendance.get_all_training()

    @staticmethod
    def get_by_training(training_id):
        return RepoAttendance.get_by_training(training_id)

    @staticmethod
    def get_by_player(player_id):
        return RepoAttendance.get_by_player(player_id)

    @staticmethod
    def put_training(request):
        reqs = {
            'attendance': request.data['attendance'],
            'player': request.data['player'],
            'training': request.data.get('training'),
            'attendance_status': request.data.get('attendance_status'),
            'notes': request.data.get('notes')
        }
        return RepoAttendance.put_training(reqs)

    @staticmethod
    def delete_training(request):
        reqs = {
            'attendance': request.data['attendance']
        }
        return RepoAttendance.delete_training(reqs)
