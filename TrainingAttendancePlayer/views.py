from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status as http_status
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .usecase import UsecaseTrainingAttendancePlayer
from .models import TrainingAttendancePlayer
from player.models import player
from training.models import training

@api_view(["POST", "GET", "PUT", "DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def training_attendance_player_handler(request):
    try:
        if request.method == "POST":
            required_fields = ["player", "training", "status"]
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

            data = UsecaseTrainingAttendancePlayer.post_training_attendance_player(request)
            return Response({
                "code": 200,
                "message": "Training attendance player created successfully",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "GET":
            trainingattendance_id = request.query_params.get("trainingattendance_id")
            player_id = request.query_params.get("player")
            training_id = request.query_params.get("training")

            if trainingattendance_id:
                data = UsecaseTrainingAttendancePlayer.get_training_attendance_player(trainingattendance_id)
                return Response({
                    "code": 200,
                    "message": "Training attendance player retrieved successfully",
                    "data": data
                }, status=http_status.HTTP_200_OK)
            elif player_id:
                try:
                    player.objects.get(player=player_id)  # Validate player exists
                    data = UsecaseTrainingAttendancePlayer.get_by_player(player_id)
                    return Response({
                        "code": 200,
                        "message": "Training attendance player by player retrieved successfully",
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
                    data = UsecaseTrainingAttendancePlayer.get_by_training(training_id)
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
                data = UsecaseTrainingAttendancePlayer.get_all_training_attendance_player()
                return Response({
                    "code": 200,
                    "message": "All training attendance players retrieved successfully",
                    "data": data
                }, status=http_status.HTTP_200_OK)

        elif request.method == "PUT":
            required_fields = ["trainingattendance_id", "player"]
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

            data = UsecaseTrainingAttendancePlayer.put_training_attendance_player(request)
            return Response({
                "code": 200,
                "message": "Training attendance player updated successfully",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "DELETE":
            if "trainingattendance_id" not in request.data:
                return Response({
                    "code": 400,
                    "message": "trainingattendance_id is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseTrainingAttendancePlayer.delete_training_attendance_player(request)
            return Response({
                "code": 200,
                "message": "Training attendance player deleted successfully",
                "data": data
            }, status=http_status.HTTP_200_OK)

    except ValidationError as e:
        return Response({
            "code": 400,
            "message": str(e)
        }, status=http_status.HTTP_400_BAD_REQUEST)
    except TrainingAttendancePlayer.DoesNotExist:
        return Response({
            "code": 404,
            "message": "Training attendance player not found"
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