import os
import hmac
import hashlib
from datetime import datetime
from integration.models import PlayerIntegration, ActivityLog
from player.models import player
from django.utils.timezone import make_aware

try:
    from terra.base_client import Terra
except ImportError:
    Terra = None

TERRA_API_KEY = os.getenv('TERRA_API_KEY')
TERRA_DEV_ID = os.getenv('TERRA_DEV_ID')
TERRA_WEBHOOK_SECRET = os.getenv('TERRA_WEBHOOK_SECRET')

terra_client = None
if TERRA_API_KEY and TERRA_DEV_ID and TERRA_WEBHOOK_SECRET and Terra:
    terra_client = Terra(api_key=TERRA_API_KEY, dev_id=TERRA_DEV_ID, secret=TERRA_WEBHOOK_SECRET)

def get_terra_widget_url(athlete_id):
    """Generate Terra Widget Session URL"""
    if not terra_client:
        return None, "Terra API is not configured properly (Missing Keys or terra-python not installed)."
        
    try:
        response = terra_client.generate_widget_session(
            reference_id=str(athlete_id),
            providers=["GARMIN", "FITBIT", "OURA", "APPLE", "SAMSUNG", "WITHINGS", "POLAR"],
            language="en"
        )
        # Handle terra-python response
        if hasattr(response, 'url'):
            return response.url, None
        elif isinstance(response, dict) and 'url' in response:
            return response['url'], None
        elif hasattr(response, 'get_parsed_response'):
            data = response.get_parsed_response()
            return data.get('url'), None
        else:
            return None, "Failed to parse Terra response."
    except Exception as e:
        return None, str(e)

def verify_terra_signature(payload_str, signature):
    """Verify the terra webhook signature"""
    if not TERRA_WEBHOOK_SECRET:
        return False
        
    try:
        parts = signature.split(',')
        timestamp = parts[0].split('=')[1]
        sig_v1 = parts[1].split('=')[1]
        
        message = timestamp + "." + payload_str
        expected_sig = hmac.new(
            TERRA_WEBHOOK_SECRET.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(expected_sig, sig_v1)
    except Exception:
        return False

def process_terra_webhook(payload):
    """Process incoming data from Terra Webhook"""
    event_type = payload.get('type')
    
    if event_type == 'auth_success':
        user = payload.get('user', {})
        reference_id = user.get('reference_id') # This is our athlete_id
        terra_user_id = user.get('user_id')
        
        if reference_id and terra_user_id:
            p = player.objects.filter(player=reference_id).first()
            if p:
                integration, _ = PlayerIntegration.objects.get_or_create(player=p)
                integration.terra_user_id = terra_user_id
                integration.save()
                
    elif event_type == 'activity':
        data_arr = payload.get('data', [])
        for act in data_arr:
            terra_user_id = act.get('user', {}).get('user_id')
            integration = PlayerIntegration.objects.filter(terra_user_id=terra_user_id).first()
            if not integration:
                continue
            
            p = integration.player
            external_id = str(act.get('metadata', {}).get('summary_id', ''))
            existing = ActivityLog.objects.filter(player=p, source='terra', external_id=external_id).first()
            
            if not existing:
                try:
                    start_time = datetime.fromisoformat(act.get('metadata', {}).get('start_time', '').replace('Z', '+00:00'))
                    if start_time.tzinfo is None:
                        start_time = make_aware(start_time)
                except:
                    start_time = make_aware(datetime.utcnow())
                    
                distance = act.get('distance_data', {}).get('summary', {}).get('distance_meters')
                duration = act.get('active_durations_data', {}).get('activity_seconds')
                avg_hr = act.get('heart_rate_data', {}).get('summary', {}).get('avg_hr_bpm')
                sport_type = act.get('metadata', {}).get('type')
                
                ActivityLog.objects.create(
                    player=p,
                    source='terra',
                    external_id=external_id,
                    name=act.get('metadata', {}).get('name', 'Terra Activity'),
                    sport_type=sport_type,
                    start_time=start_time,
                    duration=duration,
                    distance=distance,
                    avg_hr=avg_hr,
                    raw_payload=act
                )
