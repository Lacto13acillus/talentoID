# views/player_search_views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .usecase import UsecasePlayerSearch
from rest_framework import status as http_status
from django.core.exceptions import ValidationError
import json

@api_view(["POST", "GET", "PUT", "DELETE"])
def player_search_handler(request):
    try:
        if request.method == "POST":
            # Handle POST request
            required_fields = ["nama_player", "kata_kunci"]
            if not all(key in request.data for key in required_fields):
                return Response({
                    "code": 400,
                    "message": f"{', '.join(required_fields)} are required"
                }, status=http_status.HTTP_400_BAD_REQUEST)
            
            data = UsecasePlayerSearch.post(request)
            return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "GET":
            # Handle GET request
            try:
                player_search_id = request.query_params.get("id")
                if player_search_id:
                    # Existing single player search GET
                    data = UsecasePlayerSearch.get(player_search_id)
                    return Response({
                        "code": 200,
                        "message": "sukses",
                        "data": data
                    }, status=http_status.HTTP_200_OK)
                else:
                    # New GET ALL implementation
                    data = UsecasePlayerSearch.get_all()
                    return Response({
                        "code": 200,
                        "message": "sukses",
                        "data": data
                    }, status=http_status.HTTP_200_OK)
            except Exception as e:
                return Response({
                    "code": 404,
                    "message": str(e)
                }, status=http_status.HTTP_404_NOT_FOUND)

        elif request.method == "PUT":
            # Handle PUT request
            if "id" not in request.data:
                return Response({
                    "code": 400,
                    "message": "id is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecasePlayerSearch.put(request)
            return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "DELETE":
            # Handle DELETE request
            if "id" not in request.data:
                return Response({
                    "code": 400,
                    "message": "id is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecasePlayerSearch.delete(request)
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
