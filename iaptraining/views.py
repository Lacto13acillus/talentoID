from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .usecase import UsecaseIAPTraining
from rest_framework import status as http_status
from django.core.exceptions import ValidationError
from .models import iaptraining
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError
from training.models import training
from player.models import player

@api_view(["POST", "GET", "PUT", "DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def iaptraining_handler(request):
    print("Reached iaptraining_handler with method:", request.method)
    print("Request data:", request.data)
    try:
        if request.method == "POST":
            required_fields = ["player", "training", "technical", "physical", "goalkeeper", "social"]
            if not all(key in request.data for key in required_fields):
                return Response({
                    "code": 400,
                    "message": f"{', '.join(required_fields)} are required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            # Validate training exists
            try:
                training.objects.get(training=request.data['training'])
            except training.DoesNotExist:
                return Response({
                    "code": 400,
                    "message": f"Training with id {request.data['training']} does not exist"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            for category in ['technical', 'physical', 'goalkeeper', 'social']:
                data = request.data[category]
                if not isinstance(data, list):
                    return Response({
                        "code": 400,
                        "message": f"{category} must be a list"
                    }, status=http_status.HTTP_400_BAD_REQUEST)
                if data and len(data) % 3 != 0:  # Allow empty lists
                    return Response({
                        "code": 400,
                        "message": f"{category} must have length as a multiple of 3 (type, current_achieve, target)"
                    }, status=http_status.HTTP_400_BAD_REQUEST)
                valid_types = [choice[0] for choice in iaptraining.IAP_TYPE_CHOICES]
                for i in range(0, len(data), 3):
                    if data[i] not in valid_types:
                        return Response({
                            "code": 400,
                            "message": f"Invalid {category} type: {data[i]}"
                        }, status=http_status.HTTP_400_BAD_REQUEST)
                    try:
                        int(data[i + 1])
                        int(data[i + 2])
                    except ValueError:
                        return Response({
                            "code": 400,
                            "message": f"{category} current_achieve and target must be integers"
                        }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseIAPTraining.post(request)
            return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "GET":
            iaptraining_id = request.query_params.get("iaptraining")
            player_id = request.query_params.get("player")
            training_id = request.query_params.get("training")
            if iaptraining_id:
                data = UsecaseIAPTraining.get(iaptraining_id)
            elif player_id and training_id:
                try:
                    player.objects.get(player=player_id)  # Validate player exists
                    training.objects.get(training=training_id)
                    data = UsecaseIAPTraining.get_by_player_and_training(player_id, training_id)
                except player.DoesNotExist:
                    return Response({
                        "code": 404,
                        "message": f"Player with id {player_id} not found"
                    }, status=http_status.HTTP_404_NOT_FOUND)
                except training.DoesNotExist:
                    return Response({
                        "code": 404,
                        "message": f"Training with id {training_id} not found"
                    }, status=http_status.HTTP_404_NOT_FOUND)
            elif player_id:
                try:
                    player.objects.get(player=player_id)  # Validate player exists
                    data = UsecaseIAPTraining.get_by_player(player_id)
                except player.DoesNotExist:
                    return Response({
                        "code": 404,
                        "message": f"Player with id {player_id} not found"
                    }, status=http_status.HTTP_404_NOT_FOUND)
            else:
                data = UsecaseIAPTraining.get_all()
            
            return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "PUT":
            if "iaptraining" not in request.data:
                return Response({
                    "code": 400,
                    "message": "iaptraining id is required"
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

            data = UsecaseIAPTraining.put(request)
            return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "DELETE":
            if "iaptraining" not in request.data:
                return Response({
                    "code": 400,
                    "message": "iaptraining id is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseIAPTraining.delete(request)
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
    except iaptraining.DoesNotExist:
        return Response({
            "code": 404,
            "message": "IAPTraining not found"
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