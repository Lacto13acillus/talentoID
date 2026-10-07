from django.urls import path
from . import views

urlpatterns = [
    # Strava
    path('strava/auth/<str:athlete_id>', views.strava_auth, name='strava_auth'),
    path('strava/callback', views.strava_callback, name='strava_callback'),
    path('strava/sync/<str:athlete_id>', views.strava_sync, name='strava_sync'),
    
    # Terra
    path('terra/auth/<str:athlete_id>', views.terra_auth, name='terra_auth'),
    path('terra/webhook', views.terra_webhook, name='terra_webhook'),
    
    # Whoop
    path('whoop/auth/<str:athlete_id>', views.whoop_auth, name='whoop_auth'),
    path('whoop/callback', views.whoop_callback, name='whoop_callback'),
    path('whoop/sync/<str:athlete_id>', views.whoop_sync, name='whoop_sync'),
    
    # Polar
    path('polar/auth/<str:athlete_id>', views.polar_auth, name='polar_auth'),
    path('polar/callback', views.polar_callback, name='polar_callback'),
    path('polar/sync/<str:athlete_id>', views.polar_sync, name='polar_sync'),
    
    # Huawei
    path('huawei/auth/<str:athlete_id>', views.huawei_auth, name='huawei_auth'),
    path('huawei/callback', views.huawei_callback, name='huawei_callback'),
    path('huawei/sync/<str:athlete_id>', views.huawei_sync, name='huawei_sync'),
]
