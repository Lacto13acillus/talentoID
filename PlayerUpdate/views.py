from rest_framework.decorators import api_view
from rest_framework.response import Response
from .usecase import UsecasePlayerUpdate
from rest_framework import status as http_status
from django.core.exceptions import ValidationError
import json

@api_view(["POST", "GET", "PUT", "DELETE"])
def playerupdate_handler(request):
    try:
        if request.method == "POST":
            # Handle POST request
            required_fields = ["player", "judul_update", "deskripsi"]
            if not all(key in request.data for key in required_fields):
                return Response({
                    "code": 400,
                    "message": f"{', '.join(required_fields)} are required"
                }, status=http_status.HTTP_400_BAD_REQUEST)
            
            data = UsecasePlayerUpdate.post(request)
            return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "GET":
            playerupdate_id = request.query_params.get("playerupdate")
            if playerupdate_id:
                # Jika ada playerupdate_id, ambil data spesifik
                data = UsecasePlayerUpdate.get(playerupdate_id)
            else:
                # Jika tidak ada playerupdate_id, ambil semua data
                data = UsecasePlayerUpdate.get_all()
            
            return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "PUT":
            # Handle PUT request
            if "playerupdate" not in request.data:
                return Response({
                    "code": 400,
                    "message": "playerupdate id is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecasePlayerUpdate.put(request)
            return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "DELETE":
            # Handle DELETE request
            if "playerupdate" not in request.data:
                return Response({
                    "code": 400,
                    "message": "playerupdate id is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecasePlayerUpdate.delete(request)
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