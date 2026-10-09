import os
import uuid
import logging
import threading
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from analysis.models import TotalResult, PlayerResult
from footprint.models import footprint as Footprint
from analysis.views.helpers import get_json_data

logger = logging.getLogger(__name__)

_upload_jobs = {}


def auth_status(request):
    """Check if YouTube OAuth2 is authenticated."""
    try:
        from analysis.services.youtube_service import get_auth_status
        status = get_auth_status()
        resp = JsonResponse(status)
        resp['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        return resp
    except Exception as e:
        logger.error(f"[YOUTUBE] Error checking auth status: {e}")
        return JsonResponse({'authenticated': False, 'message': f'Error: {str(e)}'}, status=500)


@csrf_exempt
def trigger_auth(request):
    """Redirect user ke Google OAuth2 login page."""
    try:
        from analysis.services.youtube_service import create_auth_url
        result = create_auth_url()
        if request.method == 'GET':
            return HttpResponseRedirect(result['auth_url'])
        return JsonResponse({
            'success': True,
            'auth_url': result['auth_url'],
            'message': 'Redirect ke auth_url untuk login Google.'
        })
    except Exception as e:
        logger.error(f"[YOUTUBE] Auth error: {e}")
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


def oauth2_callback(request):
    """Handle Google OAuth2 redirect callback."""
    code = request.GET.get('code')
    state = request.GET.get('state')
    error = request.GET.get('error')

    if error:
        return HttpResponse(f"<h2>Login YouTube Gagal</h2><p>Error: {error}</p><a href='/history'>Kembali</a>", status=400)
    if not code:
        return HttpResponse("<h2>Authorization code tidak ditemukan</h2><a href='/history'>Kembali</a>", status=400)

    try:
        from analysis.services.youtube_service import exchange_auth_code
        creds = exchange_auth_code(code, state=state)
        if creds and creds.valid:
            html = """
            <html><head><title>YouTube Login Berhasil</title><meta http-equiv="refresh" content="2;url=/history"></head>
            <body style="font-family:sans-serif;text-align:center;padding:3rem;background:#0e1319;color:#e2e8f0">
                <h2 style="color:#00e676">Berhasil Login ke YouTube!</h2>
                <p>Redirect ke History dalam 2 detik...</p>
                <a href="/history" style="color:#00e676">Kembali ke History</a>
            </body></html>
            """
            return HttpResponse(html)
        else:
            return HttpResponse("<h2>Gagal mendapatkan token yang valid</h2><a href='/history'>Kembali</a>", status=400)
    except Exception as e:
        logger.error(f"[YOUTUBE] OAuth2 callback error: {e}", exc_info=True)
        return HttpResponse(f"<h2>Error exchange auth code</h2><p>{str(e)}</p><a href='/history'>Kembali</a>", status=500)


@csrf_exempt
def auth_callback_manual(request):
    data = get_json_data(request)
    code = data.get('code', '').strip()
    if not code:
        return JsonResponse({'success': False, 'message': 'Parameter "code" wajib diisi.'}, status=400)

    try:
        from analysis.services.youtube_service import exchange_auth_code
        creds = exchange_auth_code(code)
        if creds and creds.valid:
            return JsonResponse({'success': True, 'message': 'Berhasil login ke YouTube!'})
        return JsonResponse({'success': False, 'message': 'Token tidak valid'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


def _resolve_video_path(job_id, media_url, label='video'):
    temp_file = None
    video_path = None
    is_http = media_url.startswith(('http://', 'https://'))

    if is_http:
        import tempfile
        import requests as http_req
        from analysis.services.s3_service import get_s3_client, S3_BUCKET_NAME, S3_ENDPOINT_URL
        prefix = f"{S3_ENDPOINT_URL}/{S3_BUCKET_NAME}/"
        if media_url.startswith(prefix):
            s3_key = media_url[len(prefix):]
            s3_client = get_s3_client()
            temp_file = tempfile.NamedTemporaryFile(suffix='.mp4', prefix=f'yt_{label}_', delete=False)
            s3_client.download_fileobj(S3_BUCKET_NAME, s3_key, temp_file)
            temp_file.close()
            video_path = temp_file.name
        else:
            try:
                resp = http_req.get(media_url, stream=True, timeout=60, headers={'User-Agent': 'Mozilla/5.0'})
                resp.raise_for_status()
                temp_file = tempfile.NamedTemporaryFile(suffix='.mp4', prefix=f'yt_{label}_', delete=False)
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        temp_file.write(chunk)
                temp_file.close()
                video_path = temp_file.name
            except Exception as e:
                logger.error(f"[YOUTUBE] HTTP download error: {e}")
                if temp_file:
                    try:
                        temp_file.close()
                        os.unlink(temp_file.name)
                    except Exception:
                        pass
                return None, None
    else:
        media_path = media_url.replace('\\', '/')
        if not os.path.isabs(media_path):
            idx = media_path.find('static/')
            if idx != -1:
                media_path = media_path[idx:]
            video_path = os.path.abspath(media_path)
        else:
            video_path = media_path

    return video_path, temp_file


def _do_upload_job(job_id, footprint_id, media_after, title, description, privacy, media_before=None, title_before=None):
    temp_after = None
    temp_before = None
    try:
        from analysis.services.youtube_service import upload_to_youtube
        _upload_jobs[job_id]['status'] = 'downloading'
        _upload_jobs[job_id]['message'] = 'Menyiapkan video hasil counting...'

        video_after_path, temp_after = _resolve_video_path(job_id, media_after, label='after')
        if not video_after_path or not os.path.exists(video_after_path):
            _upload_jobs[job_id]['status'] = 'error'
            _upload_jobs[job_id]['error'] = f'File video after tidak ditemukan: {video_after_path}'
            return

        _upload_jobs[job_id]['status'] = 'uploading'
        _upload_jobs[job_id]['message'] = 'Mengupload video hasil counting ke YouTube...'
        result_after = upload_to_youtube(video_path=video_after_path, title=title, description=description, privacy=privacy)

        result_before = None
        if media_before:
            _upload_jobs[job_id]['status'] = 'uploading_before'
            _upload_jobs[job_id]['message'] = 'Mengupload video original ke YouTube...'
            video_before_path, temp_before = _resolve_video_path(job_id, media_before, label='before')
            if video_before_path and os.path.exists(video_before_path):
                result_before = upload_to_youtube(
                    video_path=video_before_path,
                    title=title_before or (title + ' — Before Counting'),
                    description=description,
                    privacy=privacy,
                )

        _upload_jobs[job_id]['status'] = 'done'
        _upload_jobs[job_id]['result'] = {
            'youtube_url': result_after['youtube_url'],
            'video_id': result_after['video_id'],
            'title': result_after['title'],
            'privacy': result_after['privacy'],
            'youtube_url_after': result_after['youtube_url'],
            'youtube_url_before': result_before['youtube_url'] if result_before else None,
            'has_before': result_before is not None,
        }
        _upload_jobs[job_id]['message'] = 'Upload selesai!'
    except Exception as e:
        logger.error(f"[YOUTUBE] Upload worker error: {e}", exc_info=True)
        _upload_jobs[job_id]['status'] = 'error'
        _upload_jobs[job_id]['error'] = str(e)
    finally:
        for tf in [temp_after, temp_before]:
            if tf:
                try:
                    os.unlink(tf.name)
                except Exception:
                    pass


def _build_title(fp, latest):
    parts = []
    category = fp.category_id or ''
    if category:
        parts.append(category.capitalize())
    parts.append('Training Analysis')
    if latest and latest.created_at:
        parts.append(f'— {latest.created_at.strftime("%d %b %Y")}')
    title = ' '.join(parts)
    return title if len(title) <= 100 else title[:97] + '...'


def _build_description(fp, latest, player_results):
    lines = ['Football Training Analysis — Video Hasil Counting', '', 'Statistik Analisis:']
    if latest:
        lines.extend([
            f'  • Total Passing: {latest.total_passing or 0}',
            f'  • Passing Sukses: {latest.passing_sukses or 0}',
            f'  • Passing Gagal: {latest.passing_gagal or 0}',
            f'  • Akurasi: {latest.akurasi_passing or "0%"}',
            '',
        ])
    if player_results:
        lines.append('Statistik Per Pemain:')
        for pr in player_results:
            lines.append(f'  • {pr.player or "Unknown"}: {pr.passing_sukses or 0}/{pr.total_passing or 0} ({pr.akurasi_passing or "0%"})')
        lines.append('')
    lines.extend([
        f'Kategori: {fp.category_id or "-"}',
        f'Footprint: {fp.footprint}',
        '',
        'Powered by Football Training Analytics',
    ])
    return '\n'.join(lines)


@csrf_exempt
def upload_video(request):
    """Start async YouTube upload."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    data = get_json_data(request)
    footprint_id = data.get('footprint_id', '').strip()
    if not footprint_id:
        return JsonResponse({'error': 'footprint_id wajib diisi'}, status=400)

    try:
        fp = Footprint.objects.filter(footprint=footprint_id).first()
        if not fp:
            return JsonResponse({'error': f'Footprint {footprint_id} tidak ditemukan'}, status=404)

        if not getattr(fp, 'media_after', None):
            return JsonResponse({'error': 'Video hasil analisis belum tersedia untuk footprint ini'}, status=404)

        latest = TotalResult.objects.filter(footprint_id=footprint_id).order_by('-created_at').first()
        player_results = PlayerResult.objects.filter(total_result=latest) if latest else []

        custom_title = data.get('title', '').strip()
        custom_desc = data.get('description', '').strip()
        privacy = data.get('privacy', '').strip() or 'unlisted'

        title = custom_title or _build_title(fp, latest)
        description = custom_desc or _build_description(fp, latest, player_results)

        is_by_admin = (getattr(fp, 'type', '') or '').strip().lower() == 'by admin'
        media_before = None
        title_before = None
        if not is_by_admin and fp.media and fp.media.strip():
            media_before = fp.media.strip()
            title_before = (title + ' — Before Counting')[:100]

        job_id = str(uuid.uuid4())[:8]
        _upload_jobs[job_id] = {
            'status': 'queued',
            'message': 'Memulai upload...',
            'result': None,
            'error': None,
            'footprint_id': footprint_id,
            'title': title,
            'is_by_admin': is_by_admin,
        }

        threading.Thread(
            target=_do_upload_job,
            args=(job_id, footprint_id, fp.media_after, title, description, privacy),
            kwargs={'media_before': media_before, 'title_before': title_before},
            daemon=True
        ).start()

        return JsonResponse({
            'success': True,
            'job_id': job_id,
            'is_by_admin': is_by_admin,
            'has_before': media_before is not None,
            'message': 'Upload dimulai di background.'
        })
    except Exception as e:
        logger.error(f"[YOUTUBE] Upload start error: {e}", exc_info=True)
        return JsonResponse({'error': f'Gagal memulai upload: {str(e)}'}, status=500)


def upload_status(request, job_id):
    """Poll status upload YouTube."""
    job = _upload_jobs.get(job_id)
    if not job:
        return JsonResponse({'error': f'Job {job_id} tidak ditemukan'}, status=404)

    resp_data = {
        'job_id': job_id,
        'status': job['status'],
        'message': job.get('message', ''),
    }
    if job['status'] == 'done' and job.get('result'):
        resp_data['result'] = job['result']
    if job['status'] == 'error':
        resp_data['error'] = job.get('error', 'Unknown error')

    resp = JsonResponse(resp_data)
    resp['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return resp
