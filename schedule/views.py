from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from .usecase import UsecaseSchedule
from rest_framework import status
import json

@api_view(["POST", "GET", "PUT", "DELETE"])
@authentication_classes([JWTAuthentication])  # Tambahkan autentikasi JWT
@permission_classes([IsAuthenticated])       # Hanya user yang terautentikasi yang bisa mengakses
def schedule_handler(request):
    if request.method == "POST":
        # Handle POST request
        if not all(key in request.data for key in ["tanggal", "start_time", "end_time"]):
            return Response({
                "code": 400,
                "message": "tanggal, start_time, and end_time are required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        data = UsecaseSchedule.post(request)
        return Response({
            "code": 200,
            "message": "sukses",
            "data": data
        }, status=status.HTTP_200_OK)

    elif request.method == "GET":
        # Handle GET request
        try:
            schedule_id = request.query_params.get("schedule")
            if schedule_id:
                # Existing single schedule GET
                data = UsecaseSchedule.get(str(schedule_id))
                return Response({
                    "code": 200,
                    "message": "sukses",
                    "data": data
                }, status=status.HTTP_200_OK)
            else:
                # New GET ALL implementation
                data = UsecaseSchedule.get_all()
                return Response({
                    "code": 200,
                    "message": "sukses",
                    "data": data
                }, status=status.HTTP_200_OK)
                
        except json.JSONDecodeError:
            return Response({
                "code": 400,
                "message": "Invalid JSON in request body"
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "code": 404,
                "message": str(e)
            }, status=status.HTTP_404_NOT_FOUND)

    elif request.method == "PUT":
        # Handle PUT request
        if "schedule" not in request.data:
            return Response({
                "code": 400,
                "message": "schedule is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        data = UsecaseSchedule.put(request)
        return Response({
            "code": 200,
            "message": "sukses",
            "data": data
        }, status=status.HTTP_200_OK)

    elif request.method == "DELETE":
        # Handle DELETE request
        if "schedule" not in request.data:
            return Response({
                "code": 400,
                "message": "schedule is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        data = UsecaseSchedule.delete(request)
        return Response({
            "code": 200,
            "message": "sukses",
            "data": data
        }, status=status.HTTP_200_OK)

