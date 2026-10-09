import os
import cv2
import threading
import logging
from datetime import datetime
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from analysis.services.heading_processor import run_heading_pipeline
from analysis.services.passing_processor import run_passing_pipeline
from analysis.job_store import JobStore
from analysis.views.helpers import get_json_data

logger = logging.getLogger(__name__)


def get_video_fps(video_path: str) -> int:
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return 30
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    return int(round(fps)) if 0 < fps <= 120 else 30


@csrf_exempt
def start_processing(request, job_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    payload = get_json_data(request)
    input_path = payload.get('input_path')
    if not input_path:
        return JsonResponse({'error': 'input_path required'}, status=400)

    input_path_abs = os.path.abspath(os.path.join(settings.BASE_DIR, input_path)) if not os.path.isabs(input_path) else input_path
    if not os.path.exists(input_path_abs):
        return JsonResponse({'error': 'File not found'}, status=404)

    actual_fps = get_video_fps(input_path_abs)

    analysis_type = payload.get('analysis_type', 'heading')
    player_names = payload.get('player_names', [])
    detection_mode = payload.get('detection_mode', 'manual')

    if analysis_type == 'passing':
        model_path = getattr(settings, 'ANALYSIS_MODEL_PATH_PASSING', os.path.join(settings.BASE_DIR, 'static', 'models', 'passing.pt'))
        if not os.path.exists(model_path):
            model_path = getattr(settings, 'ANALYSIS_MODEL_PATH', os.path.join(settings.BASE_DIR, 'static', 'models', 'best.pt'))
    else:
        model_path = getattr(settings, 'ANALYSIS_MODEL_PATH', os.path.join(settings.BASE_DIR, 'static', 'models', 'best.pt'))

    if not model_path or not os.path.exists(os.path.abspath(model_path)):
        return JsonResponse({'error': f'Model path invalid: {model_path}'}, status=500)

    output_folder = os.path.abspath(getattr(settings, 'ANALYSIS_OUTPUT_FOLDER', os.path.join(settings.BASE_DIR, 'static', 'outputs')))
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, f"{job_id}_output.mp4")

    JobStore.create(job_id, {
        'status': 'queued',
        'analysis_type': analysis_type,
        'input_path': input_path_abs,
        'output_path': output_path,
        'model_path': os.path.abspath(model_path),
        'fps': actual_fps,
        'player_names': player_names,
        'created_at': datetime.utcnow().isoformat()
    })

    def background_task():
        try:
            JobStore.update(job_id, {'status': 'processing', 'progress': 0})
            if analysis_type == 'passing':
                result = run_passing_pipeline(
                    input_path=input_path_abs,
                    output_path=output_path,
                    job_id=job_id,
                    model_path=os.path.abspath(model_path),
                    player_names=player_names,
                    detection_mode=detection_mode,
                    fps=actual_fps,
                    use_stub=True,
                    config_overrides={
                        "debug_trajectory": False,
                        "show_stats_panel": True,
                        "output_format": "mp4"
                    }
                )
            else:
                result = run_heading_pipeline(
                    input_path=input_path_abs,
                    output_path=output_path,
                    job_id=job_id,
                    model_path=os.path.abspath(model_path),
                    fps=actual_fps,
                    use_stub=True,
                    config_overrides={
                        "head_bbox_margin": 20.0, "max_head_ball_center_distance": 80.0,
                        "max_approach_distance": 200.0, "min_approach_frames": 2,
                        "cooldown_frames": 25, "max_approach_duration_sec": 4.0,
                        "min_away_frames": 5, "debug_trajectory": False,
                        "show_stats_panel": True, "output_format": "mp4"
                    }
                )
            JobStore.update(job_id, result)
        except Exception as e:
            logger.error(f"[{job_id}] Error: {str(e)}", exc_info=True)
            JobStore.update(job_id, {'status': 'failed', 'error': str(e)})

    threading.Thread(target=background_task, daemon=True).start()
    return JsonResponse({'job_id': job_id, 'status': 'queued', 'message': 'Processing started'}, status=202)


def get_status(request, job_id):
    job = JobStore.get(job_id)
    if not job:
        return JsonResponse({'error': 'Job not found'}, status=404)
    return JsonResponse(job, status=200)
