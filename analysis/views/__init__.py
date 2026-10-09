import os
import json
import logging
import uuid as uuid_lib
import threading
import requests as http_requests
from django.conf import settings
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from analysis.job_store import JobStore
from analysis.models import TotalResult, PlayerResult
from footprint.models import footprint as Footprint

logger = logging.getLogger(__name__)

MAX_VIDEO_SIZE_MB = int(os.getenv('MAX_VIDEO_SIZE_MB', '500'))


# ==============================================================
# Helper: Video stream with Range Request
# ==============================================================
def _stream_video_response(path):
    """Return a StreamingHttpResponse with Range Request support."""
    from django.http import HttpRequest
    # This is called within a view that has the request
    # We handle it differently - caller passes range_header
    pass


def _build_video_response(request, path):
    """Build a streaming response supporting HTTP Range requests."""
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
