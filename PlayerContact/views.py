# views/player_contact_views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .usecase import UsecasePlayerContact
from rest_framework import status as http_status
from django.core.exceptions import ValidationError

@api_view(["POST", "GET", "PUT", "DELETE"])
def player_contact_handler(request):
    try:
        if request.method == "POST":
            required_fields = ["player", "nama_panggilan", "nomor_hp", "nama_orangtua", "nomor_orangtua",
                               "nama_kontak_darurat", "kontak_darurat"]
            if not all(key in request.data for key in required_fields):
                return Response({
                    "code": 400,
                    "message": f"{', '.join(required_fields)} are required"
                }, status=http_status.HTTP_400_BAD_REQUEST)
            
            data = UsecasePlayerContact.post(request)
            return Response({
                "code": 200,
                "message": "Player contact created successfully",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "GET":
            player_contact_id = request.query_params.get("playercontact")
            player_id = request.query_params.get("player")

            if player_contact_id:
                data = UsecasePlayerContact.get(player_contact_id)
                return Response({
                    "code": 200,
                    "message": "Player contact retrieved successfully",
                    "data": data
                }, status=http_status.HTTP_200_OK)
            elif player_id:
                data = UsecasePlayerContact.get_by_player(player_id)
                if data is None:
                    return Response({
                        "code": 404,
                        "message": "No contact found for this player"
                    }, status=http_status.HTTP_404_NOT_FOUND)
                return Response({
                    "code": 200,
                    "message": "Player contact by player retrieved successfully",
                    "data": data
                }, status=http_status.HTTP_200_OK)
            else:
                data = UsecasePlayerContact.get_all()
                return Response({
                    "code": 200,
                    "message": "All player contacts retrieved successfully",
                    "data": data
                }, status=http_status.HTTP_200_OK)

        elif request.method == "PUT":
            if "playercontact" not in request.data:
                return Response({
                    "code": 400,
                    "message": "playercontact id is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecasePlayerContact.put(request)
            return Response({
                "code": 200,
                "message": "Player contact updated successfully",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "DELETE":
            if "playercontact" not in request.data:
                return Response({
                    "code": 400,
                    "message": "playercontact id is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecasePlayerContact.delete(request)
            return Response({
                "code": 200,
                "message": "Player contact deleted successfully",
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