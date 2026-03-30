from django.shortcuts import get_object_or_404
from .models import team
from django.core.exceptions import ValidationError
from ProfilCoach.models import ProfilCoach
from player.models import player

from wilayah.models import Kabupaten


class RepoTeam:
    @staticmethod
    def post(req):
        allowed_extensions = ["jpg", "jpeg", "png", "gif"]

        if "logo_team" not in req:
            raise ValidationError("logo_team is required.")

        logo_team = req["logo_team"]
        file_extension = logo_team.name.split(".")[-1].lower()

        if file_extension not in allowed_extensions:
            raise ValidationError(
                "Invalid file format. Only JPEG, PNG, and GIF are allowed."
            )

        Coach = get_object_or_404(ProfilCoach, coach=req["coach"])
        # club_instance = get_object_or_404(club, club=req["club"])

        kabupaten_instance = None
        if req.get("kode_kabupaten"):
            kabupaten_instance = Kabupaten.objects.filter(
                kode=req["kode_kabupaten"]
            ).first()

            if not kabupaten_instance:
                raise ValidationError("Kode kabupaten tidak valid.")

        new_team = team.objects.create(
            team=req["team"],
            nama_team=req["nama_team"],
            coach=Coach,
            # club=club_instance,
            kabupaten=kabupaten_instance,
            kategori_team=req["kategori_team"],
            logo_team=req.get("logo_team", None),
        )

        return {
            "team": new_team.team,
            "nama_team": new_team.nama_team,
            "coach": new_team.coach.coach,
            # "club": new_team.club.club,
            "coach_name": new_team.coach.user.nama,
            # "club_name": new_team.club.club_name,
            "kategori_team": new_team.kategori_team,
            "logo_team": new_team.logo_team.url if new_team.logo_team else None,
            "kabupaten": new_team.kabupaten.nama if new_team.kabupaten else None,
            "provinsi": (
                new_team.kabupaten.provinsi.nama if new_team.kabupaten else None
            ),
        }

    @staticmethod
    def get(team_id):
        team_data = get_object_or_404(team, team=team_id)
        # Get team stats
        team_stats = RepoTeam.get_team_stats_by_team_id(team_id)

        return {
            "team": team_data.team,
            "nama_team": team_data.nama_team,
            "coach": team_data.coach.coach,
            # "club": team_data.club.club,
            "coach_name": team_data.coach.user.nama,
            # "club_name": team_data.club.club_name,
            "kategori_team": team_data.kategori_team,
            "logo_team": team_data.logo_team.url if team_data.logo_team else None,
            "stats": team_stats,  # Add team stats to the response
            "kabupaten": team_data.kabupaten.nama if team_data.kabupaten else None,
            "provinsi": (
                team_data.kabupaten.provinsi.nama if team_data.kabupaten else None
            ),
        }

    @staticmethod
    def get_all():
        # teams = team.objects.all().order_by("-created_at")
        teams = (
            team.objects.select_related(
                "kabupaten", "kabupaten__provinsi", "coach__user"
            )
            .all()
            .order_by("-created_at")
        )
        return [
            {
                "team": team_data.team,
                "nama_team": team_data.nama_team,
                "coach": team_data.coach.coach,
                # "club": team_data.club.club,
                "coach_name": team_data.coach.user.nama,
                # "club_name": team_data.club.club_name,
                "kategori_team": team_data.kategori_team,
                "logo_team": team_data.logo_team.url if team_data.logo_team else None,
                "stats": RepoTeam.get_team_stats_by_team_id(
                    team_data.team
                ),  # Add team stats to each team
                "kabupaten": team_data.kabupaten.kode if team_data.kabupaten else None,
                "kabupaten_name": (
                    team_data.kabupaten.nama if team_data.kabupaten else None
                ),
                "provinsi": (
                    team_data.kabupaten.provinsi.kode if team_data.kabupaten else None
                ),
                "provinsi_name": (
                    team_data.kabupaten.provinsi.nama if team_data.kabupaten else None
                ),
            }
            for team_data in teams
        ]

    @staticmethod
    def get_all_teams_by_coach_id(coach_id):
        teams = team.objects.filter(coach=coach_id)
        return [
            {
                "team": team_data.team,
                "nama_team": team_data.nama_team,
                "coach": team_data.coach.coach,
                # "club": team_data.club.club,
                "coach_name": team_data.coach.user.nama,
                # "club_name": team_data.club.club_name,
                "kategori_team": team_data.kategori_team,
                "logo_team": team_data.logo_team.url if team_data.logo_team else None,
                "stats": RepoTeam.get_team_stats_by_team_id(
                    team_data.team
                ),  # Add team stats to each team
                "kabupaten": team_data.kabupaten.nama if team_data.kabupaten else None,
                "provinsi": (
                    team_data.kabupaten.provinsi.nama if team_data.kabupaten else None
                ),
            }
            for team_data in teams
        ]

    @staticmethod
    def get_team_stats_by_team_id(team_id):
        # Dapatkan tim berdasarkan team_id
        team_data = get_object_or_404(team, team=team_id)

        # Hitung total pemain yang ada di tim ini
        total_players = player.objects.filter(tim=team_data).count()

        # Hitung total pelatih yang terkait dengan tim ini
        total_coaches = 1 if team_data.coach else 0

        return {"jumlah_player": total_players, "jumlah_coach": total_coaches}

    @staticmethod
    def put(req):
        print(req)
        allowed_extensions = ["jpg", "jpeg", "png", "gif"]

        team_instance = get_object_or_404(team, team=req["team"])

        team_instance.nama_team = req.get("nama_team", team_instance.nama_team)
        team_instance.kategori_team = req.get(
            "kategori_team", team_instance.kategori_team
        )

        if "kode_kabupaten" in req:
            if req["kode_kabupaten"]:
                kabupaten_instance = Kabupaten.objects.filter(
                    kode=req["kode_kabupaten"]
                ).first()

                if not kabupaten_instance:
                    raise ValidationError("Kode kabupaten tidak valid.")

                team_instance.kabupaten = kabupaten_instance
            else:
                team_instance.kabupaten = None

        if "coach" in req:
            team_instance.coach = get_object_or_404(ProfilCoach, pk=req["coach"])

        if "logo_team" in req and req["logo_team"] is not None:
            logo_team = req["logo_team"]

            if not hasattr(logo_team, "name"):
                raise ValidationError("Invalid file upload.")

            file_extension = logo_team.name.split(".")[-1].lower()
            if file_extension not in allowed_extensions:
                raise ValidationError(
                    "Invalid file format. Only JPEG, PNG, and GIF are allowed."
                )

            team_instance.logo_team = logo_team

        team_instance.save()

        return {
            "team": team_instance.team,
            "nama_team": team_instance.nama_team,
            "coach": team_instance.coach.coach if team_instance.coach else None,
            # "club": team_instance.club.club if team_instance.club else None,
            "coach_name": (
                team_instance.coach.user.nama if team_instance.coach else None
            ),
            # "club_name": team_instance.club.club_name if team_instance.club else None,
            "kategori_team": team_instance.kategori_team,
            "logo_team": (
                team_instance.logo_team.url if team_instance.logo_team else None
            ),
            "kabupaten": (
                team_instance.kabupaten.nama if team_instance.kabupaten else None
            ),
            "provinsi": (
                team_instance.kabupaten.provinsi.nama
                if team_instance.kabupaten
                else None
            ),
            # 'logo_team': req.get('logo_team', team_instance.logo_team.url if team_instance.logo_team else None)
        }

    @staticmethod
    def delete(req):
        Team = get_object_or_404(team, team=req["team"])
        Team.delete()
        return {"message": f"Team with id {req['team']} has been deleted."}
