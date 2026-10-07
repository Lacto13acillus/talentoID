import os
import requests
from datetime import datetime
from integration.models import PlayerIntegration, ActivityLog
from player.models import player
from django.utils.timezone import make_aware

WHOOP_CLIENT_ID = os.getenv('WHOOP_CLIENT_ID')
WHOOP_CLIENT_SECRET = os.getenv('WHOOP_CLIENT_SECRET')
# If hosting, change this to the proper callback url
REDIRECT_URI = 'https://ai.tail1d2207.ts.net:5000/api/whoop/callback'

def get_whoop_auth_url(athlete_id):
    """Generate WHOOP OAuth URL"""
    scopes = "offline read:recovery read:sleep read:workout read:cycles read:profile"
    return (f"https://api.prod.whoop.com/oauth/oauth2/auth"
            f"?response_type=code"
            f"&client_id={WHOOP_CLIENT_ID}"
            f"&redirect_uri={REDIRECT_URI}"
            f"&scope={scopes}"
            f"&state={athlete_id}")

def exchange_whoop_token(code, athlete_id):
    """Exchange auth code for access token"""
    if not WHOOP_CLIENT_ID or not WHOOP_CLIENT_SECRET:
        return False, "WHOOP credentials not configured in .env"

    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': WHOOP_CLIENT_ID,
        'client_secret': WHOOP_CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI
    }
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        response = requests.post("https://api.prod.whoop.com/oauth/oauth2/token", data=payload, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        access_token = data.get('access_token')
        refresh_token = data.get('refresh_token')
        
        p = player.objects.filter(player=athlete_id).first()
        if p:
            integration, _ = PlayerIntegration.objects.get_or_create(player=p)
            integration.whoop_access_token = access_token
            integration.whoop_refresh_token = refresh_token
            integration.save()
            return True, "WHOOP connected successfully"
        return False, "Athlete not found"
    except Exception as e:
        print(f"WHOOP Token Error: {e}")
        if 'response' in locals() and hasattr(response, 'text'):
            print(f"WHOOP API Response: {response.text}")
        return False, str(e)

def sync_whoop_data(athlete_id):
    """Fetch WHOOP workouts and recovery"""
    p = player.objects.filter(player=athlete_id).first()
    if not p:
        return False, "Athlete not found"
        
    integration = getattr(p, 'integration', None)
    if not integration or not integration.whoop_access_token:
        return False, "WHOOP not connected for this athlete"

    headers = {
        'Authorization': f'Bearer {integration.whoop_access_token}'
    }

    try:
        # Fetch Workouts
        workout_resp = requests.get("https://api.prod.whoop.com/developer/v1/activity/workout", headers=headers)
        workout_resp.raise_for_status()
        workouts = workout_resp.json().get('records', [])
        
        synced_count = 0
        for w in workouts:
            external_id = str(w.get('id'))
            
            # Cek apakah sudah ada
            existing = ActivityLog.objects.filter(source='whoop', external_id=external_id).first()
            if existing:
                continue
                
            sport = "WHOOP Sport ID: " + str(w.get('sport_id', 'Unknown'))
            score = w.get('score', {})
            distance = w.get('distance_meter', 0)
            
            # Start time formatting
            start_str = w.get('start', '')
            try:
                dt = datetime.strptime(start_str[:19], "%Y-%m-%dT%H:%M:%S")
                dt = make_aware(dt)
            except:
                dt = make_aware(datetime.now())

            # Create activity
            ActivityLog.objects.create(
                player=p,
                source='whoop',
                external_id=external_id,
                name=f"WHOOP Workout",
                sport_type=sport,
                start_time=dt,
                duration=score.get('millisecond', 0) / 1000,
                distance=distance,
                calories=score.get('kilojoule', 0) * 0.239006 * 1000,
                avg_hr=score.get('average_heart_rate', 0),
                max_hr=score.get('max_heart_rate', 0),
                raw_payload=w
            )
            synced_count += 1
            
        return True, f"Successfully synced {synced_count} WHOOP workouts"
    except Exception as e:
        print(f"WHOOP Sync Error: {e}")
        if 'workout_resp' in locals() and hasattr(workout_resp, 'text'):
            print(f"WHOOP API Response: {workout_resp.text}")
        return False, str(e)
