from django.shortcuts import get_object_or_404
from .models import status

class RepoStatus:
    @staticmethod
    def post(req):
        # Normalize and validate match_status
        input_status = req['match_status']
        valid_choices = [choice[0] for choice in status.STATUS_CHOICES]  # ['Team Ready', ...]
        # Create a case-insensitive mapping
        choice_map = {choice.lower(): choice for choice in valid_choices}
        normalized_status = choice_map.get(input_status.lower())
        if not normalized_status:
            raise ValueError(f"Invalid match_status. Must be one of {valid_choices}")

        new_status = status.objects.create(
            status=req['status'],
            match_status=normalized_status  # Use normalized value
        )
        return {
            'status': new_status.status,
            'match_status': new_status.match_status
        }
    
    @staticmethod
    def get(status_id):
        status_update = get_object_or_404(status, status=status_id)
        return {
            'status': status_update.status,
            'match_status': status_update.match_status
        }
    
    @staticmethod
    def get_all():
        statuses = status.objects.all()
        return [{
            'status': status_data.status,
            'match_status': status_data.match_status
        } for status_data in statuses]

    @staticmethod
    def put(req):
        Status = get_object_or_404(status, status=req['status'])
        # Normalize and validate match_status if provided
        if 'match_status' in req and req['match_status']:
            input_status = req['match_status']
            valid_choices = [choice[0] for choice in status.STATUS_CHOICES]
            choice_map = {choice.lower(): choice for choice in valid_choices}
            normalized_status = choice_map.get(input_status.lower())
            if not normalized_status:
                raise ValueError(f"Invalid match_status. Must be one of {valid_choices}")
            Status.match_status = normalized_status
        Status.save()
        return {
            'status': Status.status,
            'match_status': Status.match_status
        }
    
    @staticmethod
    def delete(req):
        Status = get_object_or_404(status, status=req['status'])
        Status.delete()
        return {'message': f"Status with id {req['status']} has been deleted."}