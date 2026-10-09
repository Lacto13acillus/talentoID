import os
import logging
import requests as http_requests
from django.http import JsonResponse
from analysis.models import TotalResult, PlayerResult
from footprint.models import footprint as Footprint

logger = logging.getLogger(__name__)

CHAMPION_API_URL = os.getenv(
    'CHAMPION_API_URL',
    'https://api.champion.realdataid.live/app/v2/activity/footprint'
)
CHAMPION_API_TOKEN = os.getenv('CHAMPION_API_TOKEN', '')
CHAMPION_BASE = 'https://api.champion.realdataid.live'
CHAMPION_API_ENABLED = False


def get_results_by_footprint(request, footprint_id=None):
    """Get counting results for a specific footprint_id."""
    if not footprint_id:
        footprint_id = request.GET.get('footprint_id', '').strip()

    if not footprint_id:
        return JsonResponse({'error': 'footprint_id wajib diisi'}, status=400)

    try:
        fp = Footprint.objects.filter(footprint=footprint_id).first()
        footprint_info = None
        if fp:
            footprint_info = {
                'footprint': fp.footprint,
                'media': str(fp.media) if fp.media else None,
                'media_after': str(fp.media_after) if getattr(fp, 'media_after', None) else None,
                'type': getattr(fp, 'type', None),
                'category_id': fp.category_id,
                'training_id': fp.training_id,
            }

        total_results = TotalResult.objects.filter(
            footprint_id=footprint_id
        ).order_by('-created_at')

        results = []
        for tr in total_results:
            tr_dict = tr.to_dict()
            player_results = PlayerResult.objects.filter(total_result=tr)
            tr_dict['player_results'] = [pr.to_dict() for pr in player_results]
            results.append(tr_dict)

        return JsonResponse({
            'footprint': footprint_info,
            'results': results,
            'total_count': len(results)
        })

    except Exception as e:
        logger.error(f"[HISTORY] Error fetching results: {e}")
        return JsonResponse({'error': str(e)}, status=500)


def get_summary(request):
    """Get summary of all counted footprints with their latest results."""
    try:
        counted_fps = TotalResult.objects.exclude(
            footprint__isnull=True
        ).values_list('footprint_id', flat=True).distinct()

        summaries = []
        for fp_id in counted_fps:
            fp = Footprint.objects.filter(footprint=fp_id).first()
            latest = TotalResult.objects.filter(
                footprint_id=fp_id
            ).order_by('-created_at').first()

            if latest:
                fp_info = {
                    'footprint': fp.footprint if fp else fp_id,
                    'media': str(fp.media) if fp and fp.media else None,
                    'media_after': str(fp.media_after) if fp and getattr(fp, 'media_after', None) else None,
                    'type': getattr(fp, 'type', None) if fp else None,
                    'category_id': fp.category_id if fp else None,
                }
                summaries.append({
                    'footprint': fp_info,
                    'latest_result': latest.to_dict()
                })

        return JsonResponse({
            'summaries': summaries,
            'total': len(summaries)
        })

    except Exception as e:
        logger.error(f"[HISTORY] Error fetching summary: {e}")
        return JsonResponse({'error': str(e)}, status=500)


def get_table_data(request):
    """Get flat table data for history dashboard."""
    try:
        counted_fps = TotalResult.objects.exclude(
            footprint__isnull=True
        ).values_list('footprint_id', flat=True).distinct()
        counted_ids = set(counted_fps)

        if not counted_ids:
            return JsonResponse({'rows': [], 'filters': {'clubs': [], 'trainings': [], 'categories': []}})

        champion_map = {}
        if CHAMPION_API_ENABLED:
            headers = {'User-Agent': 'Football-Analysis-API/1.0', 'Accept': 'application/json'}
            if CHAMPION_API_TOKEN:
                headers['Authorization'] = f'Bearer {CHAMPION_API_TOKEN}'
            try:
                resp = http_requests.get(CHAMPION_API_URL, headers=headers, timeout=15)
                if resp.ok:
                    api_data = resp.json().get('data', [])
                    for item in api_data:
                        fid = item.get('footprint')
                        if fid:
                            champion_map[str(fid)] = item
            except Exception as api_err:
                logger.warning(f"[HISTORY/TABLE] Champion API error: {api_err}")

        rows = []
        clubs_set = set()
        trainings_set = set()
        categories_set = set()

        for fp_id in counted_ids:
            fp = Footprint.objects.filter(footprint=fp_id).first()
            latest = TotalResult.objects.filter(
                footprint_id=fp_id
            ).order_by('-created_at').first()

            if not latest:
                continue

            player_results = PlayerResult.objects.filter(total_result=latest)

            champ = champion_map.get(str(fp_id), {})
            training_obj = champ.get('training') or {}
            team_obj = training_obj.get('team') or {}

            club_name = team_obj.get('nama_team', '')
            club_category = team_obj.get('kategori_team', '')
            club_logo = team_obj.get('logo_team', '')
            if club_logo:
                club_logo = f"{CHAMPION_BASE}{club_logo}"

            training_name = training_obj.get('nama_latihan', '')
            training_date = (training_obj.get('schedule') or {}).get('tanggal', '')
            category = champ.get('category') or (fp.category_id if fp else '') or ''

            media_after = None
            if fp and getattr(fp, 'media_after', None):
                ma = str(fp.media_after)
                if ma.startswith(('http://', 'https://')):
                    media_after = ma
                else:
                    ma = ma.replace('\\', '/')
                    idx = ma.find('static/')
                    if idx != -1:
                        ma = ma[idx:]
                    media_after = '/' + ma

            media_before = None
            if fp and fp.media:
                mb = str(fp.media)
                if mb.startswith(('http://', 'https://')):
                    media_before = mb
                else:
                    mb = mb.replace('\\', '/')
                    idx = mb.find('static/')
                    if idx != -1:
                        mb = mb[idx:]
                    media_before = '/' + mb

            row = {
                'footprint_id': str(fp_id),
                'club_name': club_name,
                'club_category': club_category,
                'club_logo': club_logo,
                'training_name': training_name,
                'training_date': training_date,
                'category': category,
                'total_passing': latest.total_passing or 0,
                'passing_sukses': latest.passing_sukses or 0,
                'passing_gagal': latest.passing_gagal or 0,
                'akurasi_passing': latest.akurasi_passing or '0%',
                'status': latest.status or 'generated',
                'analyzed_at': latest.created_at.isoformat() if latest.created_at else None,
                'media': media_before,
                'media_after': media_after,
                'player_results': [pr.to_dict() for pr in player_results],
                'type': getattr(fp, 'type', None) if fp else None,
            }
            rows.append(row)

            if club_name:
                clubs_set.add(club_name)
            if training_name:
                trainings_set.add(training_name)
            if category:
                categories_set.add(category)

        rows.sort(key=lambda r: r['analyzed_at'] or '', reverse=True)

        return JsonResponse({
            'rows': rows,
            'total': len(rows),
            'filters': {
                'clubs': sorted(clubs_set),
                'trainings': sorted(trainings_set),
                'categories': sorted(categories_set),
            }
        })

    except Exception as e:
        logger.error(f"[HISTORY] Error fetching table data: {e}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)
