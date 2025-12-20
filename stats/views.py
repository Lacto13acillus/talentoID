from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status as http_status
from django.core.exceptions import ValidationError
from .usecase import UsecaseStats
from .models import stats
from player.models import player
from pertandingan.models import pertandingan

@api_view(["POST", "GET", "PUT", "DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def stats_handler(request):
    try:
        if request.method == "POST":
            required_fields = ["match", "stats_list"]
            if not all(key in request.data for key in required_fields):
                return Response({
                    "code": 400,
                    "message": f"{', '.join(required_fields)} are required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            # Validate match exists
            try:
                pertandingan.objects.get(match=request.data['match'])
            except pertandingan.DoesNotExist:
                return Response({
                    "code": 400,
                    "message": f"Match with id {request.data['match']} does not exist"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            # Validate stats_list
            if not isinstance(request.data['stats_list'], list):
                return Response({
                    "code": 400,
                    "message": "stats_list must be a list"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            for stat in request.data['stats_list']:
                if not isinstance(stat, dict):
                    return Response({
                        "code": 400,
                        "message": "Each stats entry must be a dictionary"
                    }, status=http_status.HTTP_400_BAD_REQUEST)

                required_stat_fields = ["player", "position_played", "minutes_played", "overall_rating"]
                if not all(key in stat for key in required_stat_fields):
                    return Response({
                        "code": 400,
                        "message": f"{', '.join(required_stat_fields)} are required in each stats entry"
                    }, status=http_status.HTTP_400_BAD_REQUEST)

                # Validate player exists
                try:
                    player.objects.get(player=stat['player'])
                except player.DoesNotExist:
                    return Response({
                        "code": 400,
                        "message": f"Player with id {stat['player']} does not exist"
                    }, status=http_status.HTTP_400_BAD_REQUEST)

                # Validate minutes_played
                if not isinstance(stat['minutes_played'], int) or stat['minutes_played'] < 0:
                    return Response({
                        "code": 400,
                        "message": "minutes_played must be a non-negative integer"
                    }, status=http_status.HTTP_400_BAD_REQUEST)

                # Validate overall_rating
                if not isinstance(stat['overall_rating'], int) or stat['overall_rating'] < 0 or stat['overall_rating'] > 10:
                    return Response({
                        "code": 400,
                        "message": "overall_rating must be an integer between 0 and 10"
                    }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseStats.post(request)
            return Response({
                "code": 201,
                "message": "Stats created successfully",
                "data": data
            }, status=http_status.HTTP_201_CREATED)

        elif request.method == "GET":
            stats_id = request.query_params.get("stats")
            player_id = request.query_params.get("player")

            if stats_id:
                data = UsecaseStats.get(stats_id)
                return Response({
                    "code": 200,
                    "message": "Stats retrieved successfully",
                    "data": data
                }, status=http_status.HTTP_200_OK)
            elif player_id:
                try:
                    player.objects.get(player=player_id)  # Validate player exists
                    data = UsecaseStats.get_by_player(player_id)
                    return Response({
                        "code": 200,
                        "message": "Stats by player retrieved successfully",
                        "data": data
                    }, status=http_status.HTTP_200_OK)
                except player.DoesNotExist:
                    return Response({
                        "code": 404,
                        "message": f"Player with id {player_id} not found"
                    }, status=http_status.HTTP_404_NOT_FOUND)
            else:
                data = UsecaseStats.get_all()
                return Response({
                    "code": 200,
                    "message": "All stats retrieved successfully",
                    "data": data
                }, status=http_status.HTTP_200_OK)

        elif request.method == "PUT":
            required_fields = ["stats", "match", "player"]
            if not all(key in request.data for key in required_fields):
                return Response({
                    "code": 400,
                    "message": f"{', '.join(required_fields)} are required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            # Validate match exists
            try:
                pertandingan.objects.get(match=request.data['match'])
            except pertandingan.DoesNotExist:
                return Response({
                    "code": 400,
                    "message": f"Match with id {request.data['match']} does not exist"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            # Validate player exists
            try:
                player.objects.get(player=request.data['player'])
            except player.DoesNotExist:
                return Response({
                    "code": 400,
                    "message": f"Player with id {request.data['player']} does not exist"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            # Validate minutes_played if provided
            if 'minutes_played' in request.data:
                if not isinstance(request.data['minutes_played'], int) or request.data['minutes_played'] < 0:
                    return Response({
                        "code": 400,
                        "message": "minutes_played must be a non-negative integer"
                    }, status=http_status.HTTP_400_BAD_REQUEST)

            # Validate overall_rating if provided
            if 'overall_rating' in request.data:
                if not isinstance(request.data['overall_rating'], int) or request.data['overall_rating'] < 0 or request.data['overall_rating'] > 10:
                    return Response({
                        "code": 400,
                        "message": "overall_rating must be an integer between 0 and 10"
                    }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseStats.put(request)
            return Response({
                "code": 200,
                "message": "Stats updated successfully",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "DELETE":
            if "stats" not in request.data:
                return Response({
                    "code": 400,
                    "message": "stats id is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseStats.delete(request)
            return Response({
                "code": 200,
                "message": "Stats deleted successfully",
                "data": data
            }, status=http_status.HTTP_200_OK)

    except ValidationError as e:
        return Response({
            "code": 400,
            "message": str(e)
        }, status=http_status.HTTP_400_BAD_REQUEST)
    except stats.DoesNotExist:
        return Response({
            "code": 404,
            "message": "Stats not found"
        }, status=http_status.HTTP_404_NOT_FOUND)
    except player.DoesNotExist:
        return Response({
            "code": 404,
            "message": "Player not found"
        }, status=http_status.HTTP_404_NOT_FOUND)
    except pertandingan.DoesNotExist:
        return Response({
            "code": 404,
            "message": "Match not found"
        }, status=http_status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            "code": 500,
            "message": f"Internal server error: {str(e)}"
        }, status=http_status.HTTP_500_INTERNAL_SERVER_ERROR)