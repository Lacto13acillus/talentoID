from .repo import RepoTeam
import uuid

class UsecaseTeam:
    @staticmethod
    def post(request):
        if 'logo_team' not in request.FILES:
            raise ValueError("logo_team is required.")

        reqs = {
            'team': uuid.uuid4(),
            'nama_team': request.data['nama_team'],
            'coach': request.data['coach'],
            'club': request.data['club'],
            'kategori_team': request.data['kategori_team'],
            'logo_team': request.FILES['logo_team']
        }
        dataPost = RepoTeam.post(reqs)
        return dataPost

    @staticmethod
    def get(team_id):
        dataTeam = RepoTeam.get(team_id)
        return dataTeam

    @staticmethod
    def get_all():
        return RepoTeam.get_all()

    @staticmethod
    def get_all_teams_by_coach_id(coach_id):
        return RepoTeam.get_all_teams_by_coach_id(coach_id)

    @staticmethod
    def get_team_stats_by_team_id(team_id):
        return RepoTeam.get_team_stats_by_team_id(team_id)

    @staticmethod
    def put(request):
        reqs = {
            'team': request.data['team'],
            'nama_team': request.data.get('nama_team'),
            'coach': request.data.get('coach'),
             'club': request.data['club'],
            'kategori_team': request.data.get('kategori_team'),
            'logo_team': request.FILES.get('logo_team')
        }
        updated_team = RepoTeam.put(reqs)
        return updated_team

    @staticmethod
    def delete(request):
        reqs = {
            'team': request.data['team']
        }
        delete_message = RepoTeam.delete(reqs)
        return delete_message
