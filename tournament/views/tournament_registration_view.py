from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)

from rest_framework.response import Response
from rest_framework import status

from tournament.usecases.tournament_registration_usecase import (
    TournamentRegistrationUsecase,
)


@api_view(["POST", "GET", "PUT", "DELETE"])
@authentication_classes([])
@permission_classes([])
def tournament_registration_handler(request):

    try:

        # CREATE
        if request.method == "POST":

            req = request.data

            result = TournamentRegistrationUsecase.create_registration(req)

            return Response(
                {
                    "code": 200,
                    "message": "sukses",
                    "data": result,
                },
                status=status.HTTP_200_OK,
            )

        # LIST
        if request.method == "GET":

            team_id = request.query_params.get("team_id")
            registrations = TournamentRegistrationUsecase.list_registration(team_id)

            data = [
                {
                    "id_registration": str(r.id_registration),
                    "tournament": r.tournament.name,
                    "team": r.team.nama_team,
                    "registration_date": r.registration_date,
                    "payment": {
                        "status": r.payment_status,
                        "channel": r.payment_channel,
                        "method": r.payment_method,
                        "invoice_id": r.invoice_id,
                        "invoice_url": r.invoice_url,
                        "expiry_date": r.expiry_date,
                        "amount": {
                            "base": r.base_amount,
                            "fee": r.fee_amount,
                            "tax": r.tax_amount,
                            "total": r.total_amount,
                        },
                    },
                }
                for r in registrations
            ]

            return Response(
                {"code": 200, "message": "sukses", "data": data},
                status=status.HTTP_200_OK,
            )

        # UPDATE
        if request.method == "PUT":

            req = request.data

            id_registration = req.get("id_registration")

            reg = TournamentRegistrationUsecase.update_registration(
                id_registration, req
            )

            if not reg:
                return Response(
                    {"code": 404, "message": "Registration not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            return Response(
                {
                    "code": 200,
                    "message": "sukses",
                    "data": {"message": "Registration updated"},
                },
                status=status.HTTP_200_OK,
            )

        # DELETE
        if request.method == "DELETE":

            id_registration = request.GET.get("id_registration")

            deleted = TournamentRegistrationUsecase.delete_registration(id_registration)

            if not deleted:
                return Response(
                    {"code": 404, "message": "Registration not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            return Response(
                {
                    "code": 200,
                    "message": "sukses",
                    "data": {"message": "Registration deleted"},
                },
                status=status.HTTP_200_OK,
            )

    except Exception as e:

        return Response(
            {"code": 500, "message": "error", "error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
