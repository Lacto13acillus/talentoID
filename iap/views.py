from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .usecase import UsecaseIAP
from rest_framework import status as http_status
from django.core.exceptions import ValidationError
from .models import iap
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError
from pertandingan.models import pertandingan
from player.models import player

@api_view(["POST", "GET", "PUT", "DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def iap_handler(request):
    try:
        if request.method == "POST":
            required_fields = ["player", "match", "iaps"]
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

            # Validate technical, physical, goalkeeper, and social data
            # for category in ['technical', 'physical', 'goalkeeper', 'social']:
            #     data = request.data.get(category, [])
            #     if not isinstance(data, list) or len(data) % 3 != 0:
            #         return Response({
            #             "code": 400,
            #             "message": f"{category} must be a list with length as a multiple of 3 (type, current_achieve, target)"
            #         }, status=http_status.HTTP_400_BAD_REQUEST)
            #     valid_types = [choice[0] for choice in iap.IAP_TYPE_CHOICES]
            #     for i in range(0, len(data), 3):
            #         if data[i] not in valid_types:
            #             return Response({
            #                 "code": 400,
            #                 "message": f"Invalid {category} type: {data[i]}"
            #             }, status=http_status.HTTP_400_BAD_REQUEST)
            #         try:
            #             int(data[i + 1])
            #             int(data[i + 2])
            #         except ValueError:
            #             return Response({
            #                 "code": 400,
            #                 "message": f"{category} current_achieve and target must be integers"
            #             }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseIAP.post(request)
            return Response({
                "code": 201,
                "message": "sukses",
                "data": data
            }, status=http_status.HTTP_201_CREATED)

        elif request.method == "GET":
            iap_id = request.query_params.get("iap")
            player_id = request.query_params.get("player")
            match_id = request.query_params.get("match")

            if iap_id:
                data = UsecaseIAP.get(iap_id)
            elif player_id and match_id:
                try:
                    player.objects.get(player=player_id)  # Validate player exists
                    pertandingan.objects.get(match=match_id)
                    data = UsecaseIAP.get_by_player_and_match(player_id, match_id)
                except player.DoesNotExist:
                    return Response({
                        "code": 404,
                        "message": f"Player with id {player_id} not found"
                    }, status=http_status.HTTP_404_NOT_FOUND)
                except pertandingan.DoesNotExist:
                    return Response({
                        "code": 404,
                        "message": f"Match with id {match_id} not found"
                    }, status=http_status.HTTP_404_NOT_FOUND)
            else:
                data = UsecaseIAP.get_all()

            return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "PUT":
            required_fields = ["iap", "player"]
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

            # Validate player exists
            try:
                player.objects.get(player=request.data['player'])
            except player.DoesNotExist:
                return Response({
                    "code": 400,
                    "message": f"Player with id {request.data['player']} does not exist"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            # Validate category and type if provided
            if 'category' in request.data:
                valid_categories = [choice[0] for choice in iap.IAP_CATEGORY_CHOICES]
                if request.data['category'] not in valid_categories:
                    return Response({
                        "code": 400,
                        "message": f"Invalid category: {request.data['category']}"
                    }, status=http_status.HTTP_400_BAD_REQUEST)
            if 'type' in request.data:
                valid_types = [choice[0] for choice in iap.IAP_TYPE_CHOICES]
                if request.data['type'] not in valid_types:
                    return Response({
                        "code": 400,
                        "message": f"Invalid type: {request.data['type']}"
                    }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseIAP.put(request)
            return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "DELETE":
            if "iap" not in request.data:
                return Response({
                    "code": 400,
                    "message": "iap id is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseIAP.delete(request)
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
    except iap.DoesNotExist:
        return Response({
            "code": 404,
            "message": "IAP not found"
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
