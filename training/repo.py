from django.shortcuts import get_object_or_404
from .models import training
from team.models import team
from schedule.models import schedule
from stadion.models import stadion
from player.models import player
from TrainingCategory.models import trainingcategory
from frequency.models import frequency
from datetime import datetime
import re
from django.utils.dateparse import parse_date
from django.core.exceptions import ValidationError
from django.utils import timezone


class RepoTraining:
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
        if date_input is None or date_input == "":
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
        Team = get_object_or_404(team, team=req["team"])
        Schedule = (
            get_object_or_404(schedule, schedule=req["schedule"])
            if req.get("schedule")
            else None
        )
        Stadion = get_object_or_404(stadion, stadion=req["stadion"])
        Frequency = (
            get_object_or_404(frequency, frequency=req["frequency"])
            if req.get("frequency")
            else None
        )

        try:
            start_time = RepoTraining._normalize_time(req["start_time"])
            end_time = RepoTraining._normalize_time(req["end_time"])
            date = RepoTraining._normalize_date(req["date"])
        except ValidationError as e:
            raise ValidationError(str(e))
        except ValueError as e:
            raise ValueError(str(e))

        new_training = training.objects.create(
            training=req["training"],
            nama_latihan=req["nama_latihan"],
            tim=Team,
            jadwal=Schedule,
            lokasi=Stadion,
            frequency=Frequency,
            date=date,
            start_time=start_time,
            end_time=end_time,
            deskripsi=req["deskripsi"],
        )

        # Handle trainingcategory (single or list)
        training_categories = req["trainingcategory"]
        if isinstance(training_categories, str):
            training_categories = [training_categories]
        for category_id in training_categories:
            category = get_object_or_404(trainingcategory, trainingcategory=category_id)
            new_training.kategori.add(category)

        schedule_data = None
        if new_training.jadwal:
            schedule_data = {
                "schedule": new_training.jadwal.schedule,
                "tanggal": new_training.jadwal.tanggal,
                "start_time": (
                    new_training.jadwal.start_time.strftime("%H:%M")
                    if new_training.jadwal.start_time
                    else None
                ),
                "end_time": (
                    new_training.jadwal.end_time.strftime("%H:%M")
                    if new_training.jadwal.end_time
                    else None
                ),
            }

        frequency_data = None
        if new_training.frequency:
            frequency_data = {
                "frequency": new_training.frequency.frequency,
                "frequency_time": new_training.frequency.get_frequency_time_display(),
            }

        categories_data = [
            {
                "trainingcategory": category.trainingcategory,
                "nama_category": category.nama_category,
            }
            for category in new_training.kategori.all()
        ]

        return {
            "training": new_training.training,
            "nama_latihan": new_training.nama_latihan,
            "team_id": Team.team,
            "team": {
                "team": Team.team,
                "nama_team": Team.nama_team,
                "kategori_team": Team.kategori_team,
                "logo_team": Team.logo_team.url if Team.logo_team else None,
            },
            "schedule": schedule_data,
            "stadion": {
                "stadion": Stadion.stadion,
                "nama_stadion": Stadion.nama_stadion,
                "lokasi": Stadion.lokasi,
            },
            "trainingcategory": categories_data,
            "frequency": frequency_data,
            "frequency_id": Frequency.frequency,
            "date": new_training.date.isoformat(),
            "start_time": new_training.start_time.strftime("%H:%M"),
            "end_time": new_training.end_time.strftime("%H:%M"),
            "deskripsi": new_training.deskripsi,
        }

    @staticmethod
    def get(training_id):
        Training = get_object_or_404(training, training=training_id)
        Team = get_object_or_404(team, team=Training.tim.team)
        Schedule = Training.jadwal
        Stadion = get_object_or_404(stadion, stadion=Training.lokasi.stadion)
        Frequency = Training.frequency

        schedule_data = None
        if Schedule:
            schedule_data = {
                "schedule": Schedule.schedule,
                "tanggal": Schedule.tanggal,
                "start_time": (
                    Schedule.start_time.strftime("%H:%M")
                    if Schedule.start_time
                    else None
                ),
                "end_time": (
                    Schedule.end_time.strftime("%H:%M") if Schedule.end_time else None
                ),
            }

        frequency_data = None
        if Frequency:
            frequency_data = {
                "frequency": Frequency.frequency,
                "frequency_time": Frequency.get_frequency_time_display(),
            }

        categories_data = [
            {
                "trainingcategory": category.trainingcategory,
                "nama_category": category.nama_category,
            }
            for category in Training.kategori.all()
        ]

        return {
            "training": Training.training,
            "nama_latihan": Training.nama_latihan,
            "team_id": Team.team,
            "team": {
                "team": Team.team,
                "nama_team": Team.nama_team,
                "kategori_team": Team.kategori_team,
                "coach": Team.coach.coach if Team.coach else None,
                "logo_team": Team.logo_team.url if Team.logo_team else None,
            },
            "schedule": schedule_data,
            "stadion": {
                "stadion": Stadion.stadion,
                "nama_stadion": Stadion.nama_stadion,
                "lokasi": Stadion.lokasi,
            },
            "trainingcategory": categories_data,
            "frequency": frequency_data,
            "frequency_id": Frequency.frequency,
            "date": Training.date.isoformat(),
            "start_time": Training.start_time.strftime("%H:%M"),
            "end_time": Training.end_time.strftime("%H:%M"),
            "deskripsi": Training.deskripsi,
        }

    @staticmethod
    def get_by_coach(coach_id):

        today = timezone.now().date()

        teams = team.objects.filter(coach=coach_id)
        trainings = training.objects.filter(tim__in=teams).order_by("-date")

        # 7 event sebelum hari ini (termasuk hari ini ke bawah, diurutkan descending lalu dibalik)
        past_events = trainings.filter(date__lt=today).order_by("-date")[:7]
        past_events = sorted(
            past_events, key=lambda x: x.date
        )  # balik urutan jadi ascending

        # event hari ini
        today_events = list(trainings.filter(date=today).order_by("start_time"))

        # 7 event setelah hari ini
        future_events = list(trainings.filter(date__gt=today).order_by("date")[:7])

        training_list = list(past_events) + today_events + future_events

        result = []

        for t in training_list:
            schedule_data = None
            if t.jadwal:
                schedule_data = {
                    "schedule": t.jadwal.schedule,
                    "tanggal": t.jadwal.tanggal,
                    "start_time": (
                        t.jadwal.start_time.strftime("%H:%M")
                        if t.jadwal.start_time
                        else None
                    ),
                    "end_time": (
                        t.jadwal.end_time.strftime("%H:%M")
                        if t.jadwal.end_time
                        else None
                    ),
                }

            frequency_data = None
            if t.frequency:
                frequency_data = {
                    "frequency": t.frequency.frequency,
                    "frequency_time": t.frequency.get_frequency_time_display(),
                }

            categories_data = [
                {
                    "trainingcategory": category.trainingcategory,
                    "nama_category": category.nama_category,
                }
                for category in t.kategori.all()
            ]

            result.append(
                {
                    "training": t.training,
                    "nama_latihan": t.nama_latihan,
                    "team_id": t.tim.team,
                    "team": {
                        "team": t.tim.team,
                        "nama_team": t.tim.nama_team,
                        "kategori_team": t.tim.kategori_team,
                        "coach": t.tim.coach.coach if t.tim.coach else None,
                        "logo_team": t.tim.logo_team.url if t.tim.logo_team else None,
                    },
                    "schedule": schedule_data,
                    "stadion": {
                        "stadion": t.lokasi.stadion,
                        "nama_stadion": t.lokasi.nama_stadion,
                        "lokasi": t.lokasi.lokasi,
                    },
                    "trainingcategory": categories_data,
                    "frequency_id": (
                        frequency_data["frequency"] if frequency_data else None
                    ),
                    "frequency": frequency_data,
                    "date": t.date.isoformat(),
                    "start_time": t.start_time.strftime("%H:%M"),
                    "end_time": t.end_time.strftime("%H:%M"),
                    "deskripsi": t.deskripsi,
                }
            )
        return result

    @staticmethod
    def get_by_player(player_id):
        print("player_id", player_id)
        player_result = player.objects.get(player=player_id)
        if player_result.verification_status != "Verified":
            return []
        # if player_result.membership_status == "EXPIRED":
        #     return []
        team_player = player_result.tim
        trainings = training.objects.filter(tim=team_player).order_by("-date")
        result = []
        for t in trainings:
            schedule_data = None
            if t.jadwal:
                schedule_data = {
                    "schedule": t.jadwal.schedule,
                    "tanggal": t.jadwal.tanggal,
                    "start_time": (
                        t.jadwal.start_time.strftime("%H:%M")
                        if t.jadwal.start_time
                        else None
                    ),
                    "end_time": (
                        t.jadwal.end_time.strftime("%H:%M")
                        if t.jadwal.end_time
                        else None
                    ),
                }

            frequency_data = None
            if t.frequency:
                frequency_data = {
                    "frequency": t.frequency.frequency,
                    "frequency_time": t.frequency.get_frequency_time_display(),
                }

            categories_data = [
                {
                    "trainingcategory": category.trainingcategory,
                    "nama_category": category.nama_category,
                }
                for category in t.kategori.all()
            ]

            result.append(
                {
                    "training": t.training,
                    "nama_latihan": t.nama_latihan,
                    "team_id": t.tim.team,
                    "team": {
                        "team": t.tim.team,
                        "nama_team": t.tim.nama_team,
                        "kategori_team": t.tim.kategori_team,
                        "coach": t.tim.coach.coach if t.tim.coach else None,
                        "logo_team": t.tim.logo_team.url if t.tim.logo_team else None,
                    },
                    "schedule": schedule_data,
                    "stadion": {
                        "stadion": t.lokasi.stadion,
                        "nama_stadion": t.lokasi.nama_stadion,
                        "lokasi": t.lokasi.lokasi,
                    },
                    "trainingcategory": categories_data,
                    "frequency_id": (
                        frequency_data["frequency"] if frequency_data else None
                    ),
                    "frequency": frequency_data,
                    "date": t.date.isoformat(),
                    "start_time": t.start_time.strftime("%H:%M"),
                    "end_time": t.end_time.strftime("%H:%M"),
                    "deskripsi": t.deskripsi,
                }
            )
        return result

    @staticmethod
    def get_by_team(team_id):
        trainings = training.objects.filter(tim=team_id).order_by("-date")
        print("get_by_team trainings ", trainings.count())
        result = []
        for t in trainings:
            print("get_by_team t ", t.jadwal)
            schedule_data = None
            if t.jadwal:
                schedule_data = {
                    "schedule": t.jadwal.schedule,
                    "tanggal": t.jadwal.tanggal,
                    "start_time": (
                        t.jadwal.start_time.strftime("%H:%M")
                        if t.jadwal.start_time
                        else None
                    ),
                    "end_time": (
                        t.jadwal.end_time.strftime("%H:%M")
                        if t.jadwal.end_time
                        else None
                    ),
                }

            frequency_data = None
            if t.frequency:
                frequency_data = {
                    "frequency": t.frequency.frequency,
                    "frequency_time": t.frequency.get_frequency_time_display(),
                }

            categories_data = [
                {
                    "trainingcategory": category.trainingcategory,
                    "nama_category": category.nama_category,
                }
                for category in t.kategori.all()
            ]

            result.append(
                {
                    "training": t.training,
                    "nama_latihan": t.nama_latihan,
                    "team_id": t.tim.team,
                    "team": {
                        "team": t.tim.team,
                        "nama_team": t.tim.nama_team,
                        "kategori_team": t.tim.kategori_team,
                        "coach": t.tim.coach.coach if t.tim.coach else None,
                        "logo_team": t.tim.logo_team.url if t.tim.logo_team else None,
                    },
                    "schedule": schedule_data,
                    "stadion": {
                        "stadion": t.lokasi.stadion,
                        "nama_stadion": t.lokasi.nama_stadion,
                        "lokasi": t.lokasi.lokasi,
                    },
                    "trainingcategory": categories_data,
                    "frequency_id": (
                        frequency_data["frequency"] if frequency_data else None
                    ),
                    "frequency": frequency_data,
                    "date": t.date.isoformat(),
                    "start_time": t.start_time.strftime("%H:%M"),
                    "end_time": t.end_time.strftime("%H:%M"),
                    "deskripsi": t.deskripsi,
                }
            )
        return result

    @staticmethod
    def get_all():
        trainings = training.objects.all().order_by("-date")
        result = []

        for t in trainings:
            schedule_data = None
            if t.jadwal:
                schedule_data = {
                    "schedule": t.jadwal.schedule,
                    "tanggal": t.jadwal.tanggal,
                    "start_time": (
                        t.jadwal.start_time.strftime("%H:%M")
                        if t.jadwal.start_time
                        else None
                    ),
                    "end_time": (
                        t.jadwal.end_time.strftime("%H:%M")
                        if t.jadwal.end_time
                        else None
                    ),
                }

            frequency_data = None
            if t.frequency:
                frequency_data = {
                    "frequency": t.frequency.frequency,
                    "frequency_time": t.frequency.get_frequency_time_display(),
                }

            categories_data = [
                {
                    "trainingcategory": category.trainingcategory,
                    "nama_category": category.nama_category,
                }
                for category in t.kategori.all()
            ]

            result.append(
                {
                    "training": t.training,
                    "nama_latihan": t.nama_latihan,
                    "team_id": t.tim.team,
                    "team": {
                        "team": t.tim.team,
                        "nama_team": t.tim.nama_team,
                        "kategori_team": t.tim.kategori_team,
                        "coach": t.tim.coach.coach if t.tim.coach else None,
                        "logo_team": t.tim.logo_team.url if t.tim.logo_team else None,
                    },
                    "schedule": schedule_data,
                    "stadion": {
                        "stadion": t.lokasi.stadion,
                        "nama_stadion": t.lokasi.nama_stadion,
                        "lokasi": t.lokasi.lokasi,
                    },
                    "trainingcategory": categories_data,
                    "frequency_id": (
                        frequency_data["frequency"] if frequency_data else None
                    ),
                    "frequency": frequency_data,
                    "date": t.date.isoformat(),
                    "start_time": t.start_time.strftime("%H:%M"),
                    "end_time": t.end_time.strftime("%H:%M"),
                    "deskripsi": t.deskripsi,
                }
            )
        return result

    @staticmethod
    def put(req):
        Training = get_object_or_404(training, training=req["training"])
        Team = (
            get_object_or_404(team, team=req["team"])
            if req.get("team")
            else Training.tim
        )
        Schedule = (
            get_object_or_404(schedule, schedule=req["schedule"])
            if req.get("schedule")
            else Training.jadwal
        )
        Stadion = (
            get_object_or_404(stadion, stadion=req["stadion"])
            if req.get("stadion")
            else Training.lokasi
        )
        Frequency = (
            get_object_or_404(frequency, frequency=req["frequency"])
            if req.get("frequency")
            else Training.frequency
        )

        try:
            start_time = (
                RepoTraining._normalize_time(req["start_time"])
                if req.get("start_time")
                else Training.start_time
            )
            end_time = (
                RepoTraining._normalize_time(req["end_time"])
                if req.get("end_time")
                else Training.end_time
            )
            date = (
                RepoTraining._normalize_date(req["date"])
                if req.get("date")
                else Training.date
            )
        except ValidationError as e:
            raise ValidationError(str(e))
        except ValueError as e:
            raise ValueError(str(e))

        Training.nama_latihan = req.get("nama_latihan", Training.nama_latihan)
        Training.tim = Team
        Training.jadwal = Schedule
        Training.lokasi = Stadion
        Training.frequency = Frequency
        Training.date = date
        Training.start_time = start_time
        Training.end_time = end_time
        Training.deskripsi = req.get("deskripsi", Training.deskripsi)
        Training.save()

        # Handle trainingcategory update (single or list)
        if "trainingcategory" in req:
            training_categories = req["trainingcategory"]
            if isinstance(training_categories, str):
                training_categories = [training_categories]
            Training.kategori.clear()  # Remove existing categories
            for category_id in training_categories:
                category = get_object_or_404(
                    trainingcategory, trainingcategory=category_id
                )
                Training.kategori.add(category)

        schedule_data = None
        if Training.jadwal:
            schedule_data = {
                "schedule": Training.jadwal.schedule,
                "tanggal": Training.jadwal.tanggal,
                "start_time": (
                    Training.jadwal.start_time.strftime("%H:%M")
                    if Training.jadwal.start_time
                    else None
                ),
                "end_time": (
                    Training.jadwal.end_time.strftime("%H:%M")
                    if Training.jadwal.end_time
                    else None
                ),
            }

        frequency_data = None
        if Training.frequency:
            frequency_data = {
                "frequency": Training.frequency.frequency,
                "frequency_time": Training.frequency.get_frequency_time_display(),
            }

        categories_data = [
            {
                "trainingcategory": category.trainingcategory,
                "nama_category": category.nama_category,
            }
            for category in Training.kategori.all()
        ]

        return {
            "training": Training.training,
            "nama_latihan": Training.nama_latihan,
            "team_id": Team.team,
            "team": {
                "team": Team.team,
                "nama_team": Team.nama_team,
                "kategori_team": Team.kategori_team,
                "coach": Team.coach.coach if Team.coach else None,
                "logo_team": Team.logo_team.url if Team.logo_team else None,
            },
            "schedule": schedule_data,
            "stadion": {
                "stadion": Stadion.stadion,
                "nama_stadion": Stadion.nama_stadion,
                "lokasi": Stadion.lokasi,
            },
            "trainingcategory": categories_data,
            "frequency_id": Frequency.frequency,
            "frequency": frequency_data,
            "date": Training.date.isoformat(),
            "start_time": Training.start_time.strftime("%H:%M"),
            "end_time": Training.end_time.strftime("%H:%M"),
            "deskripsi": Training.deskripsi,
        }

    @staticmethod
    def delete(req):
        Training = get_object_or_404(training, training=req["training"])
        Training.delete()
        return {"message": f"Training with id {req['training']} has been deleted."}
