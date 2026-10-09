# app/services/youtube_service.py
# Service untuk upload video ke YouTube menggunakan YouTube Data API v3.
# OAuth2 flow (web redirect — headless-compatible):
#   Step 1: Server generate auth URL → user di-redirect ke Google
#   Step 2: Google redirect balik ke server callback → token tersimpan otomatis
# Token disimpan di file lokal untuk sesi selanjutnya.

import os
import logging
import httplib2
from pathlib import Path

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)

# Scope yang dibutuhkan untuk upload video
YOUTUBE_UPLOAD_SCOPE = ['https://www.googleapis.com/auth/youtube.upload']

# YouTube video category: "17" = Sports
YOUTUBE_SPORTS_CATEGORY = '17'

# In-memory store for PKCE code_verifier per OAuth state
# Key: state string, Value: code_verifier string
_pending_oauth = {}


def _get_paths():
    """Get paths for client secret and token files from env."""
    client_secret = os.getenv('YOUTUBE_CLIENT_SECRET_FILE', 'client_secret.json')
    token_file = os.getenv('YOUTUBE_TOKEN_FILE', 'youtube_token.json')
    return client_secret, token_file


def _get_redirect_uri():
    """Get OAuth redirect URI from env."""
    return os.getenv('YOUTUBE_REDIRECT_URI', 'http://localhost:5000/api/youtube/oauth2callback')


def get_auth_status():
    """Check if YouTube OAuth2 token exists and is valid.
    
    Returns:
        dict: {'authenticated': bool, 'message': str}
    """
    client_secret, token_file = _get_paths()

    # Check client_secret exists
    if not os.path.exists(client_secret):
        return {
            'authenticated': False,
            'has_client_secret': False,
            'message': f'File {client_secret} belum tersedia. '
                       'Download dari Google Cloud Console > APIs & Services > Credentials.'
        }

    # Check token exists and valid
    if not os.path.exists(token_file):
        return {
            'authenticated': False,
            'has_client_secret': True,
            'message': 'Belum login ke Google. Klik "Login YouTube" untuk authorize.'
        }

    try:
        creds = Credentials.from_authorized_user_file(token_file, YOUTUBE_UPLOAD_SCOPE)
        if creds and creds.valid:
            logger.info("[YOUTUBE] Auth status: valid token found")
            return {
                'authenticated': True,
                'has_client_secret': True,
                'message': 'Sudah ter-autentikasi dengan YouTube.'
            }
        elif creds and creds.refresh_token:
            # Token mungkin expired atau access token tidak tersimpan di file
            # (to_json() kadang tidak simpan access token) — coba refresh
            try:
                creds.refresh(Request())
                # Save refreshed token
                with open(token_file, 'w') as f:
                    f.write(creds.to_json())
                logger.info("[YOUTUBE] Auth status: token refreshed successfully")
                return {
                    'authenticated': True,
                    'has_client_secret': True,
                    'message': 'Token di-refresh. Sudah ter-autentikasi.'
                }
            except Exception as refresh_err:
                logger.warning(f"[YOUTUBE] Token refresh failed: {refresh_err}")
                return {
                    'authenticated': False,
                    'has_client_secret': True,
                    'message': 'Token expired dan gagal di-refresh. Perlu login ulang.'
                }
        else:
            logger.warning("[YOUTUBE] Auth status: no valid token or refresh_token")
            return {
                'authenticated': False,
                'has_client_secret': True,
                'message': 'Token tidak valid. Perlu login ulang.'
            }
    except Exception as e:
        logger.error(f"[YOUTUBE] Error checking auth status: {e}")
        return {
            'authenticated': False,
            'has_client_secret': True,
            'message': f'Error memvalidasi token: {str(e)}'
        }


def create_auth_url():
    """Generate Google OAuth2 authorization URL (web redirect flow).
    
    User akan di-redirect ke URL ini. Setelah login,
    Google redirect balik ke server callback URL.
    
    Returns:
        dict: {'auth_url': str, 'state': str}
    
    Raises:
        FileNotFoundError: jika client_secret.json tidak ditemukan
    """
    client_secret, token_file = _get_paths()
    redirect_uri = _get_redirect_uri()

    if not os.path.exists(client_secret):
        raise FileNotFoundError(
            f"File {client_secret} tidak ditemukan. "
            "Download dari Google Cloud Console > APIs & Services > Credentials."
        )

    flow = Flow.from_client_secrets_file(
        client_secret,
        scopes=YOUTUBE_UPLOAD_SCOPE,
    )
    flow.redirect_uri = redirect_uri

    auth_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )

    # Store the PKCE code_verifier so we can use it during token exchange
    _pending_oauth[state] = flow.code_verifier
    logger.info(f"[YOUTUBE] Auth URL generated (redirect_uri={flow.redirect_uri}), state={state}")

    return {
        'auth_url': auth_url,
        'state': state
    }


