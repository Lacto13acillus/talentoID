from django.shortcuts import get_object_or_404
from .models import session
from player.models import player
from team.models import team

class RepoSession:
    @staticmethod
    def post(req):
        Player = get_object_or_404(player, player=req['player'])

        new_session = session.objects.create(
            session=req['session'],
            player=Player,
            session_type=req['session_type'],
            minutes_date=req['minutes_date'],
            notes=req['notes']
        )
        return {
            'session': new_session.session,
            'player': {
                'player': Player.player,
                'nama': Player.nama,
                'posisi': Player.posisi,
                'usia': Player.usia,
                'kewarganegaraan': Player.kewarganegaraan,
                'nomor_punggung': Player.nomor_punggung,
                'tinggi_badan': Player.tinggi_badan,
                'berat_badan': Player.berat_badan,
                'foto_profil': Player.foto_profil.url if Player.foto_profil else None,
                'team': {
                    'team': Player.tim.team,
                    'nama_team': Player.tim.nama_team,
                    'kategori_team': Player.tim.kategori_team,
                    'logo_team': Player.tim.logo_team.url if Player.tim.logo_team else None
                }
            },
            'session_type': new_session.session_type,
            'minutes_date': new_session.minutes_date,
            'notes': new_session.notes
        }
    
    @staticmethod
    def get(session_id):
        session_data = get_object_or_404(session, session=session_id)
        Player = session_data.player

        return {
            'session': session_data.session,
            'player': {
                'player': Player.player,
                'nama': Player.nama,
                'posisi': Player.posisi,
                'usia': Player.usia,
                'kewarganegaraan': Player.kewarganegaraan,
                'nomor_punggung': Player.nomor_punggung,
                'tinggi_badan': Player.tinggi_badan,
                'berat_badan': Player.berat_badan,
                'foto_profil': Player.foto_profil.url if Player.foto_profil else None,
                'team': {
                    'team': Player.tim.team,
                    'nama_team': Player.tim.nama_team,
                    'kategori_team': Player.tim.kategori_team,
                    'logo_team': Player.tim.logo_team.url if Player.tim.logo_team else None
                }
            },
            'session_type': session_data.session_type,
            'minutes_date': session_data.minutes_date,
            'notes': session_data.notes
        }
    
    @staticmethod
    def get_all():
        session_list = session.objects.all()
        result = []
        
        for session_data in session_list:
            Player = session_data.player
            result.append({
                'session': session_data.session,
                'player': {
                    'player': Player.player,
                    'nama': Player.nama,
                    'posisi': Player.posisi,
                    'usia': Player.usia,
                    'kewarganegaraan': Player.kewarganegaraan,
                    'nomor_punggung': Player.nomor_punggung,
                    'tinggi_badan': Player.tinggi_badan,
                    'berat_badan': Player.berat_badan,
                    'foto_profil': Player.foto_profil.url if Player.foto_profil else None,
                    'team': {
                        'team': Player.tim.team,
                        'nama_team': Player.tim.nama_team,
                        'kategori_team': Player.tim.kategori_team,
                        'logo_team': Player.tim.logo_team.url if Player.tim.logo_team else None
                    }
                },
                'session_type': session_data.session_type,
                'minutes_date': session_data.minutes_date,
                'notes': session_data.notes
            })
        
        return result

    @staticmethod
    def put(req):
        Session = get_object_or_404(session, session=req['session'])
        Player = get_object_or_404(player, player=req['player'])

        Session.session_type = req.get('session_type', Session.session_type)
        Session.minutes_date = req.get('minutes_date', Session.minutes_date)
        Session.notes = req.get('notes', Session.notes)
        Session.player = Player
        Session.save()

        return {
            'session': Session.session,
            'player': {
                'player': Player.player,
                'nama': Player.nama,
                'posisi': Player.posisi,
                'usia': Player.usia,
                'kewarganegaraan': Player.kewarganegaraan,
                'nomor_punggung': Player.nomor_punggung,
                'tinggi_badan': Player.tinggi_badan,
                'berat_badan': Player.berat_badan,
                'foto_profil': Player.foto_profil.url if Player.foto_profil else None,
                'team': {
                    'team': Player.tim.team,
                    'nama_team': Player.tim.nama_team,
                    'kategori_team': Player.tim.kategori_team,
                    'logo_team': Player.tim.logo_team.url if Player.tim.logo_team else None
                }
            },
            'session_type': Session.session_type,
            'minutes_date': Session.minutes_date,
            'notes': Session.notes
        }
    
    @staticmethod
    def delete(req):
        Session = get_object_or_404(session, session=req['session'])
        Session.delete()
        return {'message': f"Session with id {req['session']} has been deleted."}