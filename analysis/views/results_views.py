import logging
from django.http import JsonResponse
from analysis.job_store import JobStore

logger = logging.getLogger(__name__)


def get_results(request, job_id):
    """Ambil hasil statistics dan events."""
    job = JobStore.get(job_id)
    if not job:
        return JsonResponse({'error': 'Job not found'}, status=404)

    if job.get('status') != 'completed':
        return JsonResponse({
            'job_id': job_id,
            'status': job.get('status', 'pending'),
            'progress': job.get('progress', 0),
            'message': 'Processing not yet completed'
        }, status=200)

    analysis_type = job.get('analysis_type', 'heading')

    if analysis_type == 'passing':
        return JsonResponse({
            'job_id': job_id,
            'status': 'completed',
            'analysis_type': 'passing',
            'stats': job.get('stats'),
            'pass_events': job.get('pass_events', []),
            'output_video_url': f"/api/download/{job_id}/video"
        }, status=200)
    else:
        return JsonResponse({
            'job_id': job_id,
            'status': 'completed',
            'analysis_type': 'heading',
            'stats': job.get('stats'),
            'heading_events': job.get('heading_events', []),
            'output_video_url': f"/api/download/{job_id}/video"
        }, status=200)
