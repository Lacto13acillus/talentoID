from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_date
import re
from .usecase import UsecasePertandingan
from .models import pertandingan
from formations.models import Formation


@api_view(["POST", "GET", "PUT", "DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def pertandingan_handler(request):
    def validate_time_format(time_str, field_name):
        """Validate time format as HH:MM or HH:MM:SS."""
        if not time_str:
            return
        pattern = r"^(?:[0-1][0-9]|2[0-3]):[0-5][0-9](?::[0-5][0-9])?$"
        if not re.match(pattern, time_str):
            raise ValidationError(
                f"Invalid {field_name} format. Use HH:MM or HH:MM:SS."
            )

    try:
        if request.method == "POST":
            required_fields = [
                "nama_pertandingan",
                "team_home",
                "team_away",
                "stadion",
                "season",
                "date",
                "start_time",
                "end_time",
            ]
            missing_fields = [
                field for field in required_fields if field not in request.data
            ]
            if missing_fields:
                return Response(
                    {
                        "code": 400,
                        "message": f"Missing required fields: {', '.join(missing_fields)}",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Validate time fields
            validate_time_format(request.data["start_time"], "start_time")
            validate_time_format(request.data["end_time"], "end_time")

            # Validate date format
            if request.data["date"] == "0000-00-00":
                return Response(
                    {
                        "code": 400,
                        "message": "Invalid date: '0000-00-00' is not a valid date",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not parse_date(request.data["date"]):
                return Response(
                    {"code": 400, "message": "Invalid date format. Use YYYY-MM-DD"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Validate formasi if provided
            if "formasi" in request.data:
                try:
                    Formation.objects.get(id_formasi=request.data["formasi"])
                except Formation.DoesNotExist:
                    return Response(
                        {
                            "code": 400,
                            "message": f"Formation with id {request.data['formasi']} does not exist",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            data = UsecasePertandingan.post(request)
            return Response(
                {"code": 200, "message": "sukses", "data": data},
                status=status.HTTP_200_OK,
            )

        elif request.method == "GET":
            match = request.query_params.get("match")
            coach_id = request.query_params.get("coach")
            player_id = request.query_params.get("player")
            team_id = request.query_params.get("team")

            if match:
                data = UsecasePertandingan.get(match)
                return Response(
                    {"code": 200, "message": "sukses", "data": data},
                    status=status.HTTP_200_OK,
                )
            elif coach_id:
                data = UsecasePertandingan.get_pertandingan_by_coach(coach_id)
                return Response(
                    {"code": 200, "message": "sukses", "data": data},
                    status=status.HTTP_200_OK,
                )
            elif player_id:

                data = UsecasePertandingan.get_pertandingan_by_player(player_id)
                return Response(
                    {"code": 200, "message": "sukses", "data": data},
                    status=status.HTTP_200_OK,
                )

            elif team_id:
                data = UsecasePertandingan.get_pertandingan_by_team(team_id)
                return Response(
                    {"code": 200, "message": "sukses by team", "data": data},
                    status=status.HTTP_200_OK,
                )
            else:
                data = UsecasePertandingan.get_all()
                return Response(
                    {"code": 200, "message": "sukses", "data": data},
                    status=status.HTTP_200_OK,
                )

        elif request.method == "PUT":
            if "match" not in request.data:
                return Response(
                    {"code": 400, "message": "match is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Validate time fields if provided
            if "start_time" in request.data:
                validate_time_format(request.data["start_time"], "start_time")
            if "end_time" in request.data:
                validate_time_format(request.data["end_time"], "end_time")

            # Validate date format if provided
            if "date" in request.data:
                if request.data["date"] == "0000-00-00":
                    return Response(
                        {
                            "code": 400,
                            "message": "Invalid date: '0000-00-00' is not a valid date",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                if not parse_date(request.data["date"]):
                    return Response(
                        {"code": 400, "message": "Invalid date format. Use YYYY-MM-DD"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            # Validate formasi if provided
            if "formasi" in request.data:
                try:
                    Formation.objects.get(id_formasi=request.data["formasi"])
                except Formation.DoesNotExist:
                    return Response(
                        {
                            "code": 400,
                            "message": f"Formation with id {request.data['formasi']} does not exist",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            data = UsecasePertandingan.put(request)
            return Response(
                {"code": 200, "message": "sukses", "data": data},
                status=status.HTTP_200_OK,
            )

        elif request.method == "DELETE":
            if "match" not in request.data:
                return Response(
                    {"code": 400, "message": "match is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            data = UsecasePertandingan.delete(request)
            return Response(
                {"code": 200, "message": "sukses", "data": data},
                status=status.HTTP_200_OK,
            )

    except ValidationError as e:
        return Response(
            {"code": 400, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
        )
    except pertandingan.DoesNotExist:
        return Response(
            {"code": 404, "message": "Pertandingan not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        return Response(
            {"code": 500, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def total_handler(request):
    try:
        coach_id = request.query_params.get("coach")
        if not coach_id:
            return Response(
                {"code": 400, "message": "coach_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = UsecasePertandingan.get_stats_by_coach(coach_id)
        return Response(
            {"code": 200, "message": "sukses", "data": data}, status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {
                "code": 404,
                "message": (
                    f"Pelatih dengan id {coach_id} tidak ditemukan"
                    if "not found" in str(e)
                    else str(e)
                ),
            },
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["PUT"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def readiness_handler(request):
    try:
        matchId = request.query_params.get("match")
        if not matchId:
            return Response(
                {"code": 400, "message": "match id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # data = UsecasePertandingan.get_stats_by_coach(matchId)
        result = UsecasePertandingan.set_ready_if_preparing(matchId)
        return Response(
            {"code": 200, "message": "sukses", "data": result},
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        return Response(
            {
                "code": 404,
                "message": (
                    f"Pertandingan dengan id {matchId} tidak ditemukan"
                    if "not found" in str(e)
                    else str(e)
                ),
            },
            status=status.HTTP_404_NOT_FOUND,
        )
