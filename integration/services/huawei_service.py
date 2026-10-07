import os
import requests
import json
from datetime import datetime
from integration.models import PlayerIntegration, ActivityLog
from player.models import player
from urllib.parse import urlencode
from django.utils.timezone import make_aware

HUAWEI_CLIENT_ID = os.getenv('HUAWEI_CLIENT_ID')
HUAWEI_CLIENT_SECRET = os.getenv('HUAWEI_CLIENT_SECRET')
REDIRECT_URI = 'http://100.102.192.86:5000/api/huawei/callback'

def get_huawei_auth_url(athlete_id):
    """Generate Huawei OAuth URL"""
    scopes = "https://www.huawei.com/healthkit/activity.read https://www.huawei.com/healthkit/activityrecord.read"
    
    params = {
        'response_type': 'code',
        'client_id': HUAWEI_CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': scopes,
        'state': athlete_id,
        'access_type': 'offline'
    }
    
    return f"https://oauth-login.cloud.huawei.com/oauth2/v3/authorize?{urlencode(params)}"

def exchange_huawei_token(code, athlete_id):
    """Exchange auth code for access token"""
    if not HUAWEI_CLIENT_ID or not HUAWEI_CLIENT_SECRET:
        return False, "Huawei credentials not configured in .env"

    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': HUAWEI_CLIENT_ID,
        'client_secret': HUAWEI_CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI
    }
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        response = requests.post("https://oauth-login.cloud.huawei.com/oauth2/v3/token", data=payload, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        access_token = data.get('access_token')
        refresh_token = data.get('refresh_token')
        
        p = player.objects.filter(player=athlete_id).first()
        if p:
            integration, _ = PlayerIntegration.objects.get_or_create(player=p)
            integration.huawei_access_token = access_token
            integration.huawei_refresh_token = refresh_token
            integration.save()
            return True, "Huawei connected successfully"
        return False, "Athlete not found"
    except Exception as e:
        print(f"Huawei Token Error: {e}")
        if 'response' in locals() and hasattr(response, 'text'):
            print(f"Huawei API Response: {response.text}")
        return False, str(e)

def sync_huawei_data(athlete_id):
    """Fetch Huawei workouts"""
    p = player.objects.filter(player=athlete_id).first()
    if not p:
        return False, "Athlete not found"
        
    integration = getattr(p, 'integration', None)
    if not integration or not integration.huawei_access_token:
        return False, "Huawei not connected for this athlete"

    headers = {
        'Authorization': f'Bearer {integration.huawei_access_token}',
        'Content-Type': 'application/json'
    }

    try:
        # NOTE: Huawei usually requires specific date ranges or timestamps for fetching data.
        # This is a generalized API call.
        endpoint = "https://health-api.cloud.huawei.com/healthkit/v2/activityRecords"
        
        # Example timestamp for the last 30 days
        import time
        now = int(time.time() * 1000)
        thirty_days_ago = now - (30 * 24 * 60 * 60 * 1000)
        
        params = {
            'startTime': thirty_days_ago,
            'endTime': now
        }
        
        workout_resp = requests.get(endpoint, headers=headers, params=params)
        workout_resp.raise_for_status()
        workouts = workout_resp.json().get('activityRecords', [])
        
        synced_count = 0
        for w in workouts:
            external_id = str(w.get('activityRecordId', w.get('id')))
            
            # Cek apakah sudah ada
            existing = ActivityLog.objects.filter(source='huawei', external_id=external_id).first()
            if existing:
                continue
                
            sport_type = "Huawei Sport ID: " + str(w.get('activityType', 'Unknown'))
            summary = w.get('activitySummary', {})
            
            # Distance in meters usually
            distance = summary.get('distance', 0)
            calories = summary.get('calories', 0)
            
            # Waktu mulai
            try:
                # Huawei usually returns timestamps in milliseconds
                dt = datetime.fromtimestamp(w.get('startTime') / 1000.0)
                dt = make_aware(dt)
            except:
                dt = make_aware(datetime.now())

            # Create activity
            ActivityLog.objects.create(
                player=p,
                source='huawei',
                external_id=external_id,
                name=w.get('activityName', 'Huawei Workout'),
                sport_type=sport_type,
                start_time=dt,
                duration=w.get('duration') or (w.get('endTime', 0) - w.get('startTime', 0)) / 1000.0,
                distance=distance,
                calories=calories,
                avg_hr=summary.get('averageHeartRate', 0),
                max_hr=summary.get('maxHeartRate', 0),
                raw_payload=w
            )
            synced_count += 1
            
        return True, f"Successfully synced {synced_count} Huawei workouts"
    except Exception as e:
        print(f"Huawei Sync Error: {e}")
        if 'workout_resp' in locals() and hasattr(workout_resp, 'text'):
            print(f"Huawei API Response: {workout_resp.text}")
        return False, str(e)
