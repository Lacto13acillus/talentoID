import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from analysis.models import TotalResult
from analysis.views.helpers import get_json_data

logger = logging.getLogger(__name__)


def list_results(request):
    """List semua results, newest first."""
    results = TotalResult.objects.all().order_by('-created_at')
    return JsonResponse([r.to_dict() for r in results], safe=False)


def get_result(request, result_id):
    """Get single result by ID."""
    result = TotalResult.objects.filter(id=result_id).first()
    if not result:
        return JsonResponse({'error': 'Result tidak ditemukan'}, status=404)
    return JsonResponse(result.to_dict())


def get_history(request, result_id):
    """Get edit history: record original + semua edits."""
    original = TotalResult.objects.filter(id=result_id).first()
    if not original:
        return JsonResponse({'error': 'Result tidak ditemukan'}, status=404)

    if original.status == 'edited' and original.parent_id:
        root_id = original.parent_id
    else:
        root_id = original.id

    root = TotalResult.objects.filter(id=root_id).first()
    edits = TotalResult.objects.filter(parent_id=root_id).order_by('-created_at')

    history = {
        'original': root.to_dict() if root else None,
        'edits': [e.to_dict() for e in edits],
        'total_versions': 1 + len(edits)
    }
    return JsonResponse(history)


@csrf_exempt
def edit_result(request, result_id):
    """Edit result — membuat record BARU dengan status 'edited'."""
    if request.method not in ['PUT', 'POST']:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    original = TotalResult.objects.filter(id=result_id).first()
    if not original:
        return JsonResponse({'error': 'Result tidak ditemukan'}, status=404)

    data = get_json_data(request)
    total_passing = data.get('total_passing')
    passing_sukses = data.get('passing_sukses')
    passing_gagal = data.get('passing_gagal')

    if total_passing is None or passing_sukses is None or passing_gagal is None:
        return JsonResponse({'error': 'Field total_passing, passing_sukses, passing_gagal wajib diisi'}, status=400)

    try:
        total_passing = int(total_passing)
        passing_sukses = int(passing_sukses)
        passing_gagal = int(passing_gagal)
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Semua field harus berupa angka integer'}, status=400)

    if total_passing < 0 or passing_sukses < 0 or passing_gagal < 0:
        return JsonResponse({'error': 'Nilai tidak boleh negatif'}, status=400)

    if original.status == 'edited' and original.parent_id:
        parent_id = original.parent_id
    else:
        parent_id = str(original.id)

    akurasi = TotalResult.calculate_accuracy(total_passing, passing_sukses)

    try:
        new_result = TotalResult.objects.create(
            total_passing=total_passing,
            passing_sukses=passing_sukses,
            passing_gagal=passing_gagal,
            akurasi_passing=akurasi,
            status='edited',
            parent_id=parent_id,
            footprint_id=original.footprint_id
        )
        return JsonResponse({
            'message': 'Result berhasil diedit',
            'original_id': result_id,
            'new_result': new_result.to_dict()
        }, status=201)
    except Exception as e:
        logger.error(f"[TOTAL_RESULT] Error: {e}")
        return JsonResponse({'error': f'Gagal menyimpan: {str(e)}'}, status=500)
