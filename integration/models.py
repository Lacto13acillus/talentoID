from django.db import models
from player.models import player
from django.db.models import JSONField

class PlayerIntegration(models.Model):
    player = models.OneToOneField(player, on_delete=models.CASCADE, related_name='integration')
    
    # OAuth Tokens
    strava_access_token = models.CharField(max_length=1024, null=True, blank=True)
    strava_refresh_token = models.CharField(max_length=1024, null=True, blank=True)
    strava_expires_at = models.IntegerField(null=True, blank=True) # Unix timestamp
    
    whoop_access_token = models.CharField(max_length=1024, null=True, blank=True)
    whoop_refresh_token = models.CharField(max_length=1024, null=True, blank=True)
    
    polar_access_token = models.CharField(max_length=1024, null=True, blank=True)
    
    huawei_access_token = models.CharField(max_length=1024, null=True, blank=True)
    huawei_refresh_token = models.CharField(max_length=1024, null=True, blank=True)
    
    # Provider User IDs
    strava_athlete_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    terra_user_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    whoop_user_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    polar_user_id = models.CharField(max_length=255, unique=True, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Integrations for {self.player.nama}"

class ActivityLog(models.Model):
    player = models.ForeignKey(player, on_delete=models.CASCADE, related_name='activities')
    
    source = models.CharField(max_length=50) # e.g., 'strava', 'polar', 'terra'
    external_id = models.CharField(max_length=255, null=True, blank=True)
    
    name = models.CharField(max_length=255, null=True, blank=True)
    sport_type = models.CharField(max_length=100, null=True, blank=True)
    
    start_time = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True) # in seconds
    distance = models.FloatField(null=True, blank=True) # in meters
    calories = models.FloatField(null=True, blank=True)
    
    avg_hr = models.IntegerField(null=True, blank=True)
    max_hr = models.IntegerField(null=True, blank=True)
    
    # Raw payload for backup/debugging
    raw_payload = JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ActivityLog {self.name} via {self.source}"
