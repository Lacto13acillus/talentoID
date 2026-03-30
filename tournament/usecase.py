from tournament.repository import TournamentRepository


class TournamentUsecase:

    @staticmethod
    def list_tournament():
        return TournamentRepository.get_all()

    @staticmethod
    def detail_tournament(id_tournament):
        return TournamentRepository.get_by_id(id_tournament)

    @staticmethod
    def create_tournament(req):
        return TournamentRepository.create(req)

    @staticmethod
    def update_tournament(id_tournament, req):
        return TournamentRepository.update(id_tournament, req)

    @staticmethod
    def delete_tournament(id_tournament):
        return TournamentRepository.delete(id_tournament)
