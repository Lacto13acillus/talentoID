import os
import uuid as uuid_lib
import logging
import requests as http_requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from analysis.job_store import JobStore
from analysis.models import TotalResult, PlayerResult
from footprint.models import footprint as Footprint
from analysis.services.s3_service import upload_video_to_s3, generate_s3_key
from analysis.views.helpers import get_json_data, build_video_stream_response, MAX_VIDEO_SIZE_MB

logger = logging.getLogger(__name__)


def test(request):
    return JsonResponse({'status': 'ok', 'message': 'Manual count blueprint aktif!'})


@csrf_exempt
def upload(request):
    """Upload file video untuk manual counting."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    if 'video' not in request.FILES:
        return JsonResponse({'error': 'No video file'}, status=400)

    file = request.FILES['video']
    if not file.name:
        return JsonResponse({'error': 'No selected file'}, status=400)

    upload_dir = getattr(settings, 'ANALYSIS_UPLOAD_FOLDER', os.path.join(settings.BASE_DIR, 'static', 'uploads'))
    os.makedirs(upload_dir, exist_ok=True)
    input_path = os.path.join(upload_dir, file.name)

    with open(input_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    job_id = JobStore.create_job('manual', input_path, file.name)
    return JsonResponse({'job_id': job_id, 'message': 'Upload berhasil'})


@csrf_exempt
def upload_url(request):
    """Download video dari URL untuk manual count."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    data = get_json_data(request)
    video_url = data.get('video_url', '').strip()

    if not video_url:
        return JsonResponse({'error': 'video_url wajib diisi'}, status=400)
    if not video_url.startswith(('http://', 'https://')):
        return JsonResponse({'error': 'URL harus dimulai dengan http:// atau https://'}, status=400)

    try:
        from urllib.parse import urlparse, unquote
        parsed = urlparse(video_url)
        url_filename = os.path.basename(unquote(parsed.path))
        valid_exts = ('.mp4', '.avi', '.mov', '.mkv', '.webm')
        if not any(url_filename.lower().endswith(ext) for ext in valid_exts):
            url_filename = f"{uuid_lib.uuid4().hex[:12]}.mp4"
    except Exception:
        url_filename = f"{uuid_lib.uuid4().hex[:12]}.mp4"

    try:
        resp = http_requests.get(
            video_url, stream=True, timeout=30,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        resp.raise_for_status()

        upload_dir = getattr(settings, 'ANALYSIS_UPLOAD_FOLDER', os.path.join(settings.BASE_DIR, 'static', 'uploads'))
        os.makedirs(upload_dir, exist_ok=True)
        input_path = os.path.join(upload_dir, url_filename)

        downloaded = 0
        max_bytes = MAX_VIDEO_SIZE_MB * 1024 * 1024
        with open(input_path, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    downloaded += len(chunk)
                    if downloaded > max_bytes:
                        f.close()
                        os.remove(input_path)
                        return JsonResponse({'error': f'Video terlalu besar. Maksimal {MAX_VIDEO_SIZE_MB}MB'}, status=400)
                    f.write(chunk)

    except Exception as e:
        return JsonResponse({'error': f'Gagal download video: {str(e)}'}, status=500)

    job_id = JobStore.create_job('manual', input_path, url_filename)
    return JsonResponse({'job_id': job_id, 'message': f'Video berhasil didownload ({downloaded / 1024 / 1024:.1f}MB)'})


@csrf_exempt
def submit(request):
    """Simpan hasil manual count ke TotalResult dan PlayerResult."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    data = get_json_data(request)
    job_id = data.get('job_id')
    footprint_id = data.get('footprint_id')
    total_passing = data.get('total_passing', 0)
    passing_sukses = data.get('passing_sukses', 0)
    passing_gagal = data.get('passing_gagal', 0)
    player_results_data = data.get('player_results', [])

    try:
        total_passing = int(total_passing)
        passing_sukses = int(passing_sukses)
        passing_gagal = int(passing_gagal)
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Statistik harus berupa angka'}, status=400)

    # Duplicate Guard
    if footprint_id:
        existing_result = TotalResult.objects.filter(
            footprint_id=footprint_id, status='generated'
        ).first()
        if existing_result:
            return JsonResponse({
                'error': f'Training category ini sudah pernah dianalisis (result: {existing_result.id}). Tidak bisa diproses ulang.',
                'existing_result_id': str(existing_result.id)
            }, status=409)

    akurasi = TotalResult.calculate_accuracy(total_passing, passing_sukses)

    try:
        new_record = TotalResult.objects.create(
            total_passing=total_passing,
            passing_sukses=passing_sukses,
            passing_gagal=passing_gagal,
            akurasi_passing=akurasi,
            status='generated',
            parent_id=None,
            footprint_id=footprint_id
        )
        result_id = new_record.id

        saved_players = []
        for pr in player_results_data:
            p_name = pr.get('player', '').strip()
            if not p_name:
                continue
            p_total = int(pr.get('total_passing', 0))
            p_sukses = int(pr.get('passing_sukses', 0))
            p_gagal = int(pr.get('passing_gagal', 0))
            p_akurasi = PlayerResult.calculate_accuracy(p_total, p_sukses)

            PlayerResult.objects.create(
                total_result=new_record,
                player=p_name,
                total_passing=p_total,
                passing_sukses=p_sukses,
                passing_gagal=p_gagal,
                akurasi_passing=p_akurasi,
                status='generated',
                footprint_id=footprint_id
            )
            saved_players.append({
                'player': p_name,
                'total_passing': p_total,
                'passing_sukses': p_sukses,
                'passing_gagal': p_gagal,
                'akurasi_passing': p_akurasi,
            })

        # Upload video ke S3 & update footprint
        if footprint_id:
            try:
                fp_record = Footprint.objects.filter(footprint=footprint_id).first()
                if fp_record:
                    fp_record.type = 'by admin'
                    s3_url = None
                    if job_id:
                        job = JobStore.get_job(job_id)
                        if job and job.get('input_path') and os.path.exists(job['input_path']):
                            try:
                                s3_key = generate_s3_key('manual', job_id, os.path.basename(job['input_path']))
                                s3_url = upload_video_to_s3(job['input_path'], s3_key)
                            except Exception as s3_err:
                                logger.error(f"S3 upload error: {s3_err}")

                            fp_record.media_after = s3_url if s3_url else os.path.abspath(job['input_path'])
                    fp_record.save()
            except Exception as fp_err:
                logger.error(f"Failed to update footprint: {fp_err}")

        return JsonResponse({
            'status': 'success',
            'message': 'Hasil manual counting berhasil disimpan',
            'result_id': str(result_id),
            'total_result': {
                'id': str(result_id),
                'total_passing': total_passing,
                'passing_sukses': passing_sukses,
                'passing_gagal': passing_gagal,
                'akurasi_passing': akurasi,
            },
            'player_results': saved_players,
        })

    except Exception as db_err:
        logger.error(f"Failed to save manual count: {db_err}")
        return JsonResponse({'error': f'Gagal menyimpan: {str(db_err)}'}, status=500)


def preview(request, job_id):
    """Stream video input/original untuk manual count preview."""
    job = JobStore.get_job(job_id)
    if not job or not job.get('input_path') or not os.path.exists(job['input_path']):
        return JsonResponse({'error': 'Video tidak ditemukan'}, status=404)
    return build_video_stream_response(request, job['input_path'])
