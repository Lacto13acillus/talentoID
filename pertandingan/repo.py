from django.shortcuts import get_object_or_404
from .models import pertandingan
from team.models import team
from player.models import player
from schedule.models import schedule
from stadion.models import stadion
from status.models import status
from django.db.models import Q
from player.models import player
from training.models import training
from formations.models import Formation
from season.models import season
from LineUp.models import LineUp
from datetime import datetime
import re
from django.utils.dateparse import parse_date
from django.core.exceptions import ValidationError
import uuid
from django.utils import timezone


class RepoPertandingan:
    @staticmethod
    def _normalize_time(time_str):
        """Convert HH:MM or HH:MM:SS to a datetime.time object."""
        if not time_str:
            raise ValueError("Time string cannot be empty")

        pattern = r"^(?:[0-1][0-9]|2[0-3]):[0-5][0-9](?::[0-5][0-9])?$"
        if not re.match(pattern, time_str):
            raise ValueError(f"Invalid time format: {time_str}. Use HH:MM or HH:MM:SS")

        if len(time_str.split(":")) == 2:
            time_str = f"{time_str}:00"

        try:
            time_obj = datetime.strptime(time_str, "%H:%M:%S").time()
            return time_obj
        except ValueError as e:
            raise ValueError(f"Failed to parse time {time_str}: {str(e)}")

    @staticmethod
    def _normalize_date(date_input):
        """Convert date string (YYYY-MM-DD) to a date object."""
        if not date_input:
            raise ValidationError("Date is required")

        if date_input == "0000-00-00":
            raise ValidationError("Invalid date: '0000-00-00' is not a valid date")

        date_obj = parse_date(date_input)
        if not date_obj:
            raise ValidationError(f"Invalid date format: {date_input}. Use YYYY-MM-DD")

        try:
            datetime.strptime(date_input, "%Y-%m-%d")
        except ValueError:
            raise ValidationError(
                f"Invalid date: {date_input} is not a valid calendar date"
            )

        return date_obj

    @staticmethod
    def post(req):
        TeamHome = get_object_or_404(team, team=req["team_home"])
        TeamAway = get_object_or_404(team, team=req["team_away"])
        Schedule = (
            get_object_or_404(schedule, schedule=req["schedule"])
            if req.get("schedule")
            else None
        )
        Stadion = get_object_or_404(stadion, stadion=req["stadion"])
        Season = get_object_or_404(season, season=req["season"])
        Formasi = (
            get_object_or_404(Formation, id_formasi=req["formasi"])
            if req.get("formasi")
            else None
        )  # Diubah dari formation_team_home

        try:
            start_time = RepoPertandingan._normalize_time(req["start_time"])
            end_time = RepoPertandingan._normalize_time(req["end_time"])
            date = RepoPertandingan._normalize_date(req["date"])
        except ValidationError as e:
            raise ValidationError(str(e))
        except ValueError as e:
            raise ValueError(str(e))

        new_pertandingan = pertandingan.objects.create(
            match=req["match"],
            nama_pertandingan=req["nama_pertandingan"],
            tim_home=TeamHome,
            tim_away=TeamAway,
            formasi=Formasi,  # Diubah dari formation_team_home
            jadwal=Schedule,
            lokasi=Stadion,
            season=Season,
            date=date,
            start_time=start_time,
            end_time=end_time,
        )

        # Create LineUp records for starting and reserve players
        if "starting_players" in req and "reserve_players" in req:
            starting_players = req["starting_players"]
            reserve_players = req["reserve_players"]

            # Insert starting players
            for i, player_id in enumerate(starting_players):
                Player = get_object_or_404(player, player=player_id)
                LineUp.objects.create(
                    id_lineup=str(uuid.uuid4()),
                    match=new_pertandingan,
                    player=Player,
                    index=i,
                    status="main",
                )

            # Insert reserve players
            for i, player_id in enumerate(reserve_players):
                Player = get_object_or_404(player, player=player_id)
                LineUp.objects.create(
                    id_lineup=str(uuid.uuid4()),
                    match=new_pertandingan,
                    player=Player,
                    index=i,
                    status="reserve",
                )

        # Fetch LineUp data for the match
        lineup_data = LineUp.objects.filter(match=new_pertandingan).values(
            "id_lineup",
            "player__player",
            "player__nama",
            "player__posisi",
            "player__nomor_punggung",
            "player__foto_profil",
            "index",
            "status",
        )
        lineup_response = [
            {
                "id_lineup": item["id_lineup"],
                "player": {
                    "player": item["player__player"],
                    "nama": item["player__nama"],
                    "posisi": item["player__posisi"],
                    "nomor_punggung": item["player__nomor_punggung"],
                    "foto_profil": (
                        f"/media/{item['player__foto_profil']}"
                        if item["player__foto_profil"]
                        else None
                    ),
                },
                "index": item["index"],
                "status": item["status"],
            }
            for item in lineup_data
        ]

        formasi_data = None
        if new_pertandingan.formasi:  # Diubah dari formation_team_home
            formasi_data = {
                "id_formasi": new_pertandingan.formasi.id_formasi,
                "formasi": new_pertandingan.formasi.formasi,
            }

        schedule_data = None
        if new_pertandingan.jadwal:
            schedule_data = {
                "schedule": new_pertandingan.jadwal.schedule,
                "tanggal": (
                    new_pertandingan.jadwal.tanggal.isoformat()
                    if new_pertandingan.jadwal.tanggal
                    else None
                ),
                "start_time": (
                    new_pertandingan.jadwal.start_time.strftime("%H:%M:%S")
                    if new_pertandingan.jadwal.start_time
                    else None
                ),
                "end_time": (
                    new_pertandingan.jadwal.end_time.strftime("%H:%M:%S")
                    if new_pertandingan.jadwal.end_time
                    else None
                ),
            }
        status_instance = status.objects.get(match_status="Preparing")

        return {
            "match": new_pertandingan.match,
            "nama_pertandingan": new_pertandingan.nama_pertandingan,
            "team_home_id": TeamHome.team,
            "team_home": {
                "team": TeamHome.team,
                "nama_team": TeamHome.nama_team,
                "kategori_team": TeamHome.kategori_team,
                "logo_team": TeamHome.logo_team.url if TeamHome.logo_team else None,
            },
            "team_away": {
                "team": TeamAway.team,
                "nama_team": TeamAway.nama_team,
                "kategori_team": TeamAway.kategori_team,
                "logo_team": TeamAway.logo_team.url if TeamAway.logo_team else None,
            },
            "formasi": formasi_data,  # Diubah dari formation_team_home
            "lineup": lineup_response,
            "schedule": schedule_data,
            "stadion": {
                "stadion": Stadion.stadion,
                "nama_stadion": Stadion.nama_stadion,
                "lokasi": Stadion.lokasi,
            },
            "status_id": status_instance.status,
            "status": {
                "status": status_instance.status,
                "match_status": status_instance.match_status,
            },
            "season": {"season": Season.season, "nama_season": Season.nama_season},
            "date": new_pertandingan.date.isoformat(),
            "start_time": new_pertandingan.start_time.strftime("%H:%M"),
            "end_time": new_pertandingan.end_time.strftime("%H:%M"),
        }

    @staticmethod
    def get(pertandingan_id):
        Pertandingan = get_object_or_404(pertandingan, match=pertandingan_id)
        TeamHome = get_object_or_404(team, team=Pertandingan.tim_home.team)
        TeamAway = get_object_or_404(team, team=Pertandingan.tim_away.team)
        Schedule = Pertandingan.jadwal
        Stadion = get_object_or_404(stadion, stadion=Pertandingan.lokasi.stadion)
        Status = get_object_or_404(status, status=Pertandingan.status.status)
        Season = get_object_or_404(season, season=Pertandingan.season.season)

        # Fetch LineUp data for the match
        lineup_data = LineUp.objects.filter(match=Pertandingan).values(
            "id_lineup",
            "player__player",
            "player__nama",
            "player__posisi",
            "player__nomor_punggung",
            "player__foto_profil",
            "index",
            "status",
        )
        lineup_response = [
            {
                "id_lineup": item["id_lineup"],
                "player": {
                    "player": item["player__player"],
                    "nama": item["player__nama"],
                    "posisi": item["player__posisi"],
                    "nomor_punggung": item["player__nomor_punggung"],
                    "foto_profil": (
                        f"/media/{item['player__foto_profil']}"
                        if item["player__foto_profil"]
                        else None
                    ),
                },
                "index": item["index"],
                "status": item["status"],
            }
            for item in lineup_data
        ]

        formasi_data = None
        if Pertandingan.formasi:  # Diubah dari formation_team_home
            formasi_data = {
                "id_formasi": Pertandingan.formasi.id_formasi,
                "formasi": Pertandingan.formasi.formasi,
            }

        schedule_data = None
        if Schedule:
            schedule_data = {
                "schedule": Schedule.schedule,
                "tanggal": Schedule.tanggal.isoformat() if Schedule.tanggal else None,
                "start_time": (
                    Schedule.start_time.strftime("%H:%M:%S")
                    if Schedule.start_time
                    else None
                ),
                "end_time": (
                    Schedule.end_time.strftime("%H:%M:%S")
                    if Schedule.end_time
                    else None
                ),
            }

        return {
            "match": Pertandingan.match,
            "nama_pertandingan": Pertandingan.nama_pertandingan,
            "team_home_id": TeamHome.team,
            "team_home": {
                "team": TeamHome.team,
                "nama_team": TeamHome.nama_team,
                "kategori_team": TeamHome.kategori_team,
                "logo_team": TeamHome.logo_team.url if TeamHome.logo_team else None,
            },
            "team_away": {
                "team": TeamAway.team,
                "nama_team": TeamAway.nama_team,
                "kategori_team": TeamAway.kategori_team,
                "logo_team": TeamAway.logo_team.url if TeamAway.logo_team else None,
            },
            "formasi": formasi_data,  # Diubah dari formation_team_home
            "lineup": lineup_response,
            "schedule": schedule_data,
            "stadion": {
                "stadion": Stadion.stadion,
                "nama_stadion": Stadion.nama_stadion,
                "lokasi": Stadion.lokasi,
            },
            "status_id": Status.status,
            "status": {"status": Status.status, "match_status": Status.match_status},
            "season": {"season": Season.season, "nama_season": Season.nama_season},
            "date": Pertandingan.date.isoformat(),
            "start_time": Pertandingan.start_time.strftime("%H:%M"),
            "end_time": Pertandingan.end_time.strftime("%H:%M"),
        }

    @staticmethod
    def get_all():
        pertandingan_list = pertandingan.objects.all()
        result = []
        for pertandingan_data in pertandingan_list:
            TeamHome = get_object_or_404(team, team=pertandingan_data.tim_home.team)
            TeamAway = get_object_or_404(team, team=pertandingan_data.tim_away.team)
            Schedule = pertandingan_data.jadwal
            Stadion = get_object_or_404(
                stadion, stadion=pertandingan_data.lokasi.stadion
            )
            Status = get_object_or_404(status, status=pertandingan_data.status.status)
            Season = get_object_or_404(season, season=pertandingan_data.season.season)

            # Fetch LineUp data for the match
            lineup_data = LineUp.objects.filter(match=pertandingan_data).values(
                "id_lineup",
                "player__player",
                "player__nama",
                "player__posisi",
                "player__nomor_punggung",
                "player__foto_profil",
                "index",
                "status",
            )
            lineup_response = [
                {
                    "id_lineup": item["id_lineup"],
                    "player": {
                        "player": item["player__player"],
                        "nama": item["player__nama"],
                        "posisi": item["player__posisi"],
                        "nomor_punggung": item["player__nomor_punggung"],
                        "foto_profil": (
                            f"/media/{item['player__foto_profil']}"
                            if item["player__foto_profil"]
                            else None
                        ),
                    },
                    "index": item["index"],
                    "status": item["status"],
                }
                for item in lineup_data
            ]

            formasi_data = None
            if pertandingan_data.formasi:  # Diubah dari formation_team_home
                formasi_data = {
                    "id_formasi": pertandingan_data.formasi.id_formasi,
                    "formasi": pertandingan_data.formasi.formasi,
                }

            schedule_data = None
            if Schedule:
                schedule_data = {
                    "schedule": Schedule.schedule,
                    "tanggal": (
                        Schedule.tanggal.isoformat() if Schedule.tanggal else None
                    ),
                    "start_time": (
                        Schedule.start_time.strftime("%H:%M:%S")
                        if Schedule.start_time
                        else None
                    ),
                    "end_time": (
                        Schedule.end_time.strftime("%H:%M:%S")
                        if Schedule.end_time
                        else None
                    ),
                }

            result.append(
                {
                    "match": pertandingan_data.match,
                    "nama_pertandingan": pertandingan_data.nama_pertandingan,
                    "team_home_id": TeamHome.team,
                    "team_home": {
                        "team": TeamHome.team,
                        "nama_team": TeamHome.nama_team,
                        "kategori_team": TeamHome.kategori_team,
                        "logo_team": (
                            TeamHome.logo_team.url if TeamHome.logo_team else None
                        ),
                    },
                    "team_away": {
                        "team": TeamAway.team,
                        "nama_team": TeamAway.nama_team,
                        "kategori_team": TeamAway.kategori_team,
                        "logo_team": (
                            TeamAway.logo_team.url if TeamAway.logo_team else None
                        ),
                    },
                    "formasi": formasi_data,  # Diubah dari formation_team_home
                    "lineup": lineup_response,
                    "schedule": schedule_data,
                    "stadion": {
                        "stadion": Stadion.stadion,
                        "nama_stadion": Stadion.nama_stadion,
                        "lokasi": Stadion.lokasi,
                    },
                    "status_id": Status.status,
                    "status": {
                        "status": Status.status,
                        "match_status": Status.match_status,
                    },
                    "season": {
                        "season": Season.season,
                        "nama_season": Season.nama_season,
                    },
                    "date": pertandingan_data.date.isoformat(),
                    "start_time": pertandingan_data.start_time.strftime("%H:%M"),
                    "end_time": pertandingan_data.end_time.strftime("%H:%M"),
                }
            )
        return result

    @staticmethod
    def get_pertandingan_by_coach(coach_id, status_param=None):

        teams_dilatih = team.objects.filter(coach=coach_id)

        pertandingan_list = pertandingan.objects.select_related(
            "tim_home",
            "tim_away",
            "lokasi",
            "status",
            "season",
            "formasi",
            "jadwal",
        ).filter(Q(tim_home__in=teams_dilatih) | Q(tim_away__in=teams_dilatih))

        # =========================
        # FILTER STATUS (OPTIONAL)
        # =========================
        if status_param == "upcoming":
            today = timezone.now().date()
            pertandingan_list = pertandingan_list.filter(
                status__match_status="Preparing", date__gte=today
            )

        result = []

        for pertandingan_data in pertandingan_list:

            lineup_data = LineUp.objects.filter(match=pertandingan_data).values(
                "id_lineup",
                "player__player",
                "player__nama",
                "player__posisi",
                "player__nomor_punggung",
                "player__foto_profil",
                "index",
                "status",
            )

            lineup_response = [
                {
                    "id_lineup": item["id_lineup"],
                    "player": {
                        "player": item["player__player"],
                        "nama": item["player__nama"],
                        "posisi": item["player__posisi"],
                        "nomor_punggung": item["player__nomor_punggung"],
                        "foto_profil": (
                            f"/media/{item['player__foto_profil']}"
                            if item["player__foto_profil"]
                            else None
                        ),
                    },
                    "index": item["index"],
                    "status": item["status"],
                }
                for item in lineup_data
            ]

            formasi_data = None
            if pertandingan_data.formasi:
                formasi_data = {
                    "id_formasi": pertandingan_data.formasi.id_formasi,
                    "formasi": pertandingan_data.formasi.formasi,
                }

            schedule_data = None
            if pertandingan_data.jadwal:
                schedule_data = {
                    "schedule": pertandingan_data.jadwal.schedule,
                    "tanggal": (
                        pertandingan_data.jadwal.tanggal.isoformat()
                        if pertandingan_data.jadwal.tanggal
                        else None
                    ),
                    "start_time": (
                        pertandingan_data.jadwal.start_time.strftime("%H:%M:%S")
                        if pertandingan_data.jadwal.start_time
                        else None
                    ),
                    "end_time": (
                        pertandingan_data.jadwal.end_time.strftime("%H:%M:%S")
                        if pertandingan_data.jadwal.end_time
                        else None
                    ),
                }

            result.append(
                {
                    "match": pertandingan_data.match,
                    "nama_pertandingan": pertandingan_data.nama_pertandingan,
                    "team_home_id": pertandingan_data.tim_home.team,
                    "team_home": {
                        "team": pertandingan_data.tim_home.team,
                        "nama_team": pertandingan_data.tim_home.nama_team,
                        "kategori_team": pertandingan_data.tim_home.kategori_team,
                        "logo_team": (
                            pertandingan_data.tim_home.logo_team.url
                            if pertandingan_data.tim_home.logo_team
                            else None
                        ),
                    },
                    "team_away": {
                        "team": pertandingan_data.tim_away.team,
                        "nama_team": pertandingan_data.tim_away.nama_team,
                        "kategori_team": pertandingan_data.tim_away.kategori_team,
                        "logo_team": (
                            pertandingan_data.tim_away.logo_team.url
                            if pertandingan_data.tim_away.logo_team
                            else None
                        ),
                    },
                    "formasi": formasi_data,
                    "lineup": lineup_response,
                    "schedule": schedule_data,
                    "stadion": {
                        "stadion": pertandingan_data.lokasi.stadion,
                        "nama_stadion": pertandingan_data.lokasi.nama_stadion,
                        "lokasi": pertandingan_data.lokasi.lokasi,
                    },
                    "status_id": pertandingan_data.status.status,
                    "status": {
                        "status": pertandingan_data.status.status,
                        "match_status": pertandingan_data.status.match_status,
                    },
                    "season": {
                        "season": pertandingan_data.season.season,
                        "nama_season": pertandingan_data.season.nama_season,
                    },
                    "date": pertandingan_data.date.isoformat(),
                    "start_time": pertandingan_data.start_time.strftime("%H:%M"),
                    "end_time": pertandingan_data.end_time.strftime("%H:%M"),
                }
            )

        return result

    @staticmethod
    def get_pertandingan_by_player(player_id):
        print("get_pertandingan_by_player player_id", player_id)
        result = []
        player_result = player.objects.get(player=player_id)
        if player_result.verification_status != "Verified":
            return []
        # if player_result.membership_status == "EXPIRED":
        #     return []

        team_player = player_result.tim
        pertandingan_list = pertandingan.objects.filter(
            Q(tim_home=team_player) | Q(tim_away=team_player)
        )
        for pertandingan_data in pertandingan_list:
            TeamHome = get_object_or_404(team, team=pertandingan_data.tim_home.team)
            TeamAway = get_object_or_404(team, team=pertandingan_data.tim_away.team)
            Schedule = pertandingan_data.jadwal
            Stadion = get_object_or_404(
                stadion, stadion=pertandingan_data.lokasi.stadion
            )
            Status = get_object_or_404(status, status=pertandingan_data.status.status)
            Season = get_object_or_404(season, season=pertandingan_data.season.season)

            # Fetch LineUp data for the match
            lineup_data = LineUp.objects.filter(match=pertandingan_data).values(
                "id_lineup",
                "player__player",
                "player__nama",
                "player__posisi",
                "player__nomor_punggung",
                "player__foto_profil",
                "index",
                "status",
            )
            lineup_response = [
                {
                    "id_lineup": item["id_lineup"],
                    "player": {
                        "player": item["player__player"],
                        "nama": item["player__nama"],
                        "posisi": item["player__posisi"],
                        "nomor_punggung": item["player__nomor_punggung"],
                        "foto_profil": (
                            f"/media/{item['player__foto_profil']}"
                            if item["player__foto_profil"]
                            else None
                        ),
                    },
                    "index": item["index"],
                    "status": item["status"],
                }
                for item in lineup_data
            ]

            formasi_data = None
            if pertandingan_data.formasi:  # Diubah dari formation_team_home
                formasi_data = {
                    "id_formasi": pertandingan_data.formasi.id_formasi,
                    "formasi": pertandingan_data.formasi.formasi,
                }

            schedule_data = None
            if Schedule:
                schedule_data = {
                    "schedule": Schedule.schedule,
                    "tanggal": (
                        Schedule.tanggal.isoformat() if Schedule.tanggal else None
                    ),
                    "start_time": (
                        Schedule.start_time.strftime("%H:%M:%S")
                        if Schedule.start_time
                        else None
                    ),
                    "end_time": (
                        Schedule.end_time.strftime("%H:%M:%S")
                        if Schedule.end_time
                        else None
                    ),
                }
            result.append(
                {
                    "match": pertandingan_data.match,
                    "nama_pertandingan": pertandingan_data.nama_pertandingan,
                    "team_home_id": TeamHome.team,
                    "team_home": {
                        "team": TeamHome.team,
                        "nama_team": TeamHome.nama_team,
                        "kategori_team": TeamHome.kategori_team,
                        "logo_team": (
                            TeamHome.logo_team.url if TeamHome.logo_team else None
                        ),
                    },
                    "team_away": {
                        "team": TeamAway.team,
                        "nama_team": TeamAway.nama_team,
                        "kategori_team": TeamAway.kategori_team,
                        "logo_team": (
                            TeamAway.logo_team.url if TeamAway.logo_team else None
                        ),
                    },
                    "formasi": formasi_data,  # Diubah dari formation_team_home
                    "lineup": lineup_response,
                    "schedule": schedule_data,
                    "stadion": {
                        "stadion": Stadion.stadion,
                        "nama_stadion": Stadion.nama_stadion,
                        "lokasi": Stadion.lokasi,
                    },
                    "status_id": Status.status,
                    "status": {
                        "status": Status.status,
                        "match_status": Status.match_status,
                    },
                    "season": {
                        "season": Season.season,
                        "nama_season": Season.nama_season,
                    },
                    "date": pertandingan_data.date.isoformat(),
                    "start_time": pertandingan_data.start_time.strftime("%H:%M"),
                    "end_time": pertandingan_data.end_time.strftime("%H:%M"),
                }
            )

        return result

    @staticmethod
    def get_pertandingan_by_team(team_id):
        result = []
        pertandingan_list = pertandingan.objects.filter(
            Q(tim_home=team_id) | Q(tim_away=team_id)
        )
        for pertandingan_data in pertandingan_list:
            TeamHome = get_object_or_404(team, team=pertandingan_data.tim_home.team)
            TeamAway = get_object_or_404(team, team=pertandingan_data.tim_away.team)
            Schedule = pertandingan_data.jadwal
            Stadion = get_object_or_404(
                stadion, stadion=pertandingan_data.lokasi.stadion
            )
            Status = get_object_or_404(status, status=pertandingan_data.status.status)
            Season = get_object_or_404(season, season=pertandingan_data.season.season)

            # Fetch LineUp data for the match
            lineup_data = LineUp.objects.filter(match=pertandingan_data).values(
                "id_lineup",
                "player__player",
                "player__nama",
                "player__posisi",
                "player__nomor_punggung",
                "player__foto_profil",
                "index",
                "status",
            )
            lineup_response = [
                {
                    "id_lineup": item["id_lineup"],
                    "player": {
                        "player": item["player__player"],
                        "nama": item["player__nama"],
                        "posisi": item["player__posisi"],
                        "nomor_punggung": item["player__nomor_punggung"],
                        "foto_profil": (
                            f"/media/{item['player__foto_profil']}"
                            if item["player__foto_profil"]
                            else None
                        ),
                    },
                    "index": item["index"],
                    "status": item["status"],
                }
                for item in lineup_data
            ]

            formasi_data = None
            if pertandingan_data.formasi:  # Diubah dari formation_team_home
                formasi_data = {
                    "id_formasi": pertandingan_data.formasi.id_formasi,
                    "formasi": pertandingan_data.formasi.formasi,
                }

            schedule_data = None
            if Schedule:
                schedule_data = {
                    "schedule": Schedule.schedule,
                    "tanggal": (
                        Schedule.tanggal.isoformat() if Schedule.tanggal else None
                    ),
                    "start_time": (
                        Schedule.start_time.strftime("%H:%M:%S")
                        if Schedule.start_time
                        else None
                    ),
                    "end_time": (
                        Schedule.end_time.strftime("%H:%M:%S")
                        if Schedule.end_time
                        else None
                    ),
                }
            result.append(
                {
                    "match": pertandingan_data.match,
                    "nama_pertandingan": pertandingan_data.nama_pertandingan,
                    "team_home_id": TeamHome.team,
                    "team_home": {
                        "team": TeamHome.team,
                        "nama_team": TeamHome.nama_team,
                        "kategori_team": TeamHome.kategori_team,
                        "logo_team": (
                            TeamHome.logo_team.url if TeamHome.logo_team else None
                        ),
                    },
                    "team_away": {
                        "team": TeamAway.team,
                        "nama_team": TeamAway.nama_team,
                        "kategori_team": TeamAway.kategori_team,
                        "logo_team": (
                            TeamAway.logo_team.url if TeamAway.logo_team else None
                        ),
                    },
                    "formasi": formasi_data,  # Diubah dari formation_team_home
                    "lineup": lineup_response,
                    "schedule": schedule_data,
                    "stadion": {
                        "stadion": Stadion.stadion,
                        "nama_stadion": Stadion.nama_stadion,
                        "lokasi": Stadion.lokasi,
                    },
                    "status_id": Status.status,
                    "status": {
                        "status": Status.status,
                        "match_status": Status.match_status,
                    },
                    "season": {
                        "season": Season.season,
                        "nama_season": Season.nama_season,
                    },
                    "date": pertandingan_data.date.isoformat(),
                    "start_time": pertandingan_data.start_time.strftime("%H:%M"),
                    "end_time": pertandingan_data.end_time.strftime("%H:%M"),
                }
            )

        return result

    @staticmethod
    def get_stats_by_coach(coach_id):
        teams_dilatih = team.objects.filter(coach=coach_id)
        total_pertandingan = pertandingan.objects.filter(
            Q(tim_home__in=teams_dilatih) | Q(tim_away__in=teams_dilatih)
        ).count()
        total_training = training.objects.filter(tim__in=teams_dilatih).count()
        total_team = teams_dilatih.count()
        total_player = player.objects.filter(tim__in=teams_dilatih).count()

        return {
            "total_pertandingan": total_pertandingan if total_pertandingan else 0,
            "total_training": total_training if total_training else 0,
            "total_team": total_team if total_team else 0,
            "total_player": total_player if total_player else 0,
        }

    @staticmethod
    def put(req):
        Pertandingan = get_object_or_404(pertandingan, match=req["match"])

        Pertandingan.nama_pertandingan = req.get(
            "nama_pertandingan", Pertandingan.nama_pertandingan
        )
        if "team_home" in req:
            Pertandingan.tim_home = get_object_or_404(team, team=req["team_home"])
        if "team_away" in req:
            Pertandingan.tim_away = get_object_or_404(team, team=req["team_away"])
        if "formasi" in req:  # Diubah dari formation_team_home
            Pertandingan.formasi = (
                get_object_or_404(Formation, id_formasi=req["formasi"])
                if req["formasi"]
                else None
            )
        if "schedule" in req:
            Pertandingan.jadwal = (
                get_object_or_404(schedule, schedule=req["schedule"])
                if req["schedule"]
                else None
            )
        if "stadion" in req:
            Pertandingan.lokasi = get_object_or_404(stadion, stadion=req["stadion"])
        if "status" in req:
            Pertandingan.status = get_object_or_404(status, status=req["status"])
        if "season" in req:
            Pertandingan.season = get_object_or_404(season, season=req["season"])
        if "date" in req:
            Pertandingan.date = RepoPertandingan._normalize_date(req["date"])
        if "start_time" in req:
            Pertandingan.start_time = RepoPertandingan._normalize_time(
                req["start_time"]
            )
        if "end_time" in req:
            Pertandingan.end_time = RepoPertandingan._normalize_time(req["end_time"])

        Pertandingan.save()

        TeamHome = get_object_or_404(team, team=Pertandingan.tim_home.team)
        TeamAway = get_object_or_404(team, team=Pertandingan.tim_away.team)
        Schedule = Pertandingan.jadwal
        Stadion = get_object_or_404(stadion, stadion=Pertandingan.lokasi.stadion)
        Status = get_object_or_404(status, status=Pertandingan.status.status)
        Season = get_object_or_404(season, season=Pertandingan.season.season)

        # Fetch LineUp data for the match
        lineup_data = LineUp.objects.filter(match=Pertandingan).values(
            "id_lineup",
            "player__player",
            "player__nama",
            "player__posisi",
            "player__nomor_punggung",
            "player__foto_profil",
            "index",
            "status",
        )
        lineup_response = [
            {
                "id_lineup": item["id_lineup"],
                "player": {
                    "player": item["player__player"],
                    "nama": item["player__nama"],
                    "posisi": item["player__posisi"],
                    "nomor_punggung": item["player__nomor_punggung"],
                    "foto_profil": (
                        f"/media/{item['player__foto_profil']}"
                        if item["player__foto_profil"]
                        else None
                    ),
                },
                "index": item["index"],
                "status": item["status"],
            }
            for item in lineup_data
        ]

        formasi_data = None
        if Pertandingan.formasi:  # Diubah dari formation_team_home
            formasi_data = {
                "id_formasi": Pertandingan.formasi.id_formasi,
                "formasi": Pertandingan.formasi.formasi,
            }

        schedule_data = None
        if Schedule:
            schedule_data = {
                "schedule": Schedule.schedule,
                "tanggal": Schedule.tanggal.isoformat() if Schedule.tanggal else None,
                "start_time": (
                    Schedule.start_time.strftime("%H:%M:%S")
                    if Schedule.start_time
                    else None
                ),
                "end_time": (
                    Schedule.end_time.strftime("%H:%M:%S")
                    if Schedule.end_time
                    else None
                ),
            }

        return {
            "match": Pertandingan.match,
            "nama_pertandingan": Pertandingan.nama_pertandingan,
            "team_home_id": TeamHome.team,
            "team_home": {
                "team": TeamHome.team,
                "nama_team": TeamHome.nama_team,
                "kategori_team": TeamHome.kategori_team,
                "logo_team": TeamHome.logo_team.url if TeamHome.logo_team else None,
            },
            "team_away": {
                "team": TeamAway.team,
                "nama_team": TeamAway.nama_team,
                "kategori_team": TeamAway.kategori_team,
                "logo_team": TeamAway.logo_team.url if TeamAway.logo_team else None,
            },
            "formasi": formasi_data,  # Diubah dari formation_team_home
            "lineup": lineup_response,
            "schedule": schedule_data,
            "stadion": {
                "stadion": Stadion.stadion,
                "nama_stadion": Stadion.nama_stadion,
                "lokasi": Stadion.lokasi,
            },
            "status_id": Status.status,
            "status": {"status": Status.status, "match_status": Status.match_status},
            "season": {"season": Season.season, "nama_season": Season.nama_season},
            "date": Pertandingan.date.isoformat(),
            "start_time": Pertandingan.start_time.strftime("%H:%M"),
            "end_time": Pertandingan.end_time.strftime("%H:%M"),
        }

    @staticmethod
    def delete(req):
        Pertandingan = get_object_or_404(pertandingan, match=req["match"])
        Pertandingan.delete()
        return {"message": f"Pertandingan with id {req['match']} has been deleted."}

    @staticmethod
    def update_status_to_ready(match_id):
        match = get_object_or_404(pertandingan, match=match_id)

        if match.status.match_status != "Preparing":
            raise ValueError("Match tidak dalam status 'preparing'")

        ready_status = get_object_or_404(status, match_status="Ready")

        if not ready_status:
            raise ValueError("Status 'Ready' tidak ditemukan")

        match.status = ready_status
        match.save()

        return match
