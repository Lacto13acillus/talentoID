import os
import uuid as uuid_lib
import logging
import requests as http_requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from analysis.job_store import JobStore
from analysis.models import TotalResult
from footprint.models import footprint as Footprint
from analysis.services.heading_processor import run_heading_pipeline
from analysis.services.s3_service import upload_video_to_s3, generate_s3_key
from analysis.views.helpers import get_json_data, build_video_stream_response, build_file_download_response, MAX_VIDEO_SIZE_MB

logger = logging.getLogger(__name__)


def test(request):
    """Endpoint test verifikasi heading views aktif."""
    return JsonResponse({'status': 'ok', 'message': 'Heading views aktif!'})


@csrf_exempt
def upload(request):
    """Upload file video untuk heading analysis."""
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

    job_id = JobStore.create_job('heading', input_path, file.name)
    logger.info(f"[HEADING] Job created: {job_id} for file {file.name}")
    return JsonResponse({'job_id': job_id, 'message': 'Upload berhasil'})


@csrf_exempt
def upload_url(request):
    """Download video dari URL lalu buat job heading."""
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

        content_length = resp.headers.get('Content-Length')
        if content_length and int(content_length) > MAX_VIDEO_SIZE_MB * 1024 * 1024:
            return JsonResponse({'error': f'Video terlalu besar. Maksimal {MAX_VIDEO_SIZE_MB}MB'}, status=400)

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

    except http_requests.exceptions.Timeout:
        return JsonResponse({'error': 'Timeout: server tidak merespon dalam 30 detik'}, status=408)
    except http_requests.exceptions.ConnectionError:
        return JsonResponse({'error': 'Gagal terhubung ke URL. Periksa URL dan coba lagi.'}, status=400)
    except http_requests.exceptions.HTTPError as e:
        return JsonResponse({'error': f'Server mengembalikan error: {e.response.status_code}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Gagal download video: {str(e)}'}, status=500)

    job_id = JobStore.create_job('heading', input_path, url_filename)
    return JsonResponse({'job_id': job_id, 'message': f'Video dari URL berhasil didownload ({downloaded / 1024 / 1024:.1f}MB)'})


