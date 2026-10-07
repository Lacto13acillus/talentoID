from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from player.models import player
from integration.services import strava_service, terra_service, whoop_service, polar_service, huawei_service

# =======================
# STRAVA VIEWS
# =======================
def strava_auth(request, athlete_id):
    p = player.objects.filter(player=athlete_id).first()
    if not p:
        return JsonResponse({"error": "Athlete not found"}, status=404)
        
    auth_url = strava_service.get_auth_url(athlete_id)
    return redirect(auth_url)

def strava_callback(request):
    error = request.GET.get('error')
    if error:
        return JsonResponse({"error": f"Authorization failed: {error}"}, status=400)
        
    code = request.GET.get('code')
    athlete_id = request.GET.get('athlete_id')
    
    if not code or not athlete_id:
        return JsonResponse({"error": "Missing code or athlete_id"}, status=400)
        
    success, message = strava_service.exchange_token(code, athlete_id)
    
    if success:
        html = f"""
        <html>
        <head>
            <title>Strava Connected</title>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
            <style>
                body {{ font-family: 'Inter', sans-serif; background: #0f172a; color: white; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }}
                .container {{ text-align: center; background: #1e293b; padding: 3rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); border-top: 4px solid #fc4c02; }}
                h2 {{ color: #4ade80; margin-bottom: 1rem; }}
                .btn {{ display: inline-block; margin-top: 1.5rem; padding: 0.75rem 1.5rem; background: #3b82f6; color: white; text-decoration: none; border-radius: 6px; font-weight: 600; transition: background 0.2s; }}
                .btn:hover {{ background: #2563eb; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>✅ Strava Connected Successfully!</h2>
                <p>Data akun Strava Anda telah berhasil dihubungkan.</p>
                <a href="/integrations" class="btn">Kembali ke Dashboard</a>
            </div>
        </body>
        </html>
        """
        return HttpResponse(html, status=200)
    else:
        return JsonResponse({"error": message}, status=500)

@csrf_exempt
def strava_sync(request, athlete_id):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
        
    p = player.objects.filter(player=athlete_id).first()
    if not p:
        return JsonResponse({"error": "Athlete not found"}, status=404)
        
    success, message = strava_service.sync_activities(p)
    
    if success:
        return JsonResponse({"message": message}, status=200)
    else:
        return JsonResponse({"error": message}, status=500)


# =======================
# TERRA VIEWS
# =======================
def terra_auth(request, athlete_id):
    p = player.objects.filter(player=athlete_id).first()
    if not p:
        return JsonResponse({"error": "Athlete not found"}, status=404)
        
    url, error = terra_service.get_terra_widget_url(athlete_id)
    if error:
        return JsonResponse({"error": error}, status=400)
        
    return redirect(url)

