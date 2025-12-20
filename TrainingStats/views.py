from rest_framework.decorators import api_view
from rest_framework.response import Response
from .usecase import UsecaseTrainingStats
from rest_framework import status as http_status
from django.core.exceptions import ValidationError

@api_view(["POST", "GET", "PUT", "DELETE"])
def trainingstats_handler(request):
    try:
        if request.method == "POST":
            required_fields = ["training", "player", "position_played", "minutes_played", "overall_rating"]
            if not all(key in request.data for key in required_fields):
                return Response({
                    "code": 400,
                    "message": f"{', '.join(required_fields)} are required"
                }, status=http_status.HTTP_400_BAD_REQUEST)
            
            data = UsecaseTrainingStats.post(request)
            return Response({
                "code": 200,
                "message": "Training stats created successfully",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "GET":
            stats_id = request.query_params.get("stats")
            player_id = request.query_params.get("player")  # Ubah ke "player" seperti attendance

            if stats_id:
                data = UsecaseTrainingStats.get(stats_id)
                return Response({
                    "code": 200,
                    "message": "Training stats retrieved successfully",
                    "data": data
                }, status=http_status.HTTP_200_OK)
            elif player_id:
                data = UsecaseTrainingStats.get_by_player(player_id)
                return Response({
                    "code": 200,
                    "message": "Training stats by player retrieved successfully",
                    "data": data
                }, status=http_status.HTTP_200_OK)
            else:
                data = UsecaseTrainingStats.get_all()
                return Response({
                    "code": 200,
                    "message": "All training stats retrieved successfully",
                    "data": data
                }, status=http_status.HTTP_200_OK)

        elif request.method == "PUT":
            required_fields = ["stats", "training", "player"]
            if not all(key in request.data for key in required_fields):
                return Response({
                    "code": 400,
                    "message": f"{', '.join(required_fields)} are required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseTrainingStats.put(request)
            return Response({
                "code": 200,
                "message": "Training stats updated successfully",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "DELETE":
            if "stats" not in request.data:
                return Response({
                    "code": 400,
                    "message": "stats id is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseTrainingStats.delete(request)
            return Response({
                "code": 200,
                "message": "Training stats deleted successfully",
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