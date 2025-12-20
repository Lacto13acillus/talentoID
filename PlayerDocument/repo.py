# repository/player_document_repository.py
from django.shortcuts import get_object_or_404
from .models import PlayerDocument
from player.models import player
from django.core.exceptions import ValidationError

class RepoPlayerDocument:
    @staticmethod
    def post(req):
        Pemain = get_object_or_404(player, player=req['player'])

        # Validasi file
        if 'file_dokumen' in req and req['file_dokumen']:
            file_dokumen = req['file_dokumen']
            if file_dokumen.name.split('.')[-1].lower() not in ['jpeg', 'png', 'pdf', 'doc']:
                raise ValidationError("Invalid file format. Only JPEG, PNG, PDF, and DOC are allowed.")

        new_player_document = PlayerDocument.objects.create(
            playerdocument=req['playerdocument'],
            pemain=Pemain,
            jenis_dokumen=req['jenis_dokumen'],
            file_dokumen=req.get('file_dokumen', None)
        )
        return {
            'playerdocument': new_player_document.playerdocument,
            'player': {
                'player': Pemain.player,
                'nama': Pemain.nama,
                'posisi': Pemain.posisi,
                'usia': Pemain.usia,
                'kewarganegaraan': Pemain.kewarganegaraan,
                'team': {
                    'team': Pemain.tim.team if Pemain.tim else None,
                    'nama_team': Pemain.tim.nama_team if Pemain.tim else None,
                    'kategori_team': Pemain.tim.kategori_team if Pemain.tim else None,
                    'logo_team': Pemain.tim.logo_team.url if Pemain.tim and Pemain.tim.logo_team else None
                },
                'nomor_punggung': Pemain.nomor_punggung,
                'tinggi_badan': Pemain.tinggi_badan,
                'berat_badan': Pemain.berat_badan,
                'tanggal_gabung': Pemain.tanggal_gabung,
                'kelamin': Pemain.kelamin,
                'foto_profil': Pemain.foto_profil.url if Pemain.foto_profil else None
            },
            'jenis_dokumen': new_player_document.jenis_dokumen,
            'file_dokumen': new_player_document.file_dokumen.url if new_player_document.file_dokumen else None
        }
    
    @staticmethod
    def get(player_document_id):
        player_document_data = get_object_or_404(PlayerDocument, playerdocument=player_document_id)
        return {
            'playerdocument': player_document_data.playerdocument,
            'player': {
                'player': player_document_data.pemain.player,
                'nama': player_document_data.pemain.nama,
                'posisi': player_document_data.pemain.posisi,
                'usia': player_document_data.pemain.usia,
                'kewarganegaraan': player_document_data.pemain.kewarganegaraan,
                'team': {
                    'team': player_document_data.pemain.tim.team if player_document_data.pemain.tim else None,
                    'nama_team': player_document_data.pemain.tim.nama_team if player_document_data.pemain.tim else None,
                    'kategori_team': player_document_data.pemain.tim.kategori_team if player_document_data.pemain.tim else None,
                    'logo_team': player_document_data.pemain.tim.logo_team.url if player_document_data.pemain.tim and player_document_data.pemain.tim.logo_team else None
                },
                'nomor_punggung': player_document_data.pemain.nomor_punggung,
                'tinggi_badan': player_document_data.pemain.tinggi_badan,
                'berat_badan': player_document_data.pemain.berat_badan,
                'tanggal_gabung': player_document_data.pemain.tanggal_gabung,
                'kelamin': player_document_data.pemain.kelamin,
                'foto_profil': player_document_data.pemain.foto_profil.url if player_document_data.pemain.foto_profil else None
            },
            'jenis_dokumen': player_document_data.jenis_dokumen,
            'file_dokumen': player_document_data.file_dokumen.url if player_document_data.file_dokumen else None
        }
    
    @staticmethod
    def get_all():
        player_documents = PlayerDocument.objects.all()
        return [{
            'playerdocument': document.playerdocument,
            'player': {
                'player': document.pemain.player,
                'nama': document.pemain.nama,
                'posisi': document.pemain.posisi,
                'usia': document.pemain.usia,
                'kewarganegaraan': document.pemain.kewarganegaraan,
                'team': {
                    'team': document.pemain.tim.team if document.pemain.tim else None,
                    'nama_team': document.pemain.tim.nama_team if document.pemain.tim else None,
                    'kategori_team': document.pemain.tim.kategori_team if document.pemain.tim else None,
                    'logo_team': document.pemain.tim.logo_team.url if document.pemain.tim and document.pemain.tim.logo_team else None
                },
                'nomor_punggung': document.pemain.nomor_punggung,
                'tinggi_badan': document.pemain.tinggi_badan,
                'berat_badan': document.pemain.berat_badan,
                'tanggal_gabung': document.pemain.tanggal_gabung,
                'kelamin': document.pemain.kelamin,
                'foto_profil': document.pemain.foto_profil.url if document.pemain.foto_profil else None
            },
            'jenis_dokumen': document.jenis_dokumen,
            'file_dokumen': document.file_dokumen.url if document.file_dokumen else None
        } for document in player_documents]
    
    @staticmethod
    def get_by_player(player_id):
        Pemain = get_object_or_404(player, player=player_id)
        player_documents = PlayerDocument.objects.filter(pemain=Pemain)
        result = []
        for document in player_documents:
            try:
                result.append({
                    'playerdocument': document.playerdocument,
                    'player': {
                        'player': document.pemain.player,
                        'nama': document.pemain.nama,
                        'posisi': document.pemain.posisi,
                        'usia': document.pemain.usia,
                        'kewarganegaraan': document.pemain.kewarganegaraan,
                        'team': {
                            'team': document.pemain.tim.team if document.pemain.tim else None,
                            'nama_team': document.pemain.tim.nama_team if document.pemain.tim else None,
                            'kategori_team': document.pemain.tim.kategori_team if document.pemain.tim else None,
                            'logo_team': document.pemain.tim.logo_team.url if document.pemain.tim and document.pemain.tim.logo_team else None
                        },
                        'nomor_punggung': document.pemain.nomor_punggung,
                        'tinggi_badan': document.pemain.tinggi_badan,
                        'berat_badan': document.pemain.berat_badan,
                        'tanggal_gabung': document.pemain.tanggal_gabung,
                        'kelamin': document.pemain.kelamin,
                        'foto_profil': document.pemain.foto_profil.url if document.pemain.foto_profil else None
                    },
                    'jenis_dokumen': document.jenis_dokumen,
                    'file_dokumen': document.file_dokumen.url if document.file_dokumen else None
                })
            except Exception as e:
                print(f"Error processing player document {document.playerdocument}: {str(e)}")
                continue
        return result

    @staticmethod
    def put(req):
        PlayerDocumentData = get_object_or_404(PlayerDocument, playerdocument=req['playerdocument'])
        Pemain = get_object_or_404(player, player=req['player'])

        PlayerDocumentData.pemain = Pemain
        PlayerDocumentData.jenis_dokumen = req.get('jenis_dokumen', PlayerDocumentData.jenis_dokumen)

        if 'file_dokumen' in req and req['file_dokumen']:
            file_dokumen = req['file_dokumen']
            if file_dokumen.name.split('.')[-1].lower() not in ['jpeg', 'png', 'pdf', 'doc']:
                raise ValidationError("Invalid file format. Only JPEG, PNG, PDF, and DOC are allowed.")
            PlayerDocumentData.file_dokumen = file_dokumen

        PlayerDocumentData.save()

        return {
            'playerdocument': PlayerDocumentData.playerdocument,
            'player': {
                'player': Pemain.player,
                'nama': Pemain.nama,
                'posisi': Pemain.posisi,
                'usia': Pemain.usia,
                'kewarganegaraan': Pemain.kewarganegaraan,
                'team': {
                    'team': Pemain.tim.team if Pemain.tim else None,
                    'nama_team': Pemain.tim.nama_team if Pemain.tim else None,
                    'kategori_team': Pemain.tim.kategori_team if Pemain.tim else None,
                    'logo_team': Pemain.tim.logo_team.url if Pemain.tim and Pemain.tim.logo_team else None
                },
                'nomor_punggung': Pemain.nomor_punggung,
                'tinggi_badan': Pemain.tinggi_badan,
                'berat_badan': Pemain.berat_badan,
                'tanggal_gabung': Pemain.tanggal_gabung,
                'kelamin': Pemain.kelamin,
                'foto_profil': Pemain.foto_profil.url if Pemain.foto_profil else None
            },
            'jenis_dokumen': PlayerDocumentData.jenis_dokumen,
            'file_dokumen': PlayerDocumentData.file_dokumen.url if PlayerDocumentData.file_dokumen else None
        }
    
    @staticmethod
    def delete(req):
        PlayerDocumentData = get_object_or_404(PlayerDocument, playerdocument=req['playerdocument'])
        PlayerDocumentData.delete()
        return {'message': f"PlayerDocument with id {req['playerdocument']} has been deleted."}