@csrf_exempt
def terra_webhook(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
        
    signature = request.headers.get('terra-signature')
    if not signature:
        return JsonResponse({"status": "error", "message": "Missing signature"}, status=401)
        
    payload_str = request.body.decode('utf-8')
    
    if not terra_service.verify_terra_signature(payload_str, signature):
        return JsonResponse({"status": "error", "message": "Invalid signature"}, status=401)
        
    try:
        payload = json.loads(request.body)
        terra_service.process_terra_webhook(payload)
        return JsonResponse({"status": "success"}, status=200)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


# =======================
# WHOOP VIEWS
# =======================
def whoop_auth(request, athlete_id):
    auth_url = whoop_service.get_whoop_auth_url(athlete_id)
    return redirect(auth_url)

def whoop_callback(request):
    code = request.GET.get('code')
    athlete_id = request.GET.get('state') 
    
    if not code or not athlete_id:
        return HttpResponse("Missing code or state parameter", status=400)
        
    success, message = whoop_service.exchange_whoop_token(code, athlete_id)
    
    return redirect('/integrations')

@csrf_exempt
def whoop_sync(request, athlete_id):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
        
    success, message = whoop_service.sync_whoop_data(athlete_id)
    
    if success:
        return JsonResponse({"message": message})
    else:
        return JsonResponse({"error": message}, status=400)


# =======================
# POLAR VIEWS
# =======================
def polar_auth(request, athlete_id):
    auth_url = polar_service.get_polar_auth_url(athlete_id)
    return redirect(auth_url)

def polar_callback(request):
    code = request.GET.get('code')
    athlete_id = request.GET.get('state') 
    
    if not code or not athlete_id:
        return HttpResponse("Missing code or state parameter", status=400)
        
    success, message = polar_service.exchange_polar_token(code, athlete_id)
    
    if success:
        html = f"""
        <html>
        <head>
            <title>Polar Connected</title>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
            <style>
                body {{ font-family: 'Inter', sans-serif; background: #0f172a; color: white; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }}
                .success-box {{ background-color: #1e293b; padding: 3rem; border-radius: 12px; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.1); }}
                h1 {{ color: #4ade80; margin-bottom: 1rem; }}
                p {{ color: #94a3b8; margin-bottom: 2rem; line-height: 1.5; }}
                .btn {{ background-color: #3b82f6; color: white; padding: 0.75rem 1.5rem; text-decoration: none; border-radius: 6px; font-weight: 600; transition: background-color 0.2s; }}
                .btn:hover {{ background-color: #2563eb; }}
            </style>
        </head>
        <body>
            <div class="success-box">
                <h1>✅ Polar AccessLink Connected!</h1>
                <p>Your Polar account has been successfully linked to your profile.<br>We have also registered your account to start collecting data.</p>
                <a href="/integrations" class="btn">Kembali ke Dashboard</a>
            </div>
        </body>
        </html>
        """
        return HttpResponse(html)
    else:
        return JsonResponse({"error": message}, status=400)

@csrf_exempt
def polar_sync(request, athlete_id):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
        
    success, message = polar_service.sync_polar_activities(athlete_id)
    if success:
        return JsonResponse({"message": message})
    else:
        return JsonResponse({"error": message}, status=400)


# =======================
# HUAWEI VIEWS
# =======================
def huawei_auth(request, athlete_id):
    auth_url = huawei_service.get_huawei_auth_url(athlete_id)
    return redirect(auth_url)

def huawei_callback(request):
    code = request.GET.get('code')
    athlete_id = request.GET.get('state') 
    
    if not code or not athlete_id:
        return HttpResponse("Missing code or state parameter", status=400)
        
    success, message = huawei_service.exchange_huawei_token(code, athlete_id)
    
    if success:
        html = f"""
        <html>
        <head>
            <title>Huawei Health Connected</title>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
            <style>
                body {{ font-family: 'Inter', sans-serif; background: #0f172a; color: white; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }}
                .success-box {{ background-color: #1e293b; padding: 3rem; border-radius: 12px; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.1); border-top: 4px solid #ef4444; }}
                h1 {{ color: #4ade80; margin-bottom: 1rem; }}
                p {{ color: #94a3b8; margin-bottom: 2rem; line-height: 1.5; }}
                .btn {{ background-color: #3b82f6; color: white; padding: 0.75rem 1.5rem; text-decoration: none; border-radius: 6px; font-weight: 600; transition: background-color 0.2s; }}
                .btn:hover {{ background-color: #2563eb; }}
            </style>
        </head>
        <body>
            <div class="success-box">
                <h1>✅ Huawei Health Connected!</h1>
                <p>Your Huawei Health account has been successfully linked to your profile.</p>
                <a href="/integrations" class="btn">Kembali ke Dashboard</a>
            </div>
        </body>
        </html>
        """
        return HttpResponse(html)
    else:
        return JsonResponse({"error": message}, status=400)

@csrf_exempt
def huawei_sync(request, athlete_id):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
        
    success, message = huawei_service.sync_huawei_data(athlete_id)
    if success:
        return JsonResponse({"message": message})
    else:
        return JsonResponse({"error": message}, status=400)
