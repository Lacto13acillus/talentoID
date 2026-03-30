from django.shortcuts import get_object_or_404
from .models import MatchAttendance
from player.models import player
from pertandingan.models import pertandingan
import uuid


class RepoMatchAttendance:
    @staticmethod
    def _get_match_data(match):
        """Helper method to construct detailed match data."""
        if not match:
            return None

        team_home_data = {
            "team": match.tim_home.team,
            "nama_team": match.tim_home.nama_team,
            "kategori_team": match.tim_home.kategori_team,
            "logo_team": (
                match.tim_home.logo_team.url if match.tim_home.logo_team else None
            ),
        }
        team_away_data = {
            "team": match.tim_away.team,
            "nama_team": match.tim_away.nama_team,
            "kategori_team": match.tim_away.kategori_team,
            "logo_team": (
                match.tim_away.logo_team.url if match.tim_away.logo_team else None
            ),
        }
        schedule_data = None
        if match.jadwal:
            schedule_data = {
                "schedule": match.jadwal.schedule,
                "tanggal": (
                    match.jadwal.tanggal.isoformat() if match.jadwal.tanggal else None
                ),
                "start_time": (
                    match.jadwal.start_time.strftime("%H:%M:%S")
                    if match.jadwal.start_time
                    else None
                ),
                "end_time": (
                    match.jadwal.end_time.strftime("%H:%M:%S")
                    if match.jadwal.end_time
                    else None
                ),
            }
        stadion_data = None
        if match.lokasi:
            stadion_data = {
                "stadion": match.lokasi.stadion,
                "nama_stadion": match.lokasi.nama_stadion,
                "lokasi": match.lokasi.lokasi,
            }
        status_data = None
        if match.status:
            status_data = {
                "status": match.status.status,
                "match_status": match.status.match_status,
            }
        season_data = None
        if match.season:
            season_data = {
                "season": match.season.season,
                "nama_season": match.season.nama_season,
            }
        formasi_data = None
        if match.formasi:  # Diubah dari formation_team_home
            formasi_data = {
                "id_formasi": match.formasi.id_formasi,
                "formasi": match.formasi.formasi,
            }

        return {
            "match": match.match,
            "nama_pertandingan": match.nama_pertandingan,
            "team_home": team_home_data,
            "team_away": team_away_data,
            "formasi": formasi_data,  # Diubah dari formation_team_home
            "schedule": schedule_data,
            "stadion": stadion_data,
            "status": status_data,
            "season": season_data,
            "date": match.date.isoformat() if match.date else None,
            "start_time": (
                match.start_time.strftime("%H:%M") if match.start_time else None
            ),
            "end_time": match.end_time.strftime("%H:%M") if match.end_time else None,
        }

    @staticmethod
    def post_match_attendance(req):
        Match = (
            get_object_or_404(pertandingan, match=req["match"])
            if req.get("match")
            else None
        )
        attendances = []

        for attendance_data in req["match_attendances"]:
            Player = get_object_or_404(player, player=attendance_data["player"])
            match_attendance_id = str(uuid.uuid4())

            new_match_attendance = MatchAttendance.objects.create(
                match_attendance=match_attendance_id,
                player=Player,
                match=Match,
                attendance_status=attendance_data["attendance_status"],
                notes=attendance_data.get("notes"),
            )

            attendances.append(
                {
                    "match_attendance": new_match_attendance.match_attendance,
                    "player": {
                        "player": new_match_attendance.player.player,
                        "nama": new_match_attendance.player.nama,
                        "posisi": new_match_attendance.player.posisi,
                        "team": {
                            "team": new_match_attendance.player.tim.team,
                            "nama_team": new_match_attendance.player.tim.nama_team,
                            "kategori_team": new_match_attendance.player.tim.kategori_team,
                            "logo_team": (
                                new_match_attendance.player.tim.logo_team.url
                                if new_match_attendance.player.tim.logo_team
                                else None
                            ),
                        },
                        "nomor_punggung": new_match_attendance.player.nomor_punggung,
                        "tinggi_badan": new_match_attendance.player.tinggi_badan,
                        "berat_badan": new_match_attendance.player.berat_badan,
                        "tanggal_gabung": (
                            new_match_attendance.player.tanggal_gabung.isoformat()
                            if new_match_attendance.player.tanggal_gabung
                            else None
                        ),
                        "kelamin": new_match_attendance.player.kelamin,
                        "foto_profil": (
                            new_match_attendance.player.foto_profil.url
                            if new_match_attendance.player.foto_profil
                            else None
                        ),
                    },
                    "match": RepoMatchAttendance._get_match_data(
                        new_match_attendance.match
                    ),
                    "attendance_status": new_match_attendance.attendance_status,
                    "notes": new_match_attendance.notes,
                }
            )

        return attendances

    @staticmethod
    def get_match_attendance(match_attendance_id):
        match_attendance_data = get_object_or_404(
            MatchAttendance, match_attendance=match_attendance_id
        )

        return {
            "match_attendance": match_attendance_data.match_attendance,
            "player": {
                "player": match_attendance_data.player.player,
                "nama": match_attendance_data.player.nama,
                "posisi": match_attendance_data.player.posisi,
                "team": {
                    "team": match_attendance_data.player.tim.team,
                    "nama_team": match_attendance_data.player.tim.nama_team,
                    "kategori_team": match_attendance_data.player.tim.kategori_team,
                    "logo_team": (
                        match_attendance_data.player.tim.logo_team.url
                        if match_attendance_data.player.tim.logo_team
                        else None
                    ),
                },
                "nomor_punggung": match_attendance_data.player.nomor_punggung,
                "tinggi_badan": match_attendance_data.player.tinggi_badan,
                "berat_badan": match_attendance_data.player.berat_badan,
                "tanggal_gabung": (
                    match_attendance_data.player.tanggal_gabung.isoformat()
                    if match_attendance_data.player.tanggal_gabung
                    else None
                ),
                "kelamin": match_attendance_data.player.kelamin,
                "foto_profil": (
                    match_attendance_data.player.foto_profil.url
                    if match_attendance_data.player.foto_profil
                    else None
                ),
            },
            "match": RepoMatchAttendance._get_match_data(match_attendance_data.match),
            "attendance_status": match_attendance_data.attendance_status,
            "notes": match_attendance_data.notes,
        }

    @staticmethod
    def get_all_match_attendance():
        match_attendance_list = MatchAttendance.objects.all()

        result = []
        for data in match_attendance_list:
            result.append(
                {
                    "match_attendance": data.match_attendance,
                    "player": {
                        "player": data.player.player,
                        "nama": data.player.nama,
                        "posisi": data.player.posisi,
                        "team": {
                            "team": data.player.tim.team,
                            "nama_team": data.player.tim.nama_team,
                            "kategori_team": data.player.tim.kategori_team,
                            "logo_team": (
                                data.player.tim.logo_team.url
                                if data.player.tim.logo_team
                                else None
                            ),
                        },
                        "nomor_punggung": data.player.nomor_punggung,
                        "tinggi_badan": data.player.tinggi_badan,
                        "berat_badan": data.player.berat_badan,
                        "tanggal_gabung": (
                            data.player.tanggal_gabung.isoformat()
                            if data.player.tanggal_gabung
                            else None
                        ),
                        "kelamin": data.player.kelamin,
                        "foto_profil": (
                            data.player.foto_profil.url
                            if data.player.foto_profil
                            else None
                        ),
                    },
                    "match": RepoMatchAttendance._get_match_data(data.match),
                    "attendance_status": data.attendance_status,
                    "notes": data.notes,
                }
            )
        return result

    @staticmethod
    def get_by_player(player_id):
        Player = get_object_or_404(player, player=player_id)
        match_attendance_list = MatchAttendance.objects.filter(player=Player)

        result = []
        for data in match_attendance_list:
            result.append(
                {
                    "match_attendance": data.match_attendance,
                    "player": {
                        "player": data.player.player,
                        "nama": data.player.nama,
                        "posisi": data.player.posisi,
                        "team": {
                            "team": data.player.tim.team,
                            "nama_team": data.player.tim.nama_team,
                            "kategori_team": data.player.tim.kategori_team,
                            "logo_team": (
                                data.player.tim.logo_team.url
                                if data.player.tim.logo_team
                                else None
                            ),
                        },
                        "nomor_punggung": data.player.nomor_punggung,
                        "tinggi_badan": data.player.tinggi_badan,
                        "berat_badan": data.player.berat_badan,
                        "tanggal_gabung": (
                            data.player.tanggal_gabung.isoformat()
                            if data.player.tanggal_gabung
                            else None
                        ),
                        "kelamin": data.player.kelamin,
                        "foto_profil": (
                            data.player.foto_profil.url
                            if data.player.foto_profil
                            else None
                        ),
                    },
                    "match": RepoMatchAttendance._get_match_data(data.match),
                    "attendance_status": data.attendance_status,
                    "notes": data.notes,
                }
            )
        return result

    @staticmethod
    def put_match_attendance(req):
        MatchAttendanceData = get_object_or_404(
            MatchAttendance, match_attendance=req["match_attendance"]
        )
        Player = get_object_or_404(player, player=req["player"])
        Match = (
            get_object_or_404(pertandingan, match=req["match"])
            if req.get("match")
            else MatchAttendanceData.match
        )

        # Update fields
        MatchAttendanceData.player = Player
        MatchAttendanceData.match = Match
        MatchAttendanceData.attendance_status = req.get(
            "attendance_status", MatchAttendanceData.attendance_status
        )
        MatchAttendanceData.notes = req.get("notes", MatchAttendanceData.notes)
        MatchAttendanceData.save()

        return {
            "match_attendance": MatchAttendanceData.match_attendance,
            "player": {
                "player": MatchAttendanceData.player.player,
                "nama": MatchAttendanceData.player.nama,
                "posisi": MatchAttendanceData.player.posisi,
                "team": {
                    "team": MatchAttendanceData.player.tim.team,
                    "nama_team": MatchAttendanceData.player.tim.nama_team,
                    "kategori_team": MatchAttendanceData.player.tim.kategori_team,
                    "logo_team": (
                        MatchAttendanceData.player.tim.logo_team.url
                        if MatchAttendanceData.player.tim.logo_team
                        else None
                    ),
                },
                "nomor_punggung": MatchAttendanceData.player.nomor_punggung,
                "tinggi_badan": MatchAttendanceData.player.tinggi_badan,
                "berat_badan": MatchAttendanceData.player.berat_badan,
                "tanggal_gabung": (
                    MatchAttendanceData.player.tanggal_gabung.isoformat()
                    if MatchAttendanceData.player.tanggal_gabung
                    else None
                ),
                "kelamin": MatchAttendanceData.player.kelamin,
                "foto_profil": (
                    MatchAttendanceData.player.foto_profil.url
                    if MatchAttendanceData.player.foto_profil
                    else None
                ),
            },
            "match": RepoMatchAttendance._get_match_data(MatchAttendanceData.match),
            "attendance_status": MatchAttendanceData.attendance_status,
            "notes": MatchAttendanceData.notes,
        }

    @staticmethod
    def delete_match_attendance(req):
        MatchAttendanceData = get_object_or_404(
            MatchAttendance, match_attendance=req["match_attendance"]
        )
        match_attendance_id = MatchAttendanceData.match_attendance
        MatchAttendanceData.delete()
        return {
            "message": f"Match attendance with id {match_attendance_id} has been deleted."
        }
