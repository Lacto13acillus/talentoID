import os
import logging
from django.http import JsonResponse

from analysis.job_store import JobStore
from analysis.views.helpers import build_video_stream_response, build_file_download_response

logger = logging.getLogger(__name__)


def download_video(request, job_id):
    job = JobStore.get(job_id)
    if not job or job.get('status') != 'completed':
        return JsonResponse({'error': 'Video not ready'}, status=404)

    output_path = job.get('output_video')
    if not output_path or not os.path.exists(output_path):
        return JsonResponse({'error': 'Video file not found'}, status=404)

    analysis_type = job.get('analysis_type', 'heading')
    prefix = 'passing_analysis' if analysis_type == 'passing' else 'heading_analysis'
    return build_file_download_response(output_path, f"{prefix}_{job_id}.mp4")


def stream_video(request, job_id):
    job = JobStore.get(job_id)
    if not job or job.get('status') != 'completed':
        return JsonResponse({'error': 'Video not ready'}, status=404)

    output_path = job.get('output_video')
    if not output_path or not os.path.exists(output_path):
        return JsonResponse({'error': 'Video file not found'}, status=404)

    return build_video_stream_response(request, output_path)


def get_video_info(request, job_id):
    job = JobStore.get(job_id)
    if not job:
        return JsonResponse({'error': 'Job not found'}, status=404)
    output_path = job.get('output_video')
    if not output_path or not os.path.exists(output_path):
        return JsonResponse({'error': 'File not found'}, status=404)

    return JsonResponse({
        'size_mb': round(os.path.getsize(output_path) / (1024 * 1024), 2),
        'format': 'mp4',
        'stream_url': f'/api/download/{job_id}/stream'
    }, status=200)
