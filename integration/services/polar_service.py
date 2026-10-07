import os
import requests
from datetime import datetime
from integration.models import PlayerIntegration, ActivityLog
from player.models import player
from django.utils.timezone import make_aware
import base64
import re

POLAR_CLIENT_ID = os.getenv('POLAR_CLIENT_ID')
POLAR_CLIENT_SECRET = os.getenv('POLAR_CLIENT_SECRET')

def parse_iso_duration(duration_str):
    """Parse PT1H30M15S format to seconds"""
    if not duration_str:
        return 0
    match = re.match(r'^PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+(?:\.\d+)?)S)?$', duration_str)
    if not match:
        return 0
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = float(match.group(3) or 0)
    return int(hours * 3600 + minutes * 60 + seconds)

def get_polar_auth_url(athlete_id):
    """Generate Polar AccessLink OAuth URL"""
    return f"https://flow.polar.com/oauth2/authorization?response_type=code&client_id={POLAR_CLIENT_ID}&state={athlete_id}"

def exchange_polar_token(code, athlete_id):
    """Exchange auth code for access token"""
    if not POLAR_CLIENT_ID or not POLAR_CLIENT_SECRET:
        return False, "Polar credentials not configured in .env"
        
    url = "https://polarremote.com/v2/oauth2/token"
    
    auth_str = f"{POLAR_CLIENT_ID}:{POLAR_CLIENT_SECRET}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()
    
    headers = {
        'Authorization': f'Basic {b64_auth_str}',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json;charset=UTF-8'
    }
    
    data = {
        'grant_type': 'authorization_code',
        'code': code
    }
    
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        token_data = response.json()
        
        access_token = token_data.get('access_token')
        x_user_id = token_data.get('x_user_id')
        
        if access_token:
            p = player.objects.filter(player=athlete_id).first()
            if p:
                integration, _ = PlayerIntegration.objects.get_or_create(player=p)
                integration.polar_access_token = access_token
                integration.polar_user_id = str(x_user_id)
                integration.save()
                
                # Register user to start data collection
                register_success = register_polar_user(access_token, integration.polar_user_id)
                if not register_success:
                    print("Warning: Failed to register user for data tracking. Perhaps already registered.")
                
                return True, "Success"
            return False, "Athlete not found"
        return False, "Failed to get access token"
    except Exception as e:
        return False, str(e)

def register_polar_user(access_token, polar_user_id):
    """Register user with AccessLink API to start generating data"""
    url = "https://www.polaraccesslink.com/v3/users"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    data = {
        "member-id": str(polar_user_id)
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        # 200 means registered, 409 means already registered
        if response.status_code in [200, 409]:
            return True
        print(f"Polar register error: {response.text}")
        return False
    except Exception as e:
        print(f"Exception registering user: {e}")
        return False

def sync_polar_activities(athlete_id):
    """Fetch new exercises via transaction flow"""
    p = player.objects.filter(player=athlete_id).first()
    if not p:
        return False, "Athlete not found"
        
    integration = getattr(p, 'integration', None)
    if not integration or not integration.polar_access_token:
        return False, "Athlete not connected to Polar"
        
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {integration.polar_access_token}'
    }
    
    # 1. Create Transaction
    tx_url = f"https://www.polaraccesslink.com/v3/users/{integration.polar_user_id}/exercise-transactions"
    
    try:
        tx_resp = requests.post(tx_url, headers=headers)
        if tx_resp.status_code == 204:
            return True, "No new data available"
        elif tx_resp.status_code != 201:
            return False, f"Failed to create transaction: {tx_resp.status_code} {tx_resp.text}"
            
        tx_data = tx_resp.json()
        tx_id = tx_data.get('transaction-id')
        tx_url_commit = tx_data.get('resource-uri')
        
        # 2. List available exercises in transaction
        exercises_url = f"https://www.polaraccesslink.com/v3/users/{integration.polar_user_id}/exercise-transactions/{tx_id}"
        ex_resp = requests.get(exercises_url, headers=headers)
        ex_resp.raise_for_status()
        
        exercises_list = ex_resp.json().get('exercises', [])
        
        added_count = 0
        for ex_url in exercises_list:
            # 3. Fetch each exercise
            detail_resp = requests.get(ex_url, headers=headers)
            if detail_resp.status_code == 200:
                act = detail_resp.json()
                
                # Insert to DB
                external_id = str(act.get('id'))
                existing = ActivityLog.objects.filter(player=p, source='polar', external_id=external_id).first()
                
                if not existing:
                    try:
                        start_time = datetime.fromisoformat(act.get('start-time', '').replace('Z', '+00:00'))
                        if start_time.tzinfo is None:
                            start_time = make_aware(start_time)
                    except:
                        start_time = make_aware(datetime.utcnow())
                        
                    duration_seconds = parse_iso_duration(act.get('duration', ''))
                    distance = act.get('distance', 0) # meters
                    calories = act.get('calories', 0)
                    avg_hr = act.get('heart-rate', {}).get('average', 0)
                    max_hr = act.get('heart-rate', {}).get('maximum', 0)
                    
                    ActivityLog.objects.create(
                        player=p,
                        source='polar',
                        external_id=external_id,
                        name=act.get('sport', 'Polar Exercise'),
                        sport_type=act.get('sport'),
                        start_time=start_time,
                        duration=duration_seconds,
                        distance=distance,
                        calories=calories,
                        avg_hr=avg_hr,
                        max_hr=max_hr,
                        raw_payload=act
                    )
                    added_count += 1
        
        # 4. Commit transaction
        commit_resp = requests.put(tx_url_commit, headers=headers)
        
        return True, f"Successfully synced {added_count} activities"
        
    except Exception as e:
        return False, f"Exception syncing Polar: {str(e)}"
