from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status as http_status
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .usecase import UsecaseMatchAttendance
from .models import MatchAttendance
from player.models import player
from pertandingan.models import pertandingan

@api_view(["POST", "GET", "PUT", "DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def match_attendance_handler(request):
    try:
        if request.method == "POST":
            required_fields = ['match', 'match_attendances']
            if not all(key in request.data for key in required_fields):
                return Response({
                    "code": 400,
                    "message": f"{', '.join(required_fields)} are required"
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

            # Validate match_attendances
            if not isinstance(request.data['match_attendances'], list):
                return Response({
                    "code": 400,
                    "message": "match_attendances must be a list"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            valid_statuses = [choice[0] for choice in MatchAttendance.STATUS_CHOICES]
            for attendance in request.data['match_attendances']:
                if not isinstance(attendance, dict):
                    return Response({
                        "code": 400,
                        "message": "Each match_attendance must be a dictionary"
                    }, status=http_status.HTTP_400_BAD_REQUEST)

                required_attendance_fields = ["player", "attendance_status"]
                if not all(key in attendance for key in required_attendance_fields):
                    return Response({
                        "code": 400,
                        "message": f"{', '.join(required_attendance_fields)} are required in each match_attendance"
                    }, status=http_status.HTTP_400_BAD_REQUEST)

                # Validate player exists
                try:
                    player.objects.get(player=attendance['player'])
                except player.DoesNotExist:
                    return Response({
                        "code": 400,
                        "message": f"Player with id {attendance['player']} does not exist"
                    }, status=http_status.HTTP_400_BAD_REQUEST)

                # Validate attendance_status
                if attendance['attendance_status'] not in valid_statuses:
                    return Response({
                        "code": 400,
                        "message": f"Invalid attendance_status: {attendance['attendance_status']}"
                    }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseMatchAttendance.post_match_attendance(request)
            return Response({
                "code": 200,
                "message": "Match attendances created successfully",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "GET":
            match_attendance = request.query_params.get("match_attendance")
            player_id = request.query_params.get("player")

            if match_attendance:
                data = UsecaseMatchAttendance.get_match_attendance(match_attendance)
                return Response({
                    "code": 200,
                    "message": "Match attendance retrieved successfully",
                    "data": data
                }, status=http_status.HTTP_200_OK)
            elif player_id:
                try:
                    player.objects.get(player=player_id)  # Validate player exists
                    data = UsecaseMatchAttendance.get_by_player(player_id)
                    return Response({
                        "code": 200,
                        "message": "Match attendance by player retrieved successfully",
                        "data": data
                    }, status=http_status.HTTP_200_OK)
                except player.DoesNotExist:
                    return Response({
                        "code": 404,
                        "message": f"Player with id {player_id} not found"
                    }, status=http_status.HTTP_404_NOT_FOUND)
            else:
                data = UsecaseMatchAttendance.get_all_match_attendance()
                return Response({
                    "code": 200,
                    "message": "All match attendances retrieved successfully",
                    "data": data
                }, status=http_status.HTTP_200_OK)

        elif request.method == "PUT":
            required_fields = ["match_attendance", "player"]
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

            # Validate attendance_status if provided
            if 'attendance_status' in request.data:
                valid_statuses = [choice[0] for choice in MatchAttendance.STATUS_CHOICES]
                if request.data['attendance_status'] not in valid_statuses:
                    return Response({
                        "code": 400,
                        "message": f"Invalid attendance_status: {request.data['attendance_status']}"
                    }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseMatchAttendance.put_match_attendance(request)
            return Response({
                "code": 200,
                "message": "Match attendance updated successfully",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "DELETE":
            if "match_attendance" not in request.data:
                return Response({
                    "code": 400,
                    "message": "match_attendance is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseMatchAttendance.delete_match_attendance(request)
            return Response({
                "code": 200,
                "message": "Match attendance deleted successfully",
                "data": data
            }, status=http_status.HTTP_200_OK)

    except ValidationError as e:
        return Response({
            "code": 400,
            "message": str(e)
        }, status=http_status.HTTP_400_BAD_REQUEST)
    except MatchAttendance.DoesNotExist:
        return Response({
            "code": 404,
            "message": "Match attendance not found"
        }, status=http_status.HTTP_404_NOT_FOUND)
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