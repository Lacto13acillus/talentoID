from .repo import RepoResult
import uuid
from django.core.exceptions import ValidationError

class UsecaseResult:
    @staticmethod
    def post(request):
        required_fields = ['training', 'attendance_summary', 'footprint_summary', 'overall_evaluation']
        missing_fields = [field for field in required_fields if field not in request.data]
        if missing_fields:
            raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")

        reqs = {
            'result': str(uuid.uuid4()),
            'training': request.data['training'],
            'attendance_summary': request.data['attendance_summary'],
            'footprint_summary': request.data['footprint_summary'],
            'overall_evaluation': request.data['overall_evaluation']
        }
        return RepoResult.post(reqs)

    @staticmethod
    def get(result_id):
        return RepoResult.get(result_id)

    @staticmethod
    def get_all():
        return RepoResult.get_all()

    @staticmethod
    def put(request):
        required_fields = ['result', 'training']
        missing_fields = [field for field in required_fields if field not in request.data]
        if missing_fields:
            raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")

        reqs = {
            'result': request.data['result'],
            'training': request.data['training'],
            'attendance_summary': request.data.get('attendance_summary'),
            'footprint_summary': request.data.get('footprint_summary'),
            'overall_evaluation': request.data.get('overall_evaluation')
        }
        return RepoResult.put(reqs)

    @staticmethod
    def delete(request):
        if 'result' not in request.data:
            raise ValidationError("result id is required")

        reqs = {
            'result': request.data['result']
        }
        return RepoResult.delete(reqs)