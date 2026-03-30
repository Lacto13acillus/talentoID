from tournament.models import TournamentRegistration


class TournamentRegistrationRepository:

    @staticmethod
    def get_all(team_id=None):
        if team_id:
            return TournamentRegistration.objects.select_related(
                "tournament", "team"
            ).filter(team_id=team_id)
        return TournamentRegistration.objects.select_related("tournament", "team").all()

    @staticmethod
    def get_by_id(id_registration):
        return TournamentRegistration.objects.filter(
            id_registration=id_registration
        ).first()

    @staticmethod
    def create(data):
        return TournamentRegistration.objects.create(**data)

    @staticmethod
    def update(id_registration, data):

        reg = TournamentRegistration.objects.filter(
            id_registration=id_registration
        ).first()

        if not reg:
            return None

        for key, value in data.items():
            setattr(reg, key, value)

        reg.save()

        return reg

    @staticmethod
    def delete(id_registration):

        reg = TournamentRegistration.objects.filter(
            id_registration=id_registration
        ).first()

        if not reg:
            return False

        reg.delete()

        return True
