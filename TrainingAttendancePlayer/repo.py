from django.shortcuts import get_object_or_404
from .models import TrainingAttendancePlayer
from player.models import player
from training.models import training
from team.models import team
from stadion.models import stadion
from TrainingCategory.models import trainingcategory
from frequency.models import frequency
from schedule.models import schedule

class RepoTrainingAttendancePlayer:
    @staticmethod
    def _get_training_data(training_obj):
        """Helper method to construct detailed training data."""
        if not training_obj:
            return None

        team_data = {
            'team': training_obj.tim.team,
            'nama_team': training_obj.tim.nama_team,
            'kategori_team': training_obj.tim.kategori_team,
            'logo_team': training_obj.tim.logo_team.url if training_obj.tim.logo_team else None
        }

        schedule_data = None
        if training_obj.jadwal:
            schedule_data = {
                'schedule': training_obj.jadwal.schedule,
                'tanggal': training_obj.jadwal.tanggal.isoformat() if training_obj.jadwal.tanggal else None,
                'start_time': training_obj.jadwal.start_time.strftime('%H:%M:%S') if training_obj.jadwal.start_time else None,
                'end_time': training_obj.jadwal.end_time.strftime('%H:%M:%S') if training_obj.jadwal.end_time else None
            }

        stadion_data = {
            'stadion': training_obj.lokasi.stadion,
            'nama_stadion': training_obj.lokasi.nama_stadion,
            'lokasi': training_obj.lokasi.lokasi
        }

        frequency_data = None
        if training_obj.frequency:
            frequency_data = {
                'frequency': training_obj.frequency.frequency,
                'frequency_time': training_obj.frequency.get_frequency_time_display()
            }

        categories_data = [
            {
                'trainingcategory': category.trainingcategory,
                'nama_category': category.nama_category
            } for category in training_obj.kategori.all()
        ]

        return {
            'training': training_obj.training,
            'nama_latihan': training_obj.nama_latihan,
            'team': team_data,
            'schedule': schedule_data,
            'stadion': stadion_data,
            'trainingcategory': categories_data,
            'frequency': frequency_data,
            'date': training_obj.date.isoformat() if training_obj.date else None,
            'start_time': training_obj.start_time.strftime('%H:%M') if training_obj.start_time else None,
            'end_time': training_obj.end_time.strftime('%H:%M') if training_obj.end_time else None,
            'deskripsi': training_obj.deskripsi
        }

    @staticmethod
    def post_training_attendance_player(req):
        Player = get_object_or_404(player, player=req['player'])
        Training = get_object_or_404(training, training=req['training']) if req.get('training') else None

        # Validate reason_absent if status is False
        status = req['status']
        reason_absent = req.get('reason_absent', '').strip()
        if not status and not reason_absent:
            raise ValueError("reason_absent is required and cannot be empty when the player is absent")

        new_attendance = TrainingAttendancePlayer.objects.create(
            trainingattendance_id=req['trainingattendance_id'],
            player=Player,
            training=Training,
            status=status,
            reason_absent=reason_absent if reason_absent else None
        )

        return {
            'trainingattendance_id': new_attendance.trainingattendance_id,
            'player': {
                'player': new_attendance.player.player,
                'nama': new_attendance.player.nama,
                'posisi': new_attendance.player.posisi,
                'usia': new_attendance.player.usia,
                'kewarganegaraan': new_attendance.player.kewarganegaraan,
                'team': {
                    'team': new_attendance.player.tim.team,
                    'nama_team': new_attendance.player.tim.nama_team,
                    'kategori_team': new_attendance.player.tim.kategori_team,
                    'logo_team': new_attendance.player.tim.logo_team.url if new_attendance.player.tim.logo_team else None
                },
                'nomor_punggung': new_attendance.player.nomor_punggung,
                'tinggi_badan': new_attendance.player.tinggi_badan,
                'berat_badan': new_attendance.player.berat_badan,
                'tanggal_gabung': new_attendance.player.tanggal_gabung.isoformat() if new_attendance.player.tanggal_gabung else None,
                'kelamin': new_attendance.player.kelamin,
                'foto_profil': new_attendance.player.foto_profil.url if new_attendance.player.foto_profil else None
            },
            'training': RepoTrainingAttendancePlayer._get_training_data(new_attendance.training),
            'status': new_attendance.status,
            'reason_absent': new_attendance.reason_absent
        }

    @staticmethod
    def get_training_attendance_player(trainingattendance_id):
        attendance_data = get_object_or_404(TrainingAttendancePlayer, trainingattendance_id=trainingattendance_id)

        return {
            'trainingattendance_id': attendance_data.trainingattendance_id,
            'player': {
                'player': attendance_data.player.player,
                'nama': attendance_data.player.nama,
                'posisi': attendance_data.player.posisi,
                'usia': attendance_data.player.usia,
                'kewarganegaraan': attendance_data.player.kewarganegaraan,
                'team': {
                    'team': attendance_data.player.tim.team,
                    'nama_team': attendance_data.player.tim.nama_team,
                    'kategori_team': attendance_data.player.tim.kategori_team,
                    'logo_team': attendance_data.player.tim.logo_team.url if attendance_data.player.tim.logo_team else None
                },
                'nomor_punggung': attendance_data.player.nomor_punggung,
                'tinggi_badan': attendance_data.player.tinggi_badan,
                'berat_badan': attendance_data.player.berat_badan,
                'tanggal_gabung': attendance_data.player.tanggal_gabung.isoformat() if attendance_data.player.tanggal_gabung else None,
                'kelamin': attendance_data.player.kelamin,
                'foto_profil': attendance_data.player.foto_profil.url if attendance_data.player.foto_profil else None
            },
            'training': RepoTrainingAttendancePlayer._get_training_data(attendance_data.training),
            'status': attendance_data.status,
            'reason_absent': attendance_data.reason_absent
        }

    @staticmethod
    def get_all_training_attendance_player():
        attendance_list = TrainingAttendancePlayer.objects.all()

        result = []
        for data in attendance_list:
            result.append({
                'trainingattendance_id': data.trainingattendance_id,
                'player': {
                    'player': data.player.player,
                    'nama': data.player.nama,
                    'posisi': data.player.posisi,
                    'usia': data.player.usia,
                    'kewarganegaraan': data.player.kewarganegaraan,
                    'team': {
                        'team': data.player.tim.team,
                        'nama_team': data.player.tim.nama_team,
                        'kategori_team': data.player.tim.kategori_team,
                        'logo_team': data.player.tim.logo_team.url if data.player.tim.logo_team else None
                    },
                    'nomor_punggung': data.player.nomor_punggung,
                    'tinggi_badan': data.player.tinggi_badan,
                    'berat_badan': data.player.berat_badan,
                    'tanggal_gabung': data.player.tanggal_gabung.isoformat() if data.player.tanggal_gabung else None,
                    'kelamin': data.player.kelamin,
                    'foto_profil': data.player.foto_profil.url if data.player.foto_profil else None
                },
                'training': RepoTrainingAttendancePlayer._get_training_data(data.training),
                'status': data.status,
                'reason_absent': data.reason_absent
            })
        return result

    @staticmethod
    def get_by_player(player_id):
        Player = get_object_or_404(player, player=player_id)
        attendance_list = TrainingAttendancePlayer.objects.filter(player=Player)

        result = []
        for data in attendance_list:
            result.append({
                'trainingattendance_id': data.trainingattendance_id,
                'player': {
                    'player': data.player.player,
                    'nama': data.player.nama,
                    'posisi': data.player.posisi,
                    'usia': data.player.usia,
                    'kewarganegaraan': data.player.kewarganegaraan,
                    'team': {
                        'team': data.player.tim.team,
                        'nama_team': data.player.tim.nama_team,
                        'kategori_team': data.player.tim.kategori_team,
                        'logo_team': data.player.tim.logo_team.url if data.player.tim.logo_team else None
                    },
                    'nomor_punggung': data.player.nomor_punggung,
                    'tinggi_badan': data.player.tinggi_badan,
                    'berat_badan': data.player.berat_badan,
                    'tanggal_gabung': data.player.tanggal_gabung.isoformat() if data.player.tanggal_gabung else None,
                    'kelamin': data.player.kelamin,
                    'foto_profil': data.player.foto_profil.url if data.player.foto_profil else None
                },
                'training': RepoTrainingAttendancePlayer._get_training_data(data.training),
                'status': data.status,
                'reason_absent': data.reason_absent
            })
        return result

    @staticmethod
    def get_by_training(training_id):
        """
        Retrieve attendance data for a specific training session.
        Returns:
        - Total number of players associated with the training.
        - Total number of present players and their data.
        - Total number of absent players and their data.
        - Training details.
        """
        # Validate that the training exists
        Training = get_object_or_404(training, training=training_id)

        # Filter attendance records by training_id
        attendances = TrainingAttendancePlayer.objects.filter(training__training=training_id)

        # If no records exist, return empty data with training details
        if not attendances.exists():
            return {
                'training_id': training_id,
                'total_players': 0,
                'total_present': 0,
                'present_players': [],
                'total_absent': 0,
                'absent_players': [],
                'training': RepoTrainingAttendancePlayer._get_training_data(Training)
            }

        # Separate present and absent players
        present_players = attendances.filter(status=True)
        absent_players = attendances.filter(status=False)

        # Prepare present players' data
        present_players_data = [
            {
                'player': {
                    'player_id': attendance.player.player,
                    'nama': attendance.player.nama,
                    'posisi': attendance.player.posisi,
                    'usia': attendance.player.usia,
                    'kewarganegaraan': attendance.player.kewarganegaraan,
                    'team': {
                        'team': attendance.player.tim.team,
                        'nama_team': attendance.player.tim.nama_team,
                        'kategori_team': attendance.player.tim.kategori_team,
                        'logo_team': attendance.player.tim.logo_team.url if attendance.player.tim.logo_team else None
                    },
                    'nomor_punggung': attendance.player.nomor_punggung,
                    'tinggi_badan': attendance.player.tinggi_badan,
                    'berat_badan': attendance.player.berat_badan,
                    'tanggal_gabung': attendance.player.tanggal_gabung.isoformat() if attendance.player.tanggal_gabung else None,
                    'kelamin': attendance.player.kelamin,
                    'foto_profil': attendance.player.foto_profil.url if attendance.player.foto_profil else None
                },
                'trainingattendance_id': attendance.trainingattendance_id
            }
            for attendance in present_players
        ]

        # Prepare absent players' data (include reason_absent)
        absent_players_data = [
            {
                'player': {
                    'player_id': attendance.player.player,
                    'nama': attendance.player.nama,
                    'posisi': attendance.player.posisi,
                    'usia': attendance.player.usia,
                    'kewarganegaraan': attendance.player.kewarganegaraan,
                    'team': {
                        'team': attendance.player.tim.team,
                        'nama_team': attendance.player.tim.nama_team,
                        'kategori_team': attendance.player.tim.kategori_team,
                        'logo_team': attendance.player.tim.logo_team.url if attendance.player.tim.logo_team else None
                    },
                    'nomor_punggung': attendance.player.nomor_punggung,
                    'tinggi_badan': attendance.player.tinggi_badan,
                    'berat_badan': attendance.player.berat_badan,
                    'tanggal_gabung': attendance.player.tanggal_gabung.isoformat() if attendance.player.tanggal_gabung else None,
                    'kelamin': attendance.player.kelamin,
                    'foto_profil': attendance.player.foto_profil.url if attendance.player.foto_profil else None
                },
                'trainingattendance_id': attendance.trainingattendance_id,
                'reason_absent': attendance.reason_absent
            }
            for attendance in absent_players
        ]

        # Return the aggregated data with training details
        return {
            'training_id': training_id,
            'total_players': attendances.count(),
            'total_present': present_players.count(),
            'present_players': present_players_data,
            'total_absent': absent_players.count(),
            'absent_players': absent_players_data,
            'training': RepoTrainingAttendancePlayer._get_training_data(Training)
        }
    
    @staticmethod
    def put_training_attendance_player(req):
        AttendanceData = get_object_or_404(TrainingAttendancePlayer, trainingattendance_id=req['trainingattendance_id'])
        Player = get_object_or_404(player, player=req['player'])
        Training = get_object_or_404(training, training=req['training']) if req.get('training') else AttendanceData.training

        # Update fields
        AttendanceData.player = Player
        AttendanceData.training = Training
        AttendanceData.status = req.get('status', AttendanceData.status)
        AttendanceData.reason_absent = req.get('reason_absent', AttendanceData.reason_absent)

        # Validate reason_absent if status is False
        if not AttendanceData.status:
            reason_absent = AttendanceData.reason_absent.strip() if AttendanceData.reason_absent else ''
            if not reason_absent:
                raise ValueError("reason_absent is required and cannot be empty when the player is absent")

        AttendanceData.save()

        return {
            'trainingattendance_id': AttendanceData.trainingattendance_id,
            'player': {
                'player': AttendanceData.player.player,
                'nama': AttendanceData.player.nama,
                'posisi': AttendanceData.player.posisi,
                'usia': AttendanceData.player.usia,
                'kewarganegaraan': AttendanceData.player.kewarganegaraan,
                'team': {
                    'team': AttendanceData.player.tim.team,
                    'nama_team': AttendanceData.player.tim.nama_team,
                    'kategori_team': AttendanceData.player.tim.kategori_team,
                    'logo_team': AttendanceData.player.tim.logo_team.url if AttendanceData.player.tim.logo_team else None
                },
                'nomor_punggung': AttendanceData.player.nomor_punggung,
                'tinggi_badan': AttendanceData.player.tinggi_badan,
                'berat_badan': AttendanceData.player.berat_badan,
                'tanggal_gabung': AttendanceData.player.tanggal_gabung.isoformat() if AttendanceData.player.tanggal_gabung else None,
                'kelamin': AttendanceData.player.kelamin,
                'foto_profil': AttendanceData.player.foto_profil.url if AttendanceData.player.foto_profil else None
            },
            'training': RepoTrainingAttendancePlayer._get_training_data(AttendanceData.training),
            'status': AttendanceData.status,
            'reason_absent': AttendanceData.reason_absent
        }

    @staticmethod
    def delete_training_attendance_player(req):
        AttendanceData = get_object_or_404(TrainingAttendancePlayer, trainingattendance_id=req['trainingattendance_id'])
        trainingattendance_id = AttendanceData.trainingattendance_id
        AttendanceData.delete()
        return {'message': f"Training attendance player with id {trainingattendance_id} has been deleted."}