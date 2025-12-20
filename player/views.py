from rest_framework.response import Response
from .usecase import UsecasePlayer
from rest_framework import status as http_status
from django.core.exceptions import ValidationError
from .models import player
from user.models import user
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)


@api_view(["POST", "GET", "PUT", "DELETE"])
@authentication_classes([])
@permission_classes([])
def player_handler(request):
    try:
        if request.method == "POST":
            print(request.POST)
            print(request.FILES)
            # Handle POST request
            required_fields = [
                "password",
                "email",
                "nomor_telepon",
                "nama",
                "posisi",
                "kewarganegaraan",
                "team",
                "nomor_punggung",
                "tinggi_badan",
                "berat_badan",
                "kelamin",
                "dob",
            ]
            if not all(field in request.POST for field in required_fields):
                return Response(
                    {
                        "code": 400,
                        "message": f"{', '.join(required_fields)} are required",
                    },
                    status=http_status.HTTP_400_BAD_REQUEST,
                )

            data = UsecasePlayer.post(request)
            return Response(
                {"code": 200, "message": "sukses", "data": data},
                status=http_status.HTTP_200_OK,
            )

        elif request.method == "GET":
            player_id = request.query_params.get("player")
            team_id = request.query_params.get("team")

            if player_id:
                data = UsecasePlayer.get(player_id)
            elif team_id:
                data = UsecasePlayer.get_all_players_by_team_id(team_id)
            else:
                data = UsecasePlayer.get_all()

            return Response(
                {"code": 200, "message": "sukses get player", "data": data},
                status=http_status.HTTP_200_OK,
            )

        elif request.method == "PUT":
            # Handle PUT request
            if "player" not in request.data:
                return Response(
                    {"code": 400, "message": "player id is required"},
                    status=http_status.HTTP_400_BAD_REQUEST,
                )

            data = UsecasePlayer.put(request)
            return Response(
                {"code": 200, "message": "sukses", "data": data},
                status=http_status.HTTP_200_OK,
            )

        elif request.method == "DELETE":

            # Handle DELETE request
            if "player" not in request.data:
                return Response(
                    {"code": 400, "message": "player id is required"},
                    status=http_status.HTTP_400_BAD_REQUEST,
                )

            data = UsecasePlayer.delete(request)
            return Response(
                {"code": 200, "message": "sukses", "data": data},
                status=http_status.HTTP_200_OK,
            )

    except ValidationError as e:
        return Response(
            {"code": 400, "message": str(e)}, status=http_status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {"code": 500, "message": str(e)},
            status=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # Hanya user yang terautentikasi yang bisa mengakses


@api_view(["POST", "GET"])
@authentication_classes([])  # Tambahkan autentikasi JWT
@permission_classes([])
def xendit_handler(request):
    try:
        if request.method == "POST":
            data = request.data  # gunakan .data, bukan .POST untuk JSON

            print("Webhook received:", data)
            status = request.data.get("status")
            external_id = request.data.get("external_id")
            paid_at = request.data.get("paid_at")
            payment_method = request.data.get("payment_method")
            payment_channel = request.data.get("payment_channel")

            playerInstance = player.objects.get(external_id=external_id)

            if status == "PAID":
                playerInstance.payment_status = "PAID"
                playerInstance.verification_status = "Verified"
                playerInstance.paid_at = paid_at
                playerInstance.payment_method = payment_method
                playerInstance.payment_channel = payment_channel
                playerInstance.save()
                return Response({"message": "Payment confirmed"}, status=200)

            elif status == "EXPIRED":
                userInstance = user.objects.filter(
                    email=playerInstance.user.email
                ).first()
                playerInstance.delete()
                if userInstance:
                    userInstance.delete()
                return Response(
                    {"message": "Invoice expired, data deleted"}, status=200
                )

            return Response({"message": "Ignored"}, status=200)
        elif request.method == "GET":
            external_id = request.query_params.get("external_id")
            playerInstance = player.objects.get(external_id=external_id)
            return Response(
                {
                    "code": 200,
                    "message": "sukses",
                    "status": playerInstance.payment_status,
                },
                status=http_status.HTTP_200_OK,
            )
    except ValidationError as e:
        return Response(
            {"code": 400, "message": str(e)}, status=http_status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {"code": 500, "message": str(e)},
            status=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
