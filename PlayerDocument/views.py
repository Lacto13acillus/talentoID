# views/player_document_views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .usecase import UsecasePlayerDocument
from rest_framework import status as http_status
from django.core.exceptions import ValidationError

@api_view(["POST", "GET", "PUT", "DELETE"])
def player_document_handler(request):
    try:
        if request.method == "POST":
            required_fields = ["player", "jenis_dokumen"]
            if not all(field in request.POST for field in required_fields):
                return Response({
                    "code": 400,
                    "message": f"{', '.join(required_fields)} are required"
                }, status=http_status.HTTP_400_BAD_REQUEST)
            
            data = UsecasePlayerDocument.post(request)
            return Response({
                "code": 200,
                "message": "Player document created successfully",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "GET":
            player_document_id = request.query_params.get("playerdocument")
            player_id = request.query_params.get("player")  # Ubah ke "player" seperti attendance

            if player_document_id:
                data = UsecasePlayerDocument.get(player_document_id)
                return Response({
                    "code": 200,
                    "message": "Player document retrieved successfully",
                    "data": data
                }, status=http_status.HTTP_200_OK)
            elif player_id:
                data = UsecasePlayerDocument.get_by_player(player_id)
                return Response({
                    "code": 200,
                    "message": "Player documents by player retrieved successfully",
                    "data": data
                }, status=http_status.HTTP_200_OK)
            else:
                data = UsecasePlayerDocument.get_all()
                return Response({
                    "code": 200,
                    "message": "All player documents retrieved successfully",
                    "data": data
                }, status=http_status.HTTP_200_OK)

        elif request.method == "PUT":
            if "playerdocument" not in request.POST:
                return Response({
                    "code": 400,
                    "message": "playerdocument id is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecasePlayerDocument.put(request)
            return Response({
                "code": 200,
                "message": "Player document updated successfully",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "DELETE":
            if "playerdocument" not in request.POST:
                return Response({
                    "code": 400,
                    "message": "playerdocument id is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecasePlayerDocument.delete(request)
            return Response({
                "code": 200,
                "message": "Player document deleted successfully",
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