from .repo import RepoMatchAttendance
import uuid

class UsecaseMatchAttendance:
    @staticmethod
    def post_match_attendance(request):
        reqs = {
            'match': request.data.get('match'),  
            'match_attendances': request.data['match_attendances']
        }
        return RepoMatchAttendance.post_match_attendance(reqs)

    @staticmethod
    def get_match_attendance(match_attendance_id):
        return RepoMatchAttendance.get_match_attendance(match_attendance_id)

    @staticmethod
    def get_all_match_attendance():
        return RepoMatchAttendance.get_all_match_attendance()

    @staticmethod
    def get_by_player(player_id):
        return RepoMatchAttendance.get_by_player(player_id)
    
    @staticmethod
    def put_match_attendance(request):
        reqs = {
            'match_attendance': request.data['match_attendance'],
            'player': request.data['player'],
            'match': request.data.get('match'), 
            'attendance_status': request.data.get('attendance_status'),
            'notes': request.data.get('notes')
        }
        return RepoMatchAttendance.put_match_attendance(reqs)

    @staticmethod
    def delete_match_attendance(request):
        reqs = {
            'match_attendance': request.data['match_attendance']
        }
        return RepoMatchAttendance.delete_match_attendance(reqs)