from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status

class ScheduleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Skip middleware for specific endpoints (e.g., login or register)
        if request.path in ['/api/login/', '/api/register/']:
            return self.get_response(request)

         # ✅ Bypass POST ke /api/player/
        # if request.path.startswith('/api/player') and request.method == 'POST':
        #     return self.get_response(request)

        # ✅ Bypass semua method ke /api/xendit-callback/
        if request.path.startswith('/api/xendit-callback'):
            return self.get_response(request)

        # Check if the request is for the schedule endpoint
        if '/api/player/' in request.path:
            # Check for JWT token in the Authorization header
            auth_header = request.headers.get('Authorization', None)
            if not auth_header or not auth_header.startswith('Bearer '):
                return Response({
                    "code": 401,
                    "message": "Unauthorized: Token is missing or invalid."
                }, status=status.HTTP_401_UNAUTHORIZED)

            # Extract the token
            token = auth_header.split(' ')[1]

            # Authenticate the token
            try:
                jwt_auth = JWTAuthentication()
                validated_token = jwt_auth.get_validated_token(token)
                user = jwt_auth.get_user(validated_token)
                request.user = user  # Attach the user to the request object
            except AuthenticationFailed as e:
                return Response({
                    "code": 401,
                    "message": f"Unauthorized: {str(e)}"
                }, status=status.HTTP_401_UNAUTHORIZED)

        # Continue to the next middleware or view
        return self.get_response(request)
