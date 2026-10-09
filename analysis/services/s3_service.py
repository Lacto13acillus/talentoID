# app/services/s3_service.py
# Service untuk upload video ke S3-compatible storage (CloudHost.id)
import os
import logging
import boto3
from botocore.config import Config as BotoConfig
from botocore.exceptions import ClientError, NoCredentialsError

logger = logging.getLogger(__name__)

# S3 Configuration from environment
S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL', 'https://is3.cloudhost.id')
S3_ACCESS_KEY_ID = os.getenv('S3_ACCESS_KEY_ID', '')
S3_SECRET_ACCESS_KEY = os.getenv('S3_SECRET_ACCESS_KEY', '')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'football-analysis')
S3_REGION = os.getenv('S3_REGION', 'us-east-1')

# Cached client
_s3_client = None


def get_s3_client():
    """Get or create a boto3 S3 client configured for CloudHost.id.
    
    Uses signature v2 (s3) and path-style addressing for maximum
    compatibility with S3-compatible providers like CloudHost.id/iS3.
    """
    global _s3_client
    if _s3_client is not None:
        return _s3_client

    if not S3_ACCESS_KEY_ID or not S3_SECRET_ACCESS_KEY:
        logger.error("[S3] Access key or secret key not configured in environment")
        raise ValueError("S3 credentials not configured. Set S3_ACCESS_KEY_ID and S3_SECRET_ACCESS_KEY in .env")

    # Konfigurasi khusus untuk S3-compatible storage (CloudHost.id):
    # 1. signature_version='s3' → gunakan AWS Signature V2 (bukan V4)
    #    V4 menggunakan chunked transfer-encoding yang menghapus Content-Length header
    # 2. s3.addressing_style='path' → gunakan path-style URL, bukan virtual-hosted
    _s3_client = boto3.client(
        's3',
        endpoint_url=S3_ENDPOINT_URL,
        aws_access_key_id=S3_ACCESS_KEY_ID,
        aws_secret_access_key=S3_SECRET_ACCESS_KEY,
        region_name=S3_REGION,
        config=BotoConfig(
            signature_version='s3',
            s3={'addressing_style': 'path'},
        ),
    )
    logger.info(f"[S3] Client initialized — endpoint={S3_ENDPOINT_URL}, bucket={S3_BUCKET_NAME}, sig=v2, path-style")
    return _s3_client


def generate_s3_key(mode, job_id, filename=None):
    """Generate a structured S3 object key.

    Format: videos/{mode}/{job_id}_{filename}
    Example: videos/heading/abc123_heading_output.mp4

    Args:
        mode: Analysis mode (heading, passing, manual, dribbling)
        job_id: Job ID string
        filename: Optional original filename. If None, uses job_id.mp4

    Returns:
        S3 object key string
    """
    if filename:
        # Sanitize filename — keep only basename
        safe_name = os.path.basename(filename)
    else:
        safe_name = f"{job_id}.mp4"

    return f"videos/{mode}/{job_id}_{safe_name}"


def upload_video_to_s3(local_path, s3_key, content_type='video/mp4'):
    """Upload a video file to S3 bucket.

    Args:
        local_path: Absolute path to the local video file
        s3_key: S3 object key (path within bucket)
        content_type: MIME type (default: video/mp4)

    Returns:
        Public URL string if successful, None if failed
    """
    if not os.path.exists(local_path):
        logger.error(f"[S3] File not found: {local_path}")
        return None

    file_size = os.path.getsize(local_path)
    file_size_mb = file_size / (1024 * 1024)
    logger.info(f"[S3] Uploading {local_path} ({file_size_mb:.1f}MB) → s3://{S3_BUCKET_NAME}/{s3_key}")
    print(f"[S3] ⬆️  Uploading {file_size_mb:.1f}MB → s3://{S3_BUCKET_NAME}/{s3_key}")

    try:
        client = get_s3_client()

        # Baca file sebagai bytes agar Content-Length pasti terset di HTTP header.
        # Menggunakan file handle (open as 'rb') kadang tidak cukup untuk
        # S3-compatible storage yang strict soal Content-Length.
        file_bytes = open(local_path, 'rb').read()

        client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=s3_key,
            Body=file_bytes,
            ContentType=content_type,
            ContentLength=file_size,
        )

        # Construct public URL
        # CloudHost.id path-style: https://is3.cloudhost.id/{bucket}/{key}
        public_url = f"{S3_ENDPOINT_URL}/{S3_BUCKET_NAME}/{s3_key}"

        logger.info(f"[S3] ✅ Upload successful: {public_url}")
        print(f"[S3] ✅ Upload successful: {public_url}")

        return public_url

    except NoCredentialsError:
        logger.error("[S3] ❌ No credentials found")
        print("[S3] ❌ Upload failed: No credentials")
        return None
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', 'UnknownCode')
        error_msg = e.response.get('Error', {}).get('Message', str(e))
        logger.error(f"[S3] ❌ ClientError ({error_code}): {error_msg}")
        print(f"[S3] ❌ Upload failed: {error_code} — {error_msg}")
        return None
    except Exception as e:
        logger.error(f"[S3] ❌ Unexpected error: {e}", exc_info=True)
        print(f"[S3] ❌ Upload failed: {e}")
        return None


def check_s3_connection():
    """Test S3 connection by listing bucket contents (max 1 item).

    Returns:
        True if connection successful, False otherwise
    """
    try:
        client = get_s3_client()
        client.head_bucket(Bucket=S3_BUCKET_NAME)
        logger.info(f"[S3] ✅ Connection OK — bucket '{S3_BUCKET_NAME}' accessible")
        print(f"[S3] ✅ Connection OK — bucket '{S3_BUCKET_NAME}' accessible")
        return True
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', '')
        if error_code == '404':
            logger.error(f"[S3] ❌ Bucket '{S3_BUCKET_NAME}' not found")
            print(f"[S3] ❌ Bucket '{S3_BUCKET_NAME}' not found")
        elif error_code == '403':
            logger.error(f"[S3] ❌ Access denied to bucket '{S3_BUCKET_NAME}'")
            print(f"[S3] ❌ Access denied to bucket '{S3_BUCKET_NAME}'")
        else:
            logger.error(f"[S3] ❌ Error: {e}")
            print(f"[S3] ❌ Connection error: {e}")
        return False
    except Exception as e:
        logger.error(f"[S3] ❌ Connection failed: {e}")
        print(f"[S3] ❌ Connection failed: {e}")
        return False
