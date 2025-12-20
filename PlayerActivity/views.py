# PlayerActivity/views.py
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status as http_status
from django.core.exceptions import ValidationError
from .usecase import UsecasePlayerActivity

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def player_activity_handler(request):
    try:
        player_id = request.query_params.get("player")
        if not player_id:
            return Response({
                "code": 400,
                "message": "player_id is required"
            }, status=http_status.HTTP_400_BAD_REQUEST)

        # Hitung aktivitas dan performa
        data = UsecasePlayerActivity.calculate_activity(player_id)
        return Response({
            "code": 200,
            "message": "Player activity calculated successfully",
            "data": data
        }, status=http_status.HTTP_200_OK)

    except ValidationError as e:
        return Response({
            "code": 400,
            "message": str(e)
        }, status=http_status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            "code": 500,
            "message": str(e)
        }, status=http_status.HTTP_500_INTERNAL_SERVER_ERROR)