from .repo import RepoTrainingAttendancePlayer
import uuid

class UsecaseTrainingAttendancePlayer:
    @staticmethod
    def post_training_attendance_player(request):
        reqs = {
            'trainingattendance_id': str(uuid.uuid4()),
            'player': request.data['player'],
            'training': request.data.get('training'),  # Optional
            'status': request.data['status'],
            'reason_absent': request.data.get('reason_absent')
        }
        return RepoTrainingAttendancePlayer.post_training_attendance_player(reqs)

    @staticmethod
    def get_training_attendance_player(trainingattendance_id):
        return RepoTrainingAttendancePlayer.get_training_attendance_player(trainingattendance_id)

    @staticmethod
    def get_all_training_attendance_player():
        return RepoTrainingAttendancePlayer.get_all_training_attendance_player()

    @staticmethod
    def get_by_player(player_id):
        return RepoTrainingAttendancePlayer.get_by_player(player_id)

    @staticmethod
    def get_by_training(training_id):
        return RepoTrainingAttendancePlayer.get_by_training(training_id)
    
    @staticmethod
    def put_training_attendance_player(request):
        reqs = {
            'trainingattendance_id': request.data['trainingattendance_id'],
            'player': request.data['player'],
            'training': request.data.get('training'),  # Optional
            'status': request.data.get('status'),
            'reason_absent': request.data.get('reason_absent')
        }
        return RepoTrainingAttendancePlayer.put_training_attendance_player(reqs)

    @staticmethod
    def delete_training_attendance_player(request):
        reqs = {
            'trainingattendance_id': request.data['trainingattendance_id']
        }
        return RepoTrainingAttendancePlayer.delete_training_attendance_player(reqs)