from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status as http_status
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .usecase import UsecaseMatchAttendancePlayer
from .models import MatchAttendancePlayer
from player.models import player
from pertandingan.models import pertandingan

@api_view(["POST", "GET", "PUT", "DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def match_attendance_player_handler(request):
    try:
        if request.method == "POST":
            required_fields = ["player", "status"]
            if not all(key in request.data for key in required_fields):
                return Response({
                    "code": 400,
                    "message": f"{', '.join(required_fields)} are required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            # Validate player exists
            try:
                player.objects.get(player=request.data['player'])
            except player.DoesNotExist:
                return Response({
                    "code": 400,
                    "message": f"Player with id {request.data['player']} does not exist"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            # Validate match if provided
            if 'match' in request.data:
                try:
                    pertandingan.objects.get(match=request.data['match'])
                except pertandingan.DoesNotExist:
                    return Response({
                        "code": 400,
                        "message": f"Match with id {request.data['match']} does not exist"
                    }, status=http_status.HTTP_400_BAD_REQUEST)

            # Validate status is a boolean
            if not isinstance(request.data['status'], bool):
                return Response({
                    "code": 400,
                    "message": "status must be a boolean (true or false)"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            # Validate reason_absent if status is False (must be present and non-empty)
            if not request.data['status']:
                reason_absent = request.data.get('reason_absent', '').strip()
                if not reason_absent:
                    return Response({
                        "code": 400,
                        "message": "reason_absent is required and cannot be empty when the player is absent"
                    }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseMatchAttendancePlayer.post_match_attendance_player(request)
            return Response({
                "code": 200,
                "message": "Match attendance player created successfully",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "GET":
            attendance_id = request.query_params.get("attendance_id")
            player_id = request.query_params.get("player")
            match_id = request.query_params.get("match")

            if attendance_id:
                data = UsecaseMatchAttendancePlayer.get_match_attendance_player(attendance_id)
                return Response({
                    "code": 200,
                    "message": "Match attendance player retrieved successfully",
                    "data": data
                }, status=http_status.HTTP_200_OK)
            elif player_id:
                try:
                    player.objects.get(player=player_id)  # Validate player exists
                    data = UsecaseMatchAttendancePlayer.get_by_player(player_id)
                    return Response({
                        "code": 200,
                        "message": "Match attendance player by player retrieved successfully",
                        "data": data
                    }, status=http_status.HTTP_200_OK)
                except player.DoesNotExist:
                    return Response({
                        "code": 404,
                        "message": f"Player with id {player_id} not found"
                    }, status=http_status.HTTP_404_NOT_FOUND)
            elif match_id:
                try:
                    pertandingan.objects.get(match=match_id)  # Validate match exists
                    data = UsecaseMatchAttendancePlayer.get_by_match_id(match_id)
                    return Response({
                        "code": 200,
                        "message": "Match attendance player by match retrieved successfully",
                        "data": data
                    }, status=http_status.HTTP_200_OK)
                except pertandingan.DoesNotExist:
                    return Response({
                        "code": 404,
                        "message": f"Match with id {match_id} not found"
                    }, status=http_status.HTTP_404_NOT_FOUND)
            else:
                data = UsecaseMatchAttendancePlayer.get_all_match_attendance_player()
                return Response({
                    "code": 200,
                    "message": "All match attendance players retrieved successfully",
                    "data": data
                }, status=http_status.HTTP_200_OK)

        elif request.method == "PUT":
            required_fields = ["attendance_id", "player"]
            if not all(key in request.data for key in required_fields):
                return Response({
                    "code": 400,
                    "message": f"{', '.join(required_fields)} are required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            # Validate player exists
            try:
                player.objects.get(player=request.data['player'])
            except player.DoesNotExist:
                return Response({
                    "code": 400,
                    "message": f"Player with id {request.data['player']} does not exist"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            # Validate match if provided
            if 'match' in request.data:
                try:
                    pertandingan.objects.get(match=request.data['match'])
                except pertandingan.DoesNotExist:
                    return Response({
                        "code": 400,
                        "message": f"Match with id {request.data['match']} does not exist"
                    }, status=http_status.HTTP_400_BAD_REQUEST)

            # Validate status if provided
            if 'status' in request.data:
                if not isinstance(request.data['status'], bool):
                    return Response({
                        "code": 400,
                        "message": "status must be a boolean (true or false)"
                    }, status=http_status.HTTP_400_BAD_REQUEST)

                # Validate reason_absent if status is False (must be present and non-empty)
                if not request.data['status']:
                    reason_absent = request.data.get('reason_absent', '').strip()
                    if not reason_absent:
                        return Response({
                            "code": 400,
                            "message": "reason_absent is required and cannot be empty when the player is absent"
                        }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseMatchAttendancePlayer.put_match_attendance_player(request)
            return Response({
                "code": 200,
                "message": "Match attendance player updated successfully",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "DELETE":
            if "attendance_id" not in request.data:
                return Response({
                    "code": 400,
                    "message": "attendance_id is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseMatchAttendancePlayer.delete_match_attendance_player(request)
            return Response({
                "code": 200,
                "message": "Match attendance player deleted successfully",
                "data": data
            }, status=http_status.HTTP_200_OK)

    except ValidationError as e:
        return Response({
            "code": 400,
            "message": str(e)
        }, status=http_status.HTTP_400_BAD_REQUEST)
    except MatchAttendancePlayer.DoesNotExist:
        return Response({
            "code": 404,
            "message": "Match attendance player not found"
        }, status=http_status.HTTP_404_NOT_FOUND)
    except ValueError as e:
        return Response({
            "code": 400,
            "message": str(e)
        }, status=http_status.HTTP_400_BAD_REQUEST)
    except IntegrityError as e:
        return Response({
            "code": 400,
            "message": f"Database integrity error: {str(e)}"
        }, status=http_status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            "code": 500,
            "message": str(e)
        }, status=http_status.HTTP_500_INTERNAL_SERVER_ERROR)