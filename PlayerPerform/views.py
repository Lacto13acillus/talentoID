from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .usecase import UsecasePlayerPerform
from rest_framework import status as http_status
from django.core.exceptions import ValidationError
import json
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(["POST", "GET", "PUT", "DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def player_perform_handler(request):
    try:
        if request.method == "POST":
            # Handle POST request
            required_fields = ["player", "kick_test", "tactical", "shoot_focus", "analyst", "shoot"]
            if not all(key in request.data for key in required_fields):
                return Response({
                    "code": 400,
                    "message": f"{', '.join(required_fields)} are required"
                }, status=http_status.HTTP_400_BAD_REQUEST)
            
            data = UsecasePlayerPerform.post(request)
            return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "GET":
            player_perform_id = request.query_params.get("playerperform")
            player_id = request.query_params.get("player")

            if player_id:
                # Hitung dan update Player Performance berdasarkan data IAP
                data = UsecasePlayerPerform.calculate_and_update_performance(player_id)
                return Response({
                    "code": 200,
                    "message": "sukses",
                    "data": data
                }, status=http_status.HTTP_200_OK)
            elif player_perform_id:
                # Existing single player perform GET
                data = UsecasePlayerPerform.get(player_perform_id)
                return Response({
                    "code": 200,
                    "message": "sukses",
                    "data": data
                }, status=http_status.HTTP_200_OK)
            else:
                # New GET ALL implementation
                data = UsecasePlayerPerform.get_all()
                return Response({
                    "code": 200,
                    "message": "sukses",
                    "data": data
                }, status=http_status.HTTP_200_OK)

        elif request.method == "PUT":
            # Handle PUT request
            if "playerperform" not in request.data:
                return Response({
                    "code": 400,
                    "message": "playerperform id is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecasePlayerPerform.put(request)
            return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "DELETE":
            # Handle DELETE request
            if "playerperform" not in request.data:
                return Response({
                    "code": 400,
                    "message": "playerperform id is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecasePlayerPerform.delete(request)
            return Response({
                "code": 200,
                "message": "sukses",
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