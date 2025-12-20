# usecases/player_contact_usecase.py
from .repo import RepoPlayerContact
import uuid

class UsecasePlayerContact:
    @staticmethod
    def post(request):
        reqs = {
            'playercontact': uuid.uuid4(),
            'player': request.data['player'],
            'nama_panggilan': request.data['nama_panggilan'],
            'nomor_hp': request.data['nomor_hp'],
            'nama_orangtua': request.data['nama_orangtua'],
            'nomor_orangtua': request.data['nomor_orangtua'],
            'nama_kontak_darurat': request.data['nama_kontak_darurat'],
            'kontak_darurat': request.data['kontak_darurat']
        }
        dataPost = RepoPlayerContact.post(reqs)
        return dataPost
    
    @staticmethod
    def get(player_contact_id):
        dataPlayerContact = RepoPlayerContact.get(player_contact_id)
        return dataPlayerContact
    
    @staticmethod
    def get_all():
        return RepoPlayerContact.get_all()
    
    @staticmethod
    def get_by_player(player_id):
        return RepoPlayerContact.get_by_player(player_id)
    
    @staticmethod
    def put(request):
        reqs = {
            'playercontact': request.data['playercontact'],
            'player': request.data['player'],
            'nama_panggilan': request.data.get('nama_panggilan'),
            'nomor_hp': request.data.get('nomor_hp'),
            'nama_orangtua': request.data.get('nama_orangtua'),
            'nomor_orangtua': request.data.get('nomor_orangtua'),
            'nama_kontak_darurat': request.data.get('nama_kontak_darurat'),
            'kontak_darurat': request.data.get('kontak_darurat')
        }
        updated_player_contact = RepoPlayerContact.put(reqs)
        return updated_player_contact
    
    @staticmethod
    def delete(request):
        reqs = {
            'playercontact': request.data['playercontact']
        }
        delete_player_contact = RepoPlayerContact.delete(reqs)
        return delete_player_contact