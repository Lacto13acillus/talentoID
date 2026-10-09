import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from analysis.models import PlayerResult, TotalResult
from analysis.views.helpers import get_json_data

logger = logging.getLogger(__name__)


def list_results(request):
    """List semua player results."""
    results = PlayerResult.objects.all()
    return JsonResponse([r.to_dict() for r in results], safe=False)


def get_by_total_result(request, total_result_id):
    """Get semua player results berdasarkan total_result_id."""
    results = PlayerResult.objects.filter(total_result_id=total_result_id)
    return JsonResponse([r.to_dict() for r in results], safe=False)


def get_result(request, result_id):
    """Get single player result by ID."""
    result = PlayerResult.objects.filter(id=result_id).first()
    if not result:
        return JsonResponse({'error': 'Player result tidak ditemukan'}, status=404)
    return JsonResponse(result.to_dict())


@csrf_exempt
def edit_result(request, result_id):
    """Edit single player result."""
    if request.method not in ['PUT', 'POST']:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    original = PlayerResult.objects.filter(id=result_id).first()
    if not original:
        return JsonResponse({'error': 'Player result tidak ditemukan'}, status=404)

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

    akurasi = PlayerResult.calculate_accuracy(total_passing, passing_sukses)
    new_total_result_id = data.get('total_result_id', original.total_result_id)

    try:
        new_result = PlayerResult.objects.create(
            total_result_id=new_total_result_id,
            player=original.player,
            total_passing=total_passing,
            passing_sukses=passing_sukses,
            passing_gagal=passing_gagal,
            akurasi_passing=akurasi,
            status='edited',
            parent_id=parent_id,
            footprint_id=original.footprint_id
        )
        return JsonResponse({
            'message': 'Player result berhasil diedit',
            'original_id': str(result_id),
            'new_result': new_result.to_dict()
        }, status=201)
    except Exception as e:
        logger.error(f"[PLAYER_RESULT] Error: {e}")
        return JsonResponse({'error': f'Gagal menyimpan: {str(e)}'}, status=500)


@csrf_exempt
def batch_edit(request):
    """Batch edit multiple player results."""
    if request.method not in ['PUT', 'POST']:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    data = get_json_data(request)
    players_data = data.get('players', [])
    if not isinstance(players_data, list):
        return JsonResponse({'error': '"players" harus array'}, status=400)

    updated = []
    for item in players_data:
        pid = item.get('id')
        orig = PlayerResult.objects.filter(id=pid).first()
        if not orig:
            continue
        try:
            tp = int(item.get('total_passing', orig.total_passing or 0))
            ps = int(item.get('passing_sukses', orig.passing_sukses or 0))
            pg = int(item.get('passing_gagal', orig.passing_gagal or 0))
            parent_id = orig.parent_id if (orig.status == 'edited' and orig.parent_id) else str(orig.id)
            rec = PlayerResult.objects.create(
                total_result_id=orig.total_result_id,
                player=orig.player,
                total_passing=tp,
                passing_sukses=ps,
                passing_gagal=pg,
                akurasi_passing=PlayerResult.calculate_accuracy(tp, ps),
                status='edited',
                parent_id=parent_id,
                footprint_id=orig.footprint_id
            )
            updated.append(rec.to_dict())
        except Exception as e:
            logger.error(f"Error in batch_edit item {pid}: {e}")

    return JsonResponse({'message': f'{len(updated)} player results diedit', 'results': updated})


@csrf_exempt
def batch_save(request):
    """Batch save player results untuk total_result_id baru."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    data = get_json_data(request)
    total_result_id = data.get('total_result_id')
    players_data = data.get('players', [])

    if not total_result_id:
        return JsonResponse({'error': 'total_result_id wajib diisi'}, status=400)
    if not isinstance(players_data, list) or len(players_data) == 0:
        return JsonResponse({'error': '"players" harus berupa array dan tidak boleh kosong'}, status=400)

    try:
        total_rec = TotalResult.objects.filter(id=total_result_id).first()
        fallback_footprint = total_rec.footprint_id if total_rec else None

        created = []
        for p in players_data:
            player_name = p.get('player', '').strip()
            if not player_name:
                continue

            total_passing = int(p.get('total_passing', 0))
            passing_sukses = int(p.get('passing_sukses', 0))
            passing_gagal = int(p.get('passing_gagal', 0))
            akurasi = PlayerResult.calculate_accuracy(total_passing, passing_sukses)

            record = PlayerResult.objects.create(
                total_result_id=total_result_id,
                player=player_name,
                total_passing=total_passing,
                passing_sukses=passing_sukses,
                passing_gagal=passing_gagal,
                akurasi_passing=akurasi,
                status='generated',
                footprint_id=fallback_footprint
            )
            created.append(record.to_dict())

        return JsonResponse({
            'message': f'{len(created)} player results berhasil dibuat',
            'results': created
        }, status=201)
    except Exception as e:
        logger.error(f"[PLAYER_RESULT] Batch save error: {e}")
        return JsonResponse({'error': f'Gagal batch save: {str(e)}'}, status=500)
