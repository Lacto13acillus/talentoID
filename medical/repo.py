# repository/medical_repository.py
from django.shortcuts import get_object_or_404
from .models import medical
from player.models import player
from MedicalHistory.models import MedicalHistory
from session.models import session

class RepoMedical:
    @staticmethod
    def post(req):
        Player = get_object_or_404(player, player=req['player'])
        MedicalHistoryData = get_object_or_404(MedicalHistory, medicalhistory=req['medical_history'])
        Session = get_object_or_404(session, session=req['session'])

        new_medical = medical.objects.create(
            medical=req['medical'],
            player=Player,
            medical_history=MedicalHistoryData,
            session=Session
        )
        return {
            'medical': new_medical.medical,
            'player': {
                'player': Player.player,
                'nama': Player.nama,
                'posisi': Player.posisi,
                'usia': Player.usia,
                'kewarganegaraan': Player.kewarganegaraan,
                'team': {
                    'team': Player.tim.team,
                    'nama_team': Player.tim.nama_team,
                    'kategori_team': Player.tim.kategori_team,
                    'logo_team': Player.tim.logo_team.url if Player.tim.logo_team else None
                },
                'nomor_punggung': Player.nomor_punggung,
                'tinggi_badan': Player.tinggi_badan,
                'berat_badan': Player.berat_badan,
                'tanggal_gabung': Player.tanggal_gabung,
                'kelamin': Player.kelamin,
                'foto_profil': Player.foto_profil.url if Player.foto_profil else None
            },
            'medical_history': {
                'medical_history': MedicalHistoryData.medicalhistory,
                'jenis_pemeriksaan': MedicalHistoryData.jenis_pemeriksaan,
                'file_dokumen': MedicalHistoryData.file_dokumen.url if MedicalHistoryData.file_dokumen else None
            },
            'session': {
                'session': Session.session,
                'session_type': Session.session_type,
                'minutes_date': Session.minutes_date,
                'notes': Session.notes
            }
        }
    
    @staticmethod
    def get(medical_id):
        medical_data = get_object_or_404(medical, medical=medical_id)
        return {
            'medical': medical_data.medical,
            'player': {
                'player': medical_data.player.player,
                'nama': medical_data.player.nama,
                'posisi': medical_data.player.posisi,
                'usia': medical_data.player.usia,
                'kewarganegaraan': medical_data.player.kewarganegaraan,
                'team': {
                    'team': medical_data.player.tim.team,
                    'nama_team': medical_data.player.tim.nama_team,
                    'kategori_team': medical_data.player.tim.kategori_team
                },
                'nomor_punggung': medical_data.player.nomor_punggung,
                'tinggi_badan': medical_data.player.tinggi_badan,
                'berat_badan': medical_data.player.berat_badan,
                'tanggal_gabung': medical_data.player.tanggal_gabung,
                'kelamin': medical_data.player.kelamin,
                'foto_profil': medical_data.player.foto_profil.url if medical_data.player.foto_profil else None
            },
            'medical_history': {
                'medical_history': medical_data.medical_history.medicalhistory,
                'jenis_pemeriksaan': medical_data.medical_history.jenis_pemeriksaan,
                'file_dokumen': medical_data.medical_history.file_dokumen.url if medical_data.medical_history.file_dokumen else None
            },
            'session': {
                'session': medical_data.session.session,
                'session_type': medical_data.session.session_type,
                'minutes_date': medical_data.session.minutes_date,
                'notes': medical_data.session.notes
            }
        }
    
    @staticmethod
    def get_all():
        medical_list = medical.objects.all()
        result = []
        
        for medical_data in medical_list:
            result.append({
                'medical': medical_data.medical,
                'player': {
                    'player': medical_data.player.player,
                    'nama': medical_data.player.nama,
                    'posisi': medical_data.player.posisi,
                    'usia': medical_data.player.usia,
                    'kewarganegaraan': medical_data.player.kewarganegaraan,
                    'team': {
                        'team': medical_data.player.tim.team,
                        'nama_team': medical_data.player.tim.nama_team,
                        'kategori_team': medical_data.player.tim.kategori_team,
                        'logo_team': medical_data.player.tim.logo_team.url if medical_data.player.tim.logo_team else None
                    },
                    'nomor_punggung': medical_data.player.nomor_punggung,
                    'tinggi_badan': medical_data.player.tinggi_badan,
                    'berat_badan': medical_data.player.berat_badan,
                    'tanggal_gabung': medical_data.player.tanggal_gabung,
                    'kelamin': medical_data.player.kelamin,
                    'foto_profil': medical_data.player.foto_profil.url if medical_data.player.foto_profil else None
                },
                'medical_history': {
                    'medical_history': medical_data.medical_history.medicalhistory,
                    'jenis_pemeriksaan': medical_data.medical_history.jenis_pemeriksaan,
                    'file_dokumen': medical_data.medical_history.file_dokumen.url if medical_data.medical_history.file_dokumen else None
                },
                'session': {
                    'session': medical_data.session.session,
                    'session_type': medical_data.session.session_type,
                    'minutes_date': medical_data.session.minutes_date,
                    'notes': medical_data.session.notes
                }
            })
        
        return result
    
        
    @staticmethod
    def put(req):
        MedicalData = get_object_or_404(medical, medical=req['medical'])
        Player = get_object_or_404(player, player=req['player'])
        MedicalHistoryData = get_object_or_404(MedicalHistory, medicalhistory=req['medical_history'])
        Session = get_object_or_404(session, session=req['session'])

        MedicalData.player = Player
        MedicalData.medical_history = MedicalHistoryData
        MedicalData.session = Session
        MedicalData.save()

        return {
            'medical': MedicalData.medical,
            'player': {
                'player': Player.player,
                'nama': Player.nama,
                'posisi': Player.posisi,
                'usia': Player.usia,
                'kewarganegaraan': Player.kewarganegaraan,
                'team': {
                    'team': Player.tim.team,
                    'nama_team': Player.tim.nama_team,
                    'kategori_team': Player.tim.kategori_team
                },
                'nomor_punggung': Player.nomor_punggung,
                'tinggi_badan': Player.tinggi_badan,
                'berat_badan': Player.berat_badan,
                'tanggal_gabung': Player.tanggal_gabung,
                'kelamin': Player.kelamin,
                'foto_profil': Player.foto_profil.url if Player.foto_profil else None
            },
            'medical_history': {
                'medical_history': MedicalHistoryData.medicalhistory,
                'jenis_pemeriksaan': MedicalHistoryData.jenis_pemeriksaan,
                'file_dokumen': MedicalHistoryData.file_dokumen.url if MedicalHistoryData.file_dokumen else None
            },
            'session': {
                'session': Session.session,
                'session_type': Session.session_type,
                'minutes_date': Session.minutes_date,
                'notes': Session.notes
            }
        }
    
    @staticmethod
    def delete(req):
        MedicalData = get_object_or_404(medical, medical=req['medical'])
        MedicalData.delete()
        return {'message': f"Medical with id {req['medical']} has been deleted."}