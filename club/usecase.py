from .repo import RepoClub
import uuid

class UsecaseClub:
	@staticmethod
	def get_all():
		return RepoClub.get_all()

	@staticmethod
	def get(club_id):
		return RepoClub.get(club_id)

	@staticmethod
	def get_club_info_by_player_id(player_id):
		return RepoClub.get_club_info_by_player_id(player_id)

	@staticmethod
	def post(request):
		reqs = {
			'club': uuid.uuid4(),
			'club_name': request.data['club_name'],
			'club_logo': request.FILES['club_logo']
		}
		return RepoClub.post(reqs)

	@staticmethod
	def put(request):
		reqs = {
			'club': request.data['club'],
			'club_name': request.data['club_name'],
		}
		if request.FILES.get('club_logo') is not None:
			reqs['club_logo'] = request.FILES.get('club_logo')

		return RepoClub.put(reqs)

	@staticmethod
	def delete(request):
		reqs = {
            'club': request.data['club']
        }
		return RepoClub.delete(reqs)
