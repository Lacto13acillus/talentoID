from django.shortcuts import get_object_or_404
from .models import attendance
from training.models import training
from player.models import player
import uuid

class RepoAttendance:
    @staticmethod
    def _get_training_data(training_instance):
        """Helper method to construct detailed training data."""
        if not training_instance:
            return None

        training_data = {
            'training': training_instance.training,
            'nama_latihan': training_instance.nama_latihan,
            'team': {
                'team': training_instance.tim.team if training_instance.tim else None,
                'nama_team': training_instance.tim.nama_team if training_instance.tim else None,
                'kategori_team': training_instance.tim.kategori_team if training_instance.tim else None,
                'logo_team': training_instance.tim.logo_team.url if training_instance.tim and training_instance.tim.logo_team else None
            },
            'schedule': {
                'schedule': training_instance.jadwal.schedule if training_instance.jadwal else None,
                'tanggal': training_instance.jadwal.tanggal.isoformat() if training_instance.jadwal and training_instance.jadwal.tanggal else None,
                'start_time': training_instance.jadwal.start_time.strftime('%H:%M:%S') if training_instance.jadwal and training_instance.jadwal.start_time else None,
                'end_time': training_instance.jadwal.end_time.strftime('%H:%M:%S') if training_instance.jadwal and training_instance.jadwal.end_time else None
            } if training_instance.jadwal else None,
            'stadion': {
                'stadion': training_instance.lokasi.stadion if training_instance.lokasi else None,
                'nama_stadion': training_instance.lokasi.nama_stadion if training_instance.lokasi else None,
                'lokasi': training_instance.lokasi.lokasi if training_instance.lokasi else None
            },
            'trainingcategory': [
                {
                    'trainingcategory': category.trainingcategory,
                    'nama_category': category.nama_category
                } for category in training_instance.kategori.all()
            ] if training_instance.kategori.exists() else [],
            'frequency': {
                'frequency': training_instance.frequency.frequency if training_instance.frequency else None,
                'frequency_time': training_instance.frequency.get_frequency_time_display() if training_instance.frequency else None
            } if training_instance.frequency else None,
            'date': training_instance.date.isoformat() if training_instance.date else None,
            'start_time': training_instance.start_time.strftime('%H:%M:%S') if training_instance.start_time else None,
            'end_time': training_instance.end_time.strftime('%H:%M:%S') if training_instance.end_time else None,
            'deskripsi': training_instance.deskripsi
        }
        return training_data

    @staticmethod
    def post_training(req):
        Training = get_object_or_404(training, training=req['training']) if req.get('training') else None
        attendances = []

        for attendance_data in req['attendances']:
            Player = get_object_or_404(player, player=attendance_data['player'])
            attendance_id = str(uuid.uuid4())

            new_attendance = attendance.objects.create(
                attendance=attendance_id,
                player=Player,
                training=Training,
                attendance_status=attendance_data['attendance_status'],
                notes=attendance_data.get('notes')
            )

            attendances.append({
                'attendance': new_attendance.attendance,
                'player': {
                    'player': new_attendance.player.player,
                    'nama': new_attendance.player.nama,
                    'posisi': new_attendance.player.posisi,
                    'kewarganegaraan': new_attendance.player.kewarganegaraan,
                    'team': {
                        'team': new_attendance.player.tim.team if new_attendance.player.tim else None,
                        'nama_team': new_attendance.player.tim.nama_team if new_attendance.player.tim else None,
                        'kategori_team': new_attendance.player.tim.kategori_team if new_attendance.player.tim else None,
                        'logo_team': new_attendance.player.tim.logo_team.url if new_attendance.player.tim and new_attendance.player.tim.logo_team else None
                    },
                    'nomor_punggung': new_attendance.player.nomor_punggung,
                    'tinggi_badan': new_attendance.player.tinggi_badan,
                    'berat_badan': new_attendance.player.berat_badan,
                    'tanggal_gabung': new_attendance.player.tanggal_gabung.isoformat() if new_attendance.player.tanggal_gabung else None,
                    'kelamin': new_attendance.player.kelamin,
                    'foto_profil': new_attendance.player.foto_profil.url if new_attendance.player.foto_profil else None
                },
                'training': RepoAttendance._get_training_data(new_attendance.training),
                'attendance_status': new_attendance.attendance_status,
                'notes': new_attendance.notes
            })

        return attendances

    @staticmethod
    def get_training(attendance_id):
        attendance_data = get_object_or_404(attendance, attendance=attendance_id)

        return {
            'attendance': attendance_data.attendance,
            'player': {
                'player': attendance_data.player.player,
                'nama': attendance_data.player.nama,
                'posisi': attendance_data.player.posisi,
                'kewarganegaraan': attendance_data.player.kewarganegaraan,
                'team': {
                    'team': attendance_data.player.tim.team if attendance_data.player.tim else None,
                    'nama_team': attendance_data.player.tim.nama_team if attendance_data.player.tim else None,
                    'kategori_team': attendance_data.player.tim.kategori_team if attendance_data.player.tim else None,
                    'logo_team': attendance_data.player.tim.logo_team.url if attendance_data.player.tim and attendance_data.player.tim.logo_team else None
                },
                'nomor_punggung': attendance_data.player.nomor_punggung,
                'tinggi_badan': attendance_data.player.tinggi_badan,
                'berat_badan': attendance_data.player.berat_badan,
                'tanggal_gabung': attendance_data.player.tanggal_gabung.isoformat() if attendance_data.player.tanggal_gabung else None,
                'kelamin': attendance_data.player.kelamin,
                'foto_profil': attendance_data.player.foto_profil.url if attendance_data.player.foto_profil else None
            },
            'training': RepoAttendance._get_training_data(attendance_data.training),
            'attendance_status': attendance_data.attendance_status,
            'notes': attendance_data.notes
        }

    @staticmethod
    def get_all_training():
        attendance_list = attendance.objects.all()
        result = []
        for data in attendance_list:
            try:
                result.append({
                    'attendance': data.attendance,
                    'player': {
                        'player': data.player.player,
                        'nama': data.player.nama,
                        'posisi': data.player.posisi,
                        'kewarganegaraan': data.player.kewarganegaraan,
                        'team': {
                            'team': data.player.tim.team if data.player.tim else None,
                            'nama_team': data.player.tim.nama_team if data.player.tim else None,
                            'kategori_team': data.player.tim.kategori_team if data.player.tim else None,
                            'logo_team': data.player.tim.logo_team.url if data.player.tim and data.player.tim.logo_team else None
                        },
                        'nomor_punggung': data.player.nomor_punggung,
                        'tinggi_badan': data.player.tinggi_badan,
                        'berat_badan': data.player.berat_badan,
                        'tanggal_gabung': data.player.tanggal_gabung.isoformat() if data.player.tanggal_gabung else None,
                        'kelamin': data.player.kelamin,
                        'foto_profil': data.player.foto_profil.url if data.player.foto_profil else None
                    },
                    'training': RepoAttendance._get_training_data(data.training),
                    'attendance_status': data.attendance_status,
                    'notes': data.notes
                })
            except Exception as e:
                print(f"Error processing attendance {data.attendance}: {str(e)}")
                continue
        return result

    @staticmethod
    def get_by_player(player_id):
        Player = get_object_or_404(player, player=player_id)
        attendance_list = attendance.objects.filter(player=Player)
        result = []
        for data in attendance_list:
            try:
                result.append({
                    'attendance': data.attendance,
                    'player': {
                        'player': data.player.player,
                        'nama': data.player.nama,
                        'posisi': data.player.posisi,
                        'kewarganegaraan': data.player.kewarganegaraan,
                        'team': {
                            'team': data.player.tim.team if data.player.tim else None,
                            'nama_team': data.player.tim.nama_team if data.player.tim else None,
                            'kategori_team': data.player.tim.kategori_team if data.player.tim else None,
                            'logo_team': data.player.tim.logo_team.url if data.player.tim and data.player.tim.logo_team else None
                        },
                        'nomor_punggung': data.player.nomor_punggung,
                        'tinggi_badan': data.player.tinggi_badan,
                        'berat_badan': data.player.berat_badan,
                        'tanggal_gabung': data.player.tanggal_gabung.isoformat() if data.player.tanggal_gabung else None,
                        'kelamin': data.player.kelamin,
                        'foto_profil': data.player.foto_profil.url if data.player.foto_profil else None
                    },
                    'training': RepoAttendance._get_training_data(data.training),
                    'attendance_status': data.attendance_status,
                    'notes': data.notes
                })
            except Exception as e:
                print(f"Error processing attendance {data.attendance}: {str(e)}")
                continue
        return result

    @staticmethod
    def put_training(req):
        AttendanceData = get_object_or_404(attendance, attendance=req['attendance'])
        Player = get_object_or_404(player, player=req['player'])
        Training = get_object_or_404(training, training=req['training']) if req.get('training') else AttendanceData.training

        # Update fields
        AttendanceData.player = Player
        AttendanceData.training = Training
        AttendanceData.attendance_status = req.get('attendance_status', AttendanceData.attendance_status)
        AttendanceData.notes = req.get('notes', AttendanceData.notes)
        AttendanceData.save()

        return {
            'attendance': AttendanceData.attendance,
            'player': {
                'player': AttendanceData.player.player,
                'nama': AttendanceData.player.nama,
                'posisi': AttendanceData.player.posisi,
                'kewarganegaraan': AttendanceData.player.kewarganegaraan,
                'team': {
                    'team': AttendanceData.player.tim.team if AttendanceData.player.tim else None,
                    'nama_team': AttendanceData.player.tim.nama_team if AttendanceData.player.tim else None,
                    'kategori_team': AttendanceData.player.tim.kategori_team if AttendanceData.player.tim else None,
                    'logo_team': AttendanceData.player.tim.logo_team.url if AttendanceData.player.tim and AttendanceData.player.tim.logo_team else None
                },
                'nomor_punggung': AttendanceData.player.nomor_punggung,
                'tinggi_badan': AttendanceData.player.tinggi_badan,
                'berat_badan': AttendanceData.player.berat_badan,
                'tanggal_gabung': AttendanceData.player.tanggal_gabung.isoformat() if AttendanceData.player.tanggal_gabung else None,
                'kelamin': AttendanceData.player.kelamin,
                'foto_profil': AttendanceData.player.foto_profil.url if AttendanceData.player.foto_profil else None
            },
            'training': RepoAttendance._get_training_data(AttendanceData.training),
            'attendance_status': AttendanceData.attendance_status,
            'notes': AttendanceData.notes
        }

    @staticmethod
    def delete_training(req):
        AttendanceData = get_object_or_404(attendance, attendance=req['attendance'])
        attendance_id = AttendanceData.attendance
        AttendanceData.delete()
        return {'message': f"Training attendance with id {attendance_id} has been deleted."}


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
        attendances = attendance.objects.filter(training__training=training_id)

        # If no records exist, return empty data with training details
        if not attendances.exists():
            return {
                'training_id': training_id,
                'total_players': 0,
                'total_present': 0,
                'present_players': [],
                'total_absent': 0,
                'absent_players': [],
                'training': RepoAttendance._get_training_data(Training)
            }

        # Separate present and absent players
        present_players = attendances.filter(attendance_status="Present")
        absent_players = attendances.filter(attendance_status="Absent")

        # Prepare present players' data
        present_players_data = [
           {
                    'player': attendance.player.player,
                    'nama': attendance.player.nama,
                    'posisi': attendance.player.posisi,
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
                }

            for attendance in present_players
        ]

        # Prepare absent players' data (include reason_absent)
        absent_players_data = [
            {
                    'player': attendance.player.player,
                    'nama': attendance.player.nama,
                    'posisi': attendance.player.posisi,
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
            'training': RepoAttendance._get_training_data(Training)
        }
