from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework import status
from tournament.usecase import TournamentUsecase


def serialize_tournament(t):
    teams = [
        {
            "id_team": str(reg.team.team),
            "nama_team": reg.team.nama_team,
            "status_payment": reg.payment_status,
        }
        for reg in t.tournamentregistration_set.all()
    ]
    return {
        "id_tournament": str(t.id_tournament),
        "name": t.name,
        "description": t.description,
        "start_date": t.start_date,
        "end_date": t.end_date,
        "registration_open": t.registration_open,
        "registration_close": t.registration_close,
        "max_teams": t.max_teams,
        "location": t.location,
        "entry_fee": float(t.entry_fee) if t.entry_fee else 0,
        "status": t.status,
        "total_teams": len(teams),
        "teams": teams,
    }


@api_view(["POST", "GET", "PUT", "DELETE"])
@authentication_classes([])
@permission_classes([])
def tournament_handler(request):

    try:

        # CREATE
        if request.method == "POST":

            req = request.data

            tournament = TournamentUsecase.create_tournament(req)

            return Response(
                {
                    "code": 200,
                    "message": "sukses",
                    "data": serialize_tournament(tournament),
                },
                status=status.HTTP_200_OK,
            )

        # LIST
        if request.method == "GET":

            tournaments = TournamentUsecase.list_tournament()

            data = [serialize_tournament(t) for t in tournaments]

            return Response(
                {"code": 200, "message": "sukses", "data": data},
                status=status.HTTP_200_OK,
            )

        # UPDATE
        if request.method == "PUT":

            req = request.data
            id_tournament = req.get("id_tournament")

            tournament = TournamentUsecase.update_tournament(id_tournament, req)

            if not tournament:
                return Response(
                    {"code": 404, "message": "Tournament not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            return Response(
                {
                    "code": 200,
                    "message": "sukses",
                    "data": serialize_tournament(tournament),
                },
                status=status.HTTP_200_OK,
            )

        # DELETE
        if request.method == "DELETE":

            id_tournament = request.GET.get("id_tournament")

            deleted = TournamentUsecase.delete_tournament(id_tournament)

            if not deleted:
                return Response(
                    {"code": 404, "message": "Tournament not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            return Response(
                {
                    "code": 200,
                    "message": "sukses",
                    "data": {"message": "Tournament deleted"},
                },
                status=status.HTTP_200_OK,
            )

    except Exception as e:

        return Response(
            {"code": 500, "message": "error", "error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
