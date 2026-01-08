from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from .usecase import UsecaseTeam
from django.core.exceptions import ValidationError


@api_view(["POST", "GET", "PUT", "DELETE"])
@authentication_classes([])  # Tambahkan autentikasi JWT
@permission_classes([])  # Hanya user yang terautentikasi yang bisa mengakses
def team_handler(request):
    try:
        if request.method == "POST":
            print(request.data)
            required_fields = ["nama_team", "coach", "kategori_team"]
            if not all(key in request.data for key in required_fields):
                return Response(
                    {
                        "code": 400,
                        "message": "nama_team, coach, and kategori_team are required",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if "logo_team" not in request.FILES:
                return Response(
                    {"code": 400, "message": "logo_team is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            data = UsecaseTeam.post(request)
            return Response(
                {"code": 200, "message": "sukses", "data": data},
                status=status.HTTP_200_OK,
            )

        elif request.method == "GET":
            team_id = request.query_params.get("team")
            coach_id = request.query_params.get("coach")

            if team_id:
                # Jika ada team_id, ambil data spesifik
                data = UsecaseTeam.get(team_id)
            elif coach_id:
                # Jika ada coach_id, ambil semua tim yang dilatih oleh coach tersebut
                data = UsecaseTeam.get_all_teams_by_coach_id(coach_id)
            else:
                # Jika tidak ada parameter, ambil semua tim
                data = UsecaseTeam.get_all()

            return Response(
                {"code": 200, "message": "sukses", "data": data},
                status=status.HTTP_200_OK,
            )

        elif request.method == "PUT":
            if "team" not in request.data:
                return Response(
                    {"code": 400, "message": "team is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            data = UsecaseTeam.put(request)
            return Response(
                {"code": 200, "message": "sukses", "data": data},
                status=status.HTTP_200_OK,
            )

        elif request.method == "DELETE":
            if "team" not in request.data:
                return Response(
                    {"code": 400, "message": "team is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            data = UsecaseTeam.delete(request)
            return Response(
                {"code": 200, "message": "sukses", "data": data},
                status=status.HTTP_200_OK,
            )

    except ValidationError as e:
        return Response(
            {"code": 400, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        print("Error:", str(e))
        return Response(
            {"code": 500, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def total_team_handler(request):
    try:
        if request.method == "GET":
            team_id = request.query_params.get("team")

            if not team_id:
                return Response(
                    {"code": 400, "message": "team is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            data = UsecaseTeam.get_team_stats_by_team_id(team_id)
            return Response(
                {"code": 200, "message": "sukses", "data": data},
                status=status.HTTP_200_OK,
            )

    except ValidationError as e:
        return Response(
            {"code": 400, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {"code": 500, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
