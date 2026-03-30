from rest_framework.response import Response
from .usecase import UsecasePlayer
from rest_framework import status as http_status
from django.core.exceptions import ValidationError
from .models import player
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from django.db import transaction
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware, is_naive

from tournament.models import TournamentRegistration


@api_view(["POST", "GET", "PUT", "DELETE"])
@authentication_classes([])
@permission_classes([])
def player_handler(request):
    try:
        if request.method == "POST":
            print(request.POST)
            print(request.FILES)
            # Handle POST request

            is_renewal = request.data.get("is_renewal", False)

            if is_renewal:
                if "player" not in request.data:
                    return Response(
                        {"code": 400, "message": "player is required for renewal"},
                        status=http_status.HTTP_400_BAD_REQUEST,
                    )

                data = UsecasePlayer.renew(request)
                return Response(
                    {"code": 200, "message": "renewal success", "data": data},
                    status=http_status.HTTP_200_OK,
                )

            required_fields = [
                "password",
                "email",
                "nomor_telepon",
                "nama",
                "posisi",
                "team",
                "nomor_punggung",
                "tinggi_badan",
                "berat_badan",
                "kelamin",
                "dob",
                "kode_kabupaten",
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
            print(request.data)
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
@authentication_classes([])
@permission_classes([])
def xendit_handler(request):

    try:

        # =========================
        # HANDLE POST (WEBHOOK)
        # =========================
        if request.method == "POST":

            data = request.data
            print("Webhook received:", data)

            status_payment = data.get("status")
            external_id = data.get("external_id")
            paid_at_raw = data.get("paid_at")
            payment_method = data.get("payment_method")
            payment_channel = data.get("payment_channel")

            # Try player table first, then tournament registration
            playerInstance = player.objects.filter(external_id=external_id).first()
            tournamentInstance = None

            if not playerInstance:
                tournamentInstance = TournamentRegistration.objects.filter(
                    external_id=external_id
                ).first()

            if not playerInstance and not tournamentInstance:
                return Response(
                    {"message": "Player or Registration not found"}, status=404
                )

            # =========================
            # PAYMENT SUCCESS
            # =========================
            if status_payment == "PAID":

                with transaction.atomic():

                    # ---- PLAYER TABLE ----
                    if playerInstance:

                        if playerInstance.payment_status in ["PAID", "SETTLED"]:
                            return Response(
                                {"message": "Already processed"}, status=200
                            )

                        paid_at = None
                        if paid_at_raw:
                            paid_at = parse_datetime(paid_at_raw)
                            if paid_at and is_naive(paid_at):
                                paid_at = make_aware(paid_at)

                        was_pending = playerInstance.payment_status == "PENDING"

                        playerInstance.payment_status = "PAID"
                        playerInstance.verification_status = "Verified"
                        playerInstance.paid_at = paid_at
                        playerInstance.payment_method = payment_method
                        playerInstance.payment_channel = payment_channel

                        if was_pending and not playerInstance.end_date:
                            pass  # is_first_payment already True by default

                        playerInstance.save()

                    # ---- TOURNAMENT REGISTRATION TABLE ----
                    elif tournamentInstance:

                        if tournamentInstance.payment_status in ["paid"]:
                            return Response(
                                {"message": "Already processed"}, status=200
                            )

                        tournamentInstance.payment_status = "paid"
                        tournamentInstance.payment_method = payment_method
                        tournamentInstance.payment_channel = payment_channel
                        tournamentInstance.save()

                return Response({"message": "Payment confirmed"}, status=200)

            else:
                return Response(
                    {"message": "Invoice expired but payment already processed"},
                    status=200,
                )

            return Response({"message": "Ignored"}, status=200)

        # =========================
        # HANDLE GET (CHECK STATUS)
        # =========================
        elif request.method == "GET":

            external_id = request.query_params.get("external_id")

            # Try player table first, then tournament registration
            playerInstance = player.objects.filter(external_id=external_id).first()

            if playerInstance:
                return Response(
                    {
                        "code": 200,
                        "message": "sukses",
                        "type": "player",
                        "payment_status": playerInstance.payment_status,
                        "membership_status": playerInstance.membership_status,
                        "end_date": playerInstance.end_date,
                        "is_first_payment": playerInstance.is_first_payment,
                    },
                    status=http_status.HTTP_200_OK,
                )

            tournamentInstance = TournamentRegistration.objects.filter(
                invoice_id=external_id
            ).first()

            if tournamentInstance:
                return Response(
                    {
                        "code": 200,
                        "message": "sukses",
                        "type": "tournament_registration",
                        "payment_status": tournamentInstance.payment_status,
                        "tournament": str(tournamentInstance.tournament.id),
                        "team": str(tournamentInstance.team.id),
                    },
                    status=http_status.HTTP_200_OK,
                )

            return Response({"message": "Not found"}, status=404)

    except Exception as e:
        return Response(
            {"code": 500, "message": str(e)},
            status=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
