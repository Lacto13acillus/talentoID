import os
import logging
from django.http import JsonResponse
from footprint.models import footprint as Footprint
from analysis.models import TotalResult

logger = logging.getLogger(__name__)

CHAMPION_API_ENABLED = False


def get_footprints(request):
    """Fetch footprint data from local DB or external API."""
    try:
        footprints = Footprint.objects.all()
        data_list = []
        for fp in footprints:
            data_list.append({
                'footprint': fp.footprint,
                'media': str(fp.media) if fp.media else None,
                'media_after': str(fp.media_after) if getattr(fp, 'media_after', None) else None,
                'type': getattr(fp, 'type', None),
                'training_id': fp.training_id,
                'category_id': fp.category_id,
                'created_at': fp.created_at.isoformat() if hasattr(fp, 'created_at') and fp.created_at else None,
                'updated_at': fp.updated_at.isoformat() if hasattr(fp, 'updated_at') and fp.updated_at else None,
            })
        return JsonResponse({'data': data_list, 'source': 'local_db'})
    except Exception as e:
        logger.error(f"[FOOTPRINT] Error: {e}")
        return JsonResponse({'error': str(e)}, status=500)


def get_counted_footprints(request):
    """Return list of footprint IDs that have generated TotalResult."""
    try:
        counted = TotalResult.objects.filter(
            footprint__isnull=False,
            status='generated'
        ).values_list('footprint_id', flat=True).distinct()
        counted_ids = [str(x) for x in counted]
        return JsonResponse({'counted': counted_ids})
    except Exception as e:
        logger.error(f"[FOOTPRINT] Error getting counted: {e}")
        return JsonResponse({'error': str(e)}, status=500)