def exchange_auth_code(code, state=None):
    """Exchange authorization code for credentials and save token.
    
    Dipanggil oleh callback endpoint setelah Google redirect.
    
    Args:
        code: Authorization code dari Google OAuth redirect
        state: OAuth state parameter — used to retrieve PKCE code_verifier
    
    Returns:
        Credentials object
    
    Raises:
        FileNotFoundError: jika client_secret.json tidak ditemukan
        Exception: jika exchange gagal
    """
    client_secret, token_file = _get_paths()
    redirect_uri = _get_redirect_uri()

    if not os.path.exists(client_secret):
        raise FileNotFoundError(
            f"File {client_secret} tidak ditemukan."
        )

    flow = Flow.from_client_secrets_file(
        client_secret,
        scopes=YOUTUBE_UPLOAD_SCOPE,
    )
    flow.redirect_uri = redirect_uri

    # Restore PKCE code_verifier from the auth step
    if state and state in _pending_oauth:
        flow.code_verifier = _pending_oauth.pop(state)
        logger.info("[YOUTUBE] PKCE code_verifier restored from state")
    else:
        logger.warning("[YOUTUBE] No PKCE code_verifier found for state — token exchange may fail")

    flow.fetch_token(code=code)
    creds = flow.credentials

    # Save token
    with open(token_file, 'w') as f:
        f.write(creds.to_json())

    logger.info("[YOUTUBE] ✅ Token saved via OAuth2 callback")
    return creds


def authenticate():
    """Get YouTube credentials from saved token.
    
    Jika token sudah ada dan valid, langsung pakai.
    Jika expired, refresh otomatis.
    Jika belum ada token, raise error (user harus login dulu via web).
    
    Returns:
        Credentials object
    
    Raises:
        RuntimeError: jika belum authenticate
    """
    client_secret, token_file = _get_paths()

    creds = None

    # Load existing token
    if os.path.exists(token_file):
        try:
            creds = Credentials.from_authorized_user_file(token_file, YOUTUBE_UPLOAD_SCOPE)
        except Exception:
            creds = None

    # Valid token
    if creds and creds.valid:
        return creds

    # Refresh token jika tidak valid tapi ada refresh_token
    # (to_json() kadang tidak simpan access token, jadi creds.valid bisa False
    #  dan creds.expired juga False — tetap coba refresh)
    if creds and not creds.valid and creds.refresh_token:
        try:
            creds.refresh(Request())
            with open(token_file, 'w') as f:
                f.write(creds.to_json())
            logger.info("[YOUTUBE] Token refreshed successfully")
            return creds
        except Exception as e:
            logger.warning(f"[YOUTUBE] Token refresh failed: {e}")
            creds = None

    # No valid token — user harus login dulu via web
    raise RuntimeError(
        "Belum authenticate ke YouTube. "
        "Klik tombol 'Login YouTube' untuk login via Google."
    )


def get_youtube_client():
    """Create authenticated YouTube API client.
    
    Returns:
        googleapiclient.discovery.Resource (YouTube API client)
    """
    creds = authenticate()
    if not creds:
        raise RuntimeError("Gagal authenticate ke YouTube")
    
    return build('youtube', 'v3', credentials=creds)


def upload_to_youtube(video_path, title, description='',
                      privacy=None, category_id=YOUTUBE_SPORTS_CATEGORY,
                      tags=None):
    """Upload video ke YouTube.
    
    Args:
        video_path: Path absolut ke file video (mp4)
        title: Judul video di YouTube
        description: Deskripsi video
        privacy: 'unlisted', 'private', atau 'public'
        category_id: YouTube category ID (default: 17 = Sports)
        tags: List of tags
    
    Returns:
        dict: {'video_id': str, 'youtube_url': str} on success
    
    Raises:
        FileNotFoundError: if video file doesn't exist
        HttpError: if YouTube API call fails
        RuntimeError: if authentication fails
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file tidak ditemukan: {video_path}")

    if privacy is None:
        privacy = os.getenv('YOUTUBE_DEFAULT_PRIVACY', 'unlisted')

    if tags is None:
        tags = ['football', 'training', 'analysis', 'counting', 'passing']

    # Truncate title to YouTube max (100 chars)
    if len(title) > 100:
        title = title[:97] + '...'

    youtube = get_youtube_client()

    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': category_id,
        },
        'status': {
            'privacyStatus': privacy,
            'selfDeclaredMadeForKids': False,
        }
    }

    # Use resumable upload for large files
    file_size = os.path.getsize(video_path)
    logger.info(f"[YOUTUBE] Uploading: {title} ({file_size / (1024*1024):.1f} MB)")

    media = MediaFileUpload(
        video_path,
        mimetype='video/mp4',
        resumable=True,
        chunksize=10 * 1024 * 1024  # 10MB chunks
    )

    request = youtube.videos().insert(
        part='snippet,status',
        body=body,
        media_body=media
    )

    # Execute upload with progress logging
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            progress = int(status.progress() * 100)
            logger.info(f"[YOUTUBE] Upload progress: {progress}%")

    video_id = response.get('id')
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"

    logger.info(f"[YOUTUBE] ✅ Upload complete: {youtube_url}")

    return {
        'video_id': video_id,
        'youtube_url': youtube_url,
        'title': response['snippet']['title'],
        'privacy': response['status']['privacyStatus'],
    }
