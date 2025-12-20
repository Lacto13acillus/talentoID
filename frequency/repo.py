from django.shortcuts import get_object_or_404
from .models import frequency

class RepoFrequency:
    @staticmethod
    def post(req):
        new_frequency = frequency.objects.create(
            frequency=req['frequency'],
            frequency_time=req['frequency_time']
        )
        return {
            'frequency': new_frequency.frequency,
            'frequency_time': new_frequency.get_frequency_time_display()
        }

    @staticmethod
    def get(frequency_id):
        freq = get_object_or_404(frequency, frequency=frequency_id)
        return {
            'frequency': freq.frequency,
            'frequency_time': freq.get_frequency_time_display()
        }

    @staticmethod
    def get_all():
        frequencies = frequency.objects.all()
        return [
            {
                'frequency': freq.frequency,
                'frequency_time': freq.get_frequency_time_display()
            }
            for freq in frequencies
        ]

    @staticmethod
    def put(req):
        freq = get_object_or_404(frequency, frequency=req['frequency'])
        freq.frequency_time = req.get('frequency_time', freq.frequency_time)
        freq.save()
        return {
            'frequency': freq.frequency,
            'frequency_time': freq.get_frequency_time_display()
        }

    @staticmethod
    def delete(req):
        freq = get_object_or_404(frequency, frequency=req['frequency'])
        freq.delete()
        return {'message': f"Frequency with id {req['frequency']} has been deleted."}