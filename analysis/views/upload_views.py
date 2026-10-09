import os
import uuid
from datetime import datetime
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@csrf_exempt
def upload_video(request):
    """Upload video umum untuk diproses."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    if 'video' not in request.FILES:
        return JsonResponse({'error': 'No video file provided'}, status=400)

    file = request.FILES['video']
    if file.name == '':
        return JsonResponse({'error': 'No file selected'}, status=400)

    if not allowed_file(file.name):
        return JsonResponse({'error': f'File type not allowed. Allowed: {list(ALLOWED_EXTENSIONS)}'}, status=400)

    ext = file.name.rsplit('.', 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    upload_dir = getattr(settings, 'ANALYSIS_UPLOAD_FOLDER', os.path.join(settings.BASE_DIR, 'static', 'uploads'))
    os.makedirs(upload_dir, exist_ok=True)
    filepath = os.path.join(upload_dir, filename)

    with open(filepath, 'wb+') as dest:
        for chunk in file.chunks():
            dest.write(chunk)

    job_id = uuid.uuid4().hex[:8]
    return JsonResponse({
        'job_id': job_id,
        'filename': file.name,
        'filepath': filepath,
        'uploaded_at': datetime.utcnow().isoformat(),
        'message': 'Video uploaded successfully. Use job_id to trigger processing.'
    }, status=201)
