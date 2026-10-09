import os
import json
import logging
from django.http import JsonResponse, StreamingHttpResponse, FileResponse

logger = logging.getLogger(__name__)

MAX_VIDEO_SIZE_MB = int(os.getenv('MAX_VIDEO_SIZE_MB', '500'))


def get_json_data(request):
    """Safely get JSON body from Django HttpRequest."""
    if hasattr(request, '_parsed_json'):
        return request._parsed_json
    try:
        if request.body:
            request._parsed_json = json.loads(request.body.decode('utf-8'))
            return request._parsed_json
    except Exception as e:
        logger.warning(f"Failed to parse JSON body: {e}")
    return {}


def build_video_stream_response(request, path):
    """Build a StreamingHttpResponse with HTTP Range Request support."""
    if not os.path.exists(path):
        return JsonResponse({'error': 'Video tidak ditemukan'}, status=404)

    file_size = os.path.getsize(path)
    range_header = request.META.get('HTTP_RANGE')

    if range_header:
        try:
            byte_range = range_header.replace('bytes=', '').split('-')
            start = int(byte_range[0]) if byte_range[0] else 0
            end = int(byte_range[1]) if len(byte_range) > 1 and byte_range[1] else file_size - 1
        except (ValueError, IndexError):
            start, end = 0, file_size - 1
        end = min(end, file_size - 1)
        chunk_size = end - start + 1

        def generate_partial():
            with open(path, 'rb') as f:
                f.seek(start)
                remaining = chunk_size
                while remaining > 0:
                    data = f.read(min(remaining, 65536))
                    if not data:
                        break
                    remaining -= len(data)
                    yield data

        response = StreamingHttpResponse(generate_partial(), status=206, content_type='video/mp4')
        response['Content-Range'] = f'bytes {start}-{end}/{file_size}'
        response['Accept-Ranges'] = 'bytes'
        response['Content-Length'] = str(chunk_size)
        response['Cache-Control'] = 'no-cache'
        return response

    def generate_full():
        with open(path, 'rb') as f:
            while True:
                data = f.read(65536)
                if not data:
                    break
                yield data

    response = StreamingHttpResponse(generate_full(), content_type='video/mp4')
    response['Content-Length'] = str(file_size)
    response['Accept-Ranges'] = 'bytes'
    response['Cache-Control'] = 'no-cache'
    return response


def build_file_download_response(path, filename):
    """Return a FileResponse attachment."""
    if not os.path.exists(path):
        return JsonResponse({'error': 'File tidak ditemukan'}, status=404)
    response = FileResponse(open(path, 'rb'), as_attachment=True, filename=filename)
    response['Content-Type'] = 'video/mp4'
    return response
