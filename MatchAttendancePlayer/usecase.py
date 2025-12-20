from .repo import RepoMatchAttendancePlayer
import uuid

class UsecaseMatchAttendancePlayer:
    @staticmethod
    def post_match_attendance_player(request):
        reqs = {
            'attendance_id': str(uuid.uuid4()),
            'player': request.data['player'],
            'match': request.data.get('match'),  # Optional
            'status': request.data['status'],
            'reason_absent': request.data.get('reason_absent')
        }
        return RepoMatchAttendancePlayer.post_match_attendance_player(reqs)

    @staticmethod
    def get_match_attendance_player(attendance_id):
        return RepoMatchAttendancePlayer.get_match_attendance_player(attendance_id)

    @staticmethod
    def get_all_match_attendance_player():
        return RepoMatchAttendancePlayer.get_all_match_attendance_player()

    @staticmethod
    def get_by_player(player_id):
        return RepoMatchAttendancePlayer.get_by_player(player_id)
    
    @staticmethod
    def put_match_attendance_player(request):
        reqs = {
            'attendance_id': request.data['attendance_id'],
            'player': request.data['player'],
            'match': request.data.get('match'),  # Optional
            'status': request.data.get('status'),
            'reason_absent': request.data.get('reason_absent')
        }
        return RepoMatchAttendancePlayer.put_match_attendance_player(reqs)

    @staticmethod
    def delete_match_attendance_player(request):
        reqs = {
            'attendance_id': request.data['attendance_id']
        }
        return RepoMatchAttendancePlayer.delete_match_attendance_player(reqs)

    @staticmethod
    def get_by_match_id(match_id):
        return RepoMatchAttendancePlayer.get_by_match_id(match_id)