@csrf_exempt
def process(request, job_id):
    """Proses video heading analysis."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    job = JobStore.get_job(job_id)
    if not job:
        return JsonResponse({'error': 'Job tidak ditemukan'}, status=400)

    if job.get('mode') != 'heading':
        return JsonResponse({'error': f"Mode salah: {job.get('mode')}"}, status=400)

    payload = get_json_data(request)
    footprint_id = payload.get('footprint_id')

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

    model_path = getattr(settings, 'ANALYSIS_MODEL_PATH', os.path.join(settings.BASE_DIR, 'static', 'models', 'best.pt'))
    if not os.path.exists(model_path):
        return JsonResponse({'error': f'Model tidak ditemukan: {model_path}'}, status=500)

    output_dir = os.path.join(getattr(settings, 'ANALYSIS_OUTPUT_FOLDER', os.path.join(settings.BASE_DIR, 'static', 'outputs')), 'heading')
    stub_dir = os.path.join(getattr(settings, 'ANALYSIS_STUBS_FOLDER', os.path.join(settings.BASE_DIR, 'static', 'stubs')), 'heading')
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(stub_dir, exist_ok=True)

    output_path = os.path.abspath(os.path.join(output_dir, f"{job_id}_heading_output.mp4"))
    stub_path = os.path.abspath(os.path.join(stub_dir, f"{job_id}_tracks.pkl"))

    input_path = job.get('input_path')
    if not input_path or not os.path.exists(input_path):
        return JsonResponse({'error': 'Input video tidak ditemukan'}, status=404)

    try:
        result = run_heading_pipeline(
            input_path=input_path,
            output_path=output_path,
            job_id=job_id,
            model_path=model_path,
            fps=30,
            use_stub=False,
            stub_path=stub_path
        )

        result['output_video'] = output_path
        JobStore.update_job(job_id, result)

        s3_url = None
        s3_url_before = None
        if result.get('status') != 'failed' and os.path.exists(output_path):
            try:
                s3_key = generate_s3_key('heading', job_id, os.path.basename(output_path))
                s3_url = upload_video_to_s3(output_path, s3_key)
                if s3_url:
                    result['s3_url'] = s3_url
            except Exception as s3_err:
                logger.error(f"S3 upload failed for job {job_id}: {s3_err}")

            try:
                if os.path.exists(input_path):
                    before_key = generate_s3_key('heading', job_id, f'before_{os.path.basename(input_path)}')
                    s3_url_before = upload_video_to_s3(input_path, before_key)
                    if s3_url_before:
                        result['s3_url_before'] = s3_url_before
            except Exception as s3_err:
                logger.error(f"S3 upload (before) failed for job {job_id}: {s3_err}")

        # Auto-save ke database total_result
        result_id = None
        stats = result.get('stats')
        if stats and result.get('status') != 'failed':
            try:
                if footprint_id:
                    fp_exists = Footprint.objects.filter(footprint=footprint_id).exists()
                    if not fp_exists:
                        try:
                            Footprint.objects.create(
                                footprint=footprint_id,
                                media=None,
                                training_id=footprint_id[:60],
                                category_id='heading',
                            )
                        except Exception as fp_create_err:
                            logger.error(f"Failed to create minimal footprint {footprint_id}: {fp_create_err}")

                total_h = stats.get('total_headings', 0)
                sukses = stats.get('successful_headings', 0)
                gagal = stats.get('failed_headings', 0)
                akurasi = TotalResult.calculate_accuracy(total_h, sukses)

                new_record = TotalResult.objects.create(
                    total_passing=total_h,
                    passing_sukses=sukses,
                    passing_gagal=gagal,
                    akurasi_passing=akurasi,
                    status='generated',
                    parent_id=None,
                    footprint_id=footprint_id
                )
                result_id = new_record.id

                # Update footprint media & media_after
                if footprint_id:
                    try:
                        fp_record = Footprint.objects.filter(footprint=footprint_id).first()
                        if fp_record:
                            fp_record.media_after = s3_url if s3_url else output_path
                            if s3_url_before:
                                fp_record.media = s3_url_before
                            elif os.path.exists(input_path):
                                fp_record.media = os.path.abspath(input_path)
                            fp_record.type = 'auto'
                            fp_record.save()
                    except Exception as fp_err:
                        logger.error(f"Failed to update footprint {footprint_id}: {fp_err}")

            except Exception as db_err:
                logger.error(f"Failed to save result to DB: {db_err}")

        response = dict(result)
        if result_id:
            response['result_id'] = str(result_id)
        return JsonResponse(response)

    except Exception as e:
        logger.error(f"[HEADING] EXCEPTION: {e}", exc_info=True)
        return JsonResponse({'error': str(e), 'status': 'failed'}, status=500)


def results(request, job_id):
    """Ambil status / hasil job heading."""
    job = JobStore.get_job(job_id)
    return JsonResponse(job) if job else JsonResponse({'error': 'Job not found'}, status=404)


def download(request, job_id):
    """Download video hasil heading."""
    job = JobStore.get_job(job_id)
    if not job or not job.get('output_video') or not os.path.exists(job['output_video']):
        return JsonResponse({'error': 'Video belum siap'}, status=404)
    return build_file_download_response(job['output_video'], f"heading_{job_id}.mp4")


def preview(request, job_id):
    """Stream video heading dengan Range Request support."""
    job = JobStore.get_job(job_id)
    if not job or not job.get('output_video') or not os.path.exists(job['output_video']):
        return JsonResponse({'error': 'Video belum siap'}, status=404)
    return build_video_stream_response(request, job['output_video'])
