from tournament.models import Tournament
from django.db.models import Prefetch
from tournament.models import TournamentRegistration


class TournamentRepository:

    @staticmethod
    def get_all():
        return Tournament.objects.prefetch_related(
            Prefetch(
                "tournamentregistration_set",
                queryset=TournamentRegistration.objects.select_related("team"),
            )
        )

    @staticmethod
    def get_by_id(id_tournament):
        return Tournament.objects.filter(id_tournament=id_tournament).first()

    @staticmethod
    def create(data):
        return Tournament.objects.create(**data)

    @staticmethod
    def update(id_tournament, data):
        tournament = Tournament.objects.filter(id_tournament=id_tournament).first()
        if not tournament:
            return None

        for key, value in data.items():
            setattr(tournament, key, value)

        tournament.save()
        return tournament

    @staticmethod
    def delete(id_tournament):
        tournament = Tournament.objects.filter(id_tournament=id_tournament).first()
        if tournament:
            tournament.delete()
            return True
        return False
