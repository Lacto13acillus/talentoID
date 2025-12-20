# PlayerActivity/repo.py
from django.shortcuts import get_object_or_404
from attendance.models import attendance
from MatchAttendance.models import MatchAttendance
from player.models import player

class RepoPlayerActivity:
    @staticmethod
    def calculate_activity(player_id):
        Player = get_object_or_404(player, player=player_id)

        # Hitung total kehadiran untuk training
        training_attendances = attendance.objects.filter(player=Player)
        total_training_present = training_attendances.filter(attendance_status__iexact='Present').count()
        total_training_absent = training_attendances.filter(attendance_status__iexact='Absent',).count()
        total_training_unknown = training_attendances.filter(attendance_status__iexact='Unknown').count()

        # Hitung performa untuk training
        training_performance = "Quite Good!" if total_training_present >= (total_training_absent + total_training_unknown) else "Keep Improving yourself!"

        # Hitung total kehadiran untuk match
        match_attendances = MatchAttendance.objects.filter(player=Player)
        total_match_present = match_attendances.filter(attendance_status__iexact='Present').count()
        total_match_absent = match_attendances.filter(attendance_status__iexact='Absent').count()
        total_match_unknown = match_attendances.filter(attendance_status__iexact='Unknown').count()

        # Hitung performa untuk match
        match_performance = "Quite Good!" if total_match_present >= (total_match_absent + total_match_unknown) else "Keep Improving yourself!"

        return {
            'player': {
                'player': Player.player,
                'nama': Player.nama,
                'posisi': Player.posisi,
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
            'total_training': {
                'Present': total_training_present,
                'Absent': total_training_absent,
                'Unknown': total_training_unknown,
                'Performance': training_performance
            },
            'total_match': {
                'Present': total_match_present,
                'Absent': total_match_absent,
                'Unknown': total_match_unknown,
                'Performance': match_performance
            }
        }
