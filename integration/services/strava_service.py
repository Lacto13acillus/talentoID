import os
import requests
from datetime import datetime
from integration.models import PlayerIntegration, ActivityLog
from player.models import player
from django.utils.timezone import make_aware, now

STRAVA_CLIENT_ID = os.getenv('STRAVA_CLIENT_ID')
STRAVA_CLIENT_SECRET = os.getenv('STRAVA_CLIENT_SECRET')
STRAVA_REDIRECT_URI = os.getenv('STRAVA_REDIRECT_URI')

def get_auth_url(athlete_id):
    """Generate Strava OAuth2 authorization URL"""
    return f"https://www.strava.com/oauth/authorize?client_id={STRAVA_CLIENT_ID}&response_type=code&redirect_uri={STRAVA_REDIRECT_URI}?athlete_id={athlete_id}&approval_prompt=force&scope=activity:read_all,profile:read_all"

def exchange_token(code, athlete_id):
    """Exchange authorization code for access/refresh tokens"""
    url = "https://www.strava.com/oauth/token"
    payload = {
        'client_id': STRAVA_CLIENT_ID,
        'client_secret': STRAVA_CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code'
    }
    
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        data = response.json()
        
        # Save to DB
        p = player.objects.filter(player=athlete_id).first()
        if p:
            integration, _ = PlayerIntegration.objects.get_or_create(player=p)
            integration.strava_access_token = data.get('access_token')
            integration.strava_refresh_token = data.get('refresh_token')
            integration.strava_expires_at = data.get('expires_at')
            integration.strava_athlete_id = str(data.get('athlete', {}).get('id'))
            integration.save()
            return True, "Successfully connected to Strava."
    
    return False, f"Failed to exchange token. Response: {response.text}"

def refresh_access_token(integration):
    """Refresh the access token if expired"""
    if not integration.strava_refresh_token:
        return False
        
    url = "https://www.strava.com/oauth/token"
    payload = {
        'client_id': STRAVA_CLIENT_ID,
        'client_secret': STRAVA_CLIENT_SECRET,
        'refresh_token': integration.strava_refresh_token,
        'grant_type': 'refresh_token'
    }
    
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        data = response.json()
        integration.strava_access_token = data.get('access_token')
        integration.strava_refresh_token = data.get('refresh_token')
        integration.strava_expires_at = data.get('expires_at')
        integration.save()
        return True
    return False

def sync_activities(p):
    """Fetch and sync activities from Strava"""
    integration = getattr(p, 'integration', None)
    if not integration:
        return False, "Player has no integrations"

    # Check token expiration
    current_time = int(now().timestamp())
    if integration.strava_expires_at and integration.strava_expires_at <= current_time:
        if not refresh_access_token(integration):
            return False, "Failed to refresh token"
            
    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {
        "Authorization": f"Bearer {integration.strava_access_token}"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        activities = response.json()
        synced_count = 0
        
        for act in activities:
            external_id = str(act.get('id'))
            
            # Check if exists
            existing = ActivityLog.objects.filter(player=p, source='strava', external_id=external_id).first()
            
            if not existing:
                try:
                    start_time = datetime.strptime(act.get('start_date_local'), "%Y-%m-%dT%H:%M:%SZ")
                    start_time = make_aware(start_time)
                except:
                    start_time = None
                    
                ActivityLog.objects.create(
                    player=p,
                    source='strava',
                    external_id=external_id,
                    name=act.get('name'),
                    sport_type=act.get('type'),
                    start_time=start_time,
                    duration=act.get('moving_time'),
                    distance=act.get('distance'),
                    avg_hr=act.get('average_heartrate'),
                    max_hr=act.get('max_heartrate'),
                    raw_payload=act
                )
                synced_count += 1
                
        return True, f"Synced {synced_count} activities."
        
    return False, f"Failed to fetch activities: {response.status_code}"
