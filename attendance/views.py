from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status as http_status
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .usecase import UsecaseAttendance
from .models import attendance
from player.models import player
from training.models import training

@api_view(["POST", "GET", "PUT", "DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def attendance_handler(request):
    try:
        if request.method == "POST":
            required_fields = ['training', 'attendances']
            if not all(key in request.data for key in required_fields):
                return Response({
                    "code": 400,
                    "message": f"{', '.join(required_fields)} are required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            # Validate training if provided
            if 'training' in request.data:
                try:
                    training.objects.get(training=request.data['training'])
                except training.DoesNotExist:
                    return Response({
                        "code": 400,
                        "message": f"Training with id {request.data['training']} does not exist"
                    }, status=http_status.HTTP_400_BAD_REQUEST)

            # Validate attendances
            if not isinstance(request.data['attendances'], list):
                return Response({
                    "code": 400,
                    "message": "attendances must be a list"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            valid_statuses = [choice[0] for choice in attendance.STATUS_CHOICES]
            for att in request.data['attendances']:
                if not isinstance(att, dict):
                    return Response({
                        "code": 400,
                        "message": "Each attendance must be a dictionary"
                    }, status=http_status.HTTP_400_BAD_REQUEST)

                required_attendance_fields = ["player", "attendance_status"]
                if not all(key in att for key in required_attendance_fields):
                    return Response({
                        "code": 400,
                        "message": f"{', '.join(required_attendance_fields)} are required in each attendance"
                    }, status=http_status.HTTP_400_BAD_REQUEST)

                # Validate player exists
                try:
                    player.objects.get(player=att['player'])
                except player.DoesNotExist:
                    return Response({
                        "code": 400,
                        "message": f"Player with id {att['player']} does not exist"
                    }, status=http_status.HTTP_400_BAD_REQUEST)

                # Validate attendance_status
                if att['attendance_status'] not in valid_statuses:
                    return Response({
                        "code": 400,
                        "message": f"Invalid attendance_status: {att['attendance_status']}. Must be one of: {', '.join(valid_statuses)}"
                    }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseAttendance.post_training(request)
            return Response({
                "code": 201,
                "message": "Training attendances created successfully",
                "data": data
            }, status=http_status.HTTP_201_CREATED)

        elif request.method == "GET":
            attendance_id = request.query_params.get("attendance")
            player_id = request.query_params.get("player")
            training_id = request.query_params.get("training")

            if attendance_id:
                data = UsecaseAttendance.get_training(attendance_id)
                return Response({
                    "code": 200,
                    "message": "Training attendance retrieved successfully",
                    "data": data
                }, status=http_status.HTTP_200_OK)
            elif player_id:
                try:
                    player.objects.get(player=player_id)  # Validate player exists
                    data = UsecaseAttendance.get_by_player(player_id)
                    return Response({
                        "code": 200,
                        "message": "Attendance by player retrieved successfully",
                        "data": data
                    }, status=http_status.HTTP_200_OK)
                except player.DoesNotExist:
                    return Response({
                        "code": 404,
                        "message": f"Player with id {player_id} not found"
                    }, status=http_status.HTTP_404_NOT_FOUND)
            elif training_id:
                try:
                    training.objects.get(training=training_id)  # Validate training exists
                    data = UsecaseAttendance.get_by_training(training_id)
                    return Response({
                        "code": 200,
                        "message": "Training attendance player by training retrieved successfully",
                        "data": data
                    }, status=http_status.HTTP_200_OK)
                except training.DoesNotExist:
                    return Response({
                        "code": 404,
                        "message": f"Training with id {training_id} not found"
                    }, status=http_status.HTTP_404_NOT_FOUND)
            else:
                data = UsecaseAttendance.get_all_training()
                return Response({
                    "code": 200,
                    "message": "All training attendances retrieved successfully",
                    "data": data
                }, status=http_status.HTTP_200_OK)

        elif request.method == "PUT":
            required_fields = ["attendance", "player"]
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

            # Validate training if provided
            if 'training' in request.data:
                try:
                    training.objects.get(training=request.data['training'])
                except training.DoesNotExist:
                    return Response({
                        "code": 400,
                        "message": f"Training with id {request.data['training']} does not exist"
                    }, status=http_status.HTTP_400_BAD_REQUEST)

            # Validate attendance_status if provided
            if 'attendance_status' in request.data:
                valid_statuses = [choice[0] for choice in attendance.STATUS_CHOICES]
                if request.data['attendance_status'] not in valid_statuses:
                    return Response({
                        "code": 400,
                        "message": f"Invalid attendance_status: {request.data['attendance_status']}. Must be one of: {', '.join(valid_statuses)}"
                    }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseAttendance.put_training(request)
            return Response({
                "code": 200,
                "message": "Training attendance updated successfully",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "DELETE":
            if "attendance" not in request.data:
                return Response({
                    "code": 400,
                    "message": "attendance is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseAttendance.delete_training(request)
            return Response({
                "code": 200,
                "message": "Training attendance deleted successfully",
                "data": data
            }, status=http_status.HTTP_200_OK)

    except ValidationError as e:
        return Response({
            "code": 400,
            "message": str(e)
        }, status=http_status.HTTP_400_BAD_REQUEST)
    except attendance.DoesNotExist:
        return Response({
            "code": 404,
            "message": "Attendance not found"
        }, status=http_status.HTTP_404_NOT_FOUND)
    except player.DoesNotExist:
        return Response({
            "code": 404,
            "message": "Player not found"
        }, status=http_status.HTTP_404_NOT_FOUND)
    except training.DoesNotExist:
        return Response({
            "code": 404,
            "message": "Training not found"
        }, status=http_status.HTTP_404_NOT_FOUND)
    except IntegrityError as e:
        return Response({
            "code": 400,
            "message": f"Database integrity error: {str(e)}"
        }, status=http_status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            "code": 500,
            "message": f"Internal server error: {str(e)}"
        }, status=http_status.HTTP_500_INTERNAL_SERVER_ERROR)
