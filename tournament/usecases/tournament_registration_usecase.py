from player.services.payment_service import create_registration_invoice
from tournament.models import Tournament
from tournament.repositories.tournament_registration_repository import (
    TournamentRegistrationRepository,
)
from django.shortcuts import get_object_or_404
from team.models import team


class TournamentRegistrationUsecase:

    @staticmethod
    def list_registration(team_id=None):
        return TournamentRegistrationRepository.get_all(team_id)

    @staticmethod
    def detail_registration(id_registration):
        return TournamentRegistrationRepository.get_by_id(id_registration)

    @staticmethod
    def create_registration(req):
        tournament_id = req["tournament_id"]
        team_id = req["team_id"]
        email = req["email"]

        tournament = get_object_or_404(Tournament, id_tournament=tournament_id)
        teamInstance = get_object_or_404(team, team=team_id)

        print("Creating registration for tournament:", tournament.name)
        print("Team:", teamInstance.nama_team)

        payment = create_registration_invoice(
            email=email,
            payment_channel_code=req["payment_channel"],
            payment_method=req["payment_method"],
            base_amount=int(tournament.entry_fee),
        )

        print("Payment details:", payment)

        data = {
            "tournament": tournament,
            "team": teamInstance,
            "payment_status": "pending",
            "base_amount": payment["breakdown"]["base_amount"],
            "fee_amount": payment["breakdown"]["fee"],
            "tax_amount": payment["breakdown"]["tax"],
            "total_amount": payment["amount"],
            "payment_channel": payment["payment_channel"],
            "payment_method": payment["payment_method"],
            "invoice_id": payment["invoice_id"],
            "invoice_url": payment["invoice_url"],
            "expiry_date": payment["expiry_date"],
            "external_id": payment["external_id"],
        }

        registration = TournamentRegistrationRepository.create(data)

        return {
            "id_registration": str(registration.id_registration),
            "tournament": registration.tournament.name,
            "team": registration.team.nama_team,
            "payment_status": registration.payment_status,
            "registration_date": registration.registration_date,
            "invoice_url": registration.invoice_url,
            "amount": registration.total_amount,
            "expiry_date": registration.expiry_date,
        }

    @staticmethod
    def update_registration(id_registration, req):
        return TournamentRegistrationRepository.update(id_registration, req)

    @staticmethod
    def delete_registration(id_registration):
        return TournamentRegistrationRepository.delete(id_registration)
