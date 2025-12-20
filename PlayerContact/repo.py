# repository/player_contact_repository.py
from django.shortcuts import get_object_or_404
from .models import PlayerContact
from player.models import player

class RepoPlayerContact:
    @staticmethod
    def post(req):
        Pemain = get_object_or_404(player, player=req['player'])

        new_player_contact = PlayerContact.objects.create(
            playercontact=req['playercontact'],
            pemain=Pemain,
            nama_panggilan=req['nama_panggilan'],
            nomor_hp=req['nomor_hp'],
            nama_orangtua=req['nama_orangtua'],
            nomor_orangtua=req['nomor_orangtua'],
            nama_kontak_darurat=req['nama_kontak_darurat'],
            kontak_darurat=req['kontak_darurat']
        )
        return {
            'playercontact': new_player_contact.playercontact,
            'player': {
                'player': Pemain.player,
                'nama': Pemain.nama,
                'posisi': Pemain.posisi,
                'kewarganegaraan': Pemain.kewarganegaraan,
                'team': {
                    'team': Pemain.tim.team,
                    'nama_team': Pemain.tim.nama_team,
                    'kategori_team': Pemain.tim.kategori_team,
                    'logo_team': Pemain.tim.logo_team.url if Pemain.tim.logo_team else None
                },
                'nomor_punggung': Pemain.nomor_punggung,
                'tinggi_badan': Pemain.tinggi_badan,
                'berat_badan': Pemain.berat_badan,
                'tanggal_gabung': Pemain.tanggal_gabung,
                'kelamin': Pemain.kelamin,
                'foto_profil': Pemain.foto_profil.url if Pemain.foto_profil else None
            },
            'nama_panggilan': new_player_contact.nama_panggilan,
            'nomor_hp': new_player_contact.nomor_hp,
            'nama_orangtua': new_player_contact.nama_orangtua,
            'nomor_orangtua': new_player_contact.nomor_orangtua,
            'nama_kontak_darurat': new_player_contact.nama_kontak_darurat,
            'kontak_darurat': new_player_contact.kontak_darurat
        }

    @staticmethod
    def get(player_contact_id):
        player_contact_data = get_object_or_404(PlayerContact, playercontact=player_contact_id)
        return {
            'playercontact': player_contact_data.playercontact,
            'player': {
                'player': player_contact_data.pemain.player,
                'nama': player_contact_data.pemain.nama,
                'posisi': player_contact_data.pemain.posisi,
                'kewarganegaraan': player_contact_data.pemain.kewarganegaraan,
                'team': {
                    'team': player_contact_data.pemain.tim.team,
                    'nama_team': player_contact_data.pemain.tim.nama_team,
                    'kategori_team': player_contact_data.pemain.tim.kategori_team,
                    'logo_team': player_contact_data.pemain.tim.logo_team.url if player_contact_data.pemain.tim.logo_team else None
                },
                'nomor_punggung': player_contact_data.pemain.nomor_punggung,
                'tinggi_badan': player_contact_data.pemain.tinggi_badan,
                'berat_badan': player_contact_data.pemain.berat_badan,
                'tanggal_gabung': player_contact_data.pemain.tanggal_gabung,
                'kelamin': player_contact_data.pemain.kelamin,
                'foto_profil': player_contact_data.pemain.foto_profil.url if player_contact_data.pemain.foto_profil else None
            },
            'nama_panggilan': player_contact_data.nama_panggilan,
            'nomor_hp': player_contact_data.nomor_hp,
            'nama_orangtua': player_contact_data.nama_orangtua,
            'nomor_orangtua': player_contact_data.nomor_orangtua,
            'nama_kontak_darurat':player_contact_data.nama_kontak_darurat,
            'kontak_darurat': player_contact_data.kontak_darurat
        }

    @staticmethod
    def get_all():
        player_contacts = PlayerContact.objects.all()
        return [{
            'playercontact': contact.playercontact,
            'player': {
                'player': contact.pemain.player,
                'nama': contact.pemain.nama,
                'posisi': contact.pemain.posisi,
                'kewarganegaraan': contact.pemain.kewarganegaraan,
                'team': {
                    'team': contact.pemain.tim.team,
                    'nama_team': contact.pemain.tim.nama_team,
                    'kategori_team': contact.pemain.tim.kategori_team,
                    'logo_team': contact.pemain.tim.logo_team.url if contact.pemain.tim.logo_team else None
                },
                'nomor_punggung': contact.pemain.nomor_punggung,
                'tinggi_badan': contact.pemain.tinggi_badan,
                'berat_badan': contact.pemain.berat_badan,
                'tanggal_gabung': contact.pemain.tanggal_gabung,
                'kelamin': contact.pemain.kelamin,
                'foto_profil': contact.pemain.foto_profil.url if contact.pemain.foto_profil else None
            },
            'nama_panggilan': contact.nama_panggilan,
            'nomor_hp': contact.nomor_hp,
            'nama_orangtua': contact.nama_orangtua,
            'nomor_orangtua': contact.nomor_orangtua,
            'nama_kontak_darurat': contact.nama_kontak_darurat,
            'kontak_darurat': contact.kontak_darurat
        } for contact in player_contacts]

    @staticmethod
    def get_by_player(player_id):
        # Ambil instance player, akan raise 404 jika tidak ditemukan
        Pemain = get_object_or_404(player, player=player_id)
        # Ambil kontak pertama yang terkait dengan player
        player_contact = PlayerContact.objects.filter(pemain=Pemain).first()

        # Jika tidak ada kontak, kembalikan None atau lempar error sesuai kebutuhan
        if not player_contact:
            return None  # atau bisa raise Exception("No contact found for this player") tergantung kebutuhan

        # Kembalikan data tunggal
        return {
            'playercontact': player_contact.playercontact,
            'player': {
                'player': player_contact.pemain.player,
                'nama': player_contact.pemain.nama,
                'posisi': player_contact.pemain.posisi,
                'kewarganegaraan': player_contact.pemain.kewarganegaraan,
                'team': {
                    'team': player_contact.pemain.tim.team if player_contact.pemain.tim else None,
                    'nama_team': player_contact.pemain.tim.nama_team if player_contact.pemain.tim else None,
                    'kategori_team': player_contact.pemain.tim.kategori_team if player_contact.pemain.tim else None,
                    'logo_team': player_contact.pemain.tim.logo_team.url if player_contact.pemain.tim and player_contact.pemain.tim.logo_team else None
                },
                'nomor_punggung': player_contact.pemain.nomor_punggung,
                'tinggi_badan': player_contact.pemain.tinggi_badan,
                'berat_badan': player_contact.pemain.berat_badan,
                'tanggal_gabung': player_contact.pemain.tanggal_gabung,
                'kelamin': player_contact.pemain.kelamin,
                'foto_profil': player_contact.pemain.foto_profil.url if player_contact.pemain.foto_profil else None
            },
            'nama_panggilan': player_contact.nama_panggilan,
            'nomor_hp': player_contact.nomor_hp,
            'nama_orangtua': player_contact.nama_orangtua,
            'nomor_orangtua': player_contact.nomor_orangtua,
            'nama_kontak_darurat': player_contact.nama_kontak_darurat,
            'kontak_darurat': player_contact.kontak_darurat
        }

    @staticmethod
    def put(req):
        PlayerContactData = get_object_or_404(PlayerContact, playercontact=req['playercontact'])
        Pemain = get_object_or_404(player, player=req['player'])

        PlayerContactData.pemain = Pemain
        PlayerContactData.nama_panggilan = req.get('nama_panggilan', PlayerContactData.nama_panggilan)
        PlayerContactData.nomor_hp = req.get('nomor_hp', PlayerContactData.nomor_hp)
        PlayerContactData.nama_orangtua = req.get('nama_orangtua', PlayerContactData.nama_orangtua)
        PlayerContactData.nomor_orangtua = req.get('nomor_orangtua', PlayerContactData.nomor_orangtua)
        PlayerContactData.nama_kontak_darurat = req.get('nama_kontak_darurat', PlayerContactData.nama_kontak_darurat)
        PlayerContactData.kontak_darurat = req.get('kontak_darurat', PlayerContactData.kontak_darurat)
        PlayerContactData.save()

        return {
            'playercontact': PlayerContactData.playercontact,
            'player': {
                'player': Pemain.player,
                'nama': Pemain.nama,
                'posisi': Pemain.posisi,
                'kewarganegaraan': Pemain.kewarganegaraan,
                'team': {
                    'team': Pemain.tim.team,
                    'nama_team': Pemain.tim.nama_team,
                    'kategori_team': Pemain.tim.kategori_team,
                    'logo_team': Pemain.tim.logo_team.url if Pemain.tim.logo_team else None
                },
                'nomor_punggung': Pemain.nomor_punggung,
                'tinggi_badan': Pemain.tinggi_badan,
                'berat_badan': Pemain.berat_badan,
                'tanggal_gabung': Pemain.tanggal_gabung,
                'kelamin': Pemain.kelamin,
                'foto_profil': Pemain.foto_profil.url if Pemain.foto_profil else None
            },
            'nama_panggilan': PlayerContactData.nama_panggilan,
            'nomor_hp': PlayerContactData.nomor_hp,
            'nama_orangtua': PlayerContactData.nama_orangtua,
            'nomor_orangtua': PlayerContactData.nomor_orangtua,
            'nama_kontak_darurat': PlayerContactData.nama_kontak_darurat,
            'kontak_darurat': PlayerContactData.kontak_darurat
        }

    @staticmethod
    def delete(req):
        PlayerContactData = get_object_or_404(PlayerContact, playercontact=req['playercontact'])
        PlayerContactData.delete()
        return {'message': f"PlayerContact with id {req['playercontact']} has been deleted."}
