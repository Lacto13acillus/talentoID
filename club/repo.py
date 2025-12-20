from club.models import club
from team.models import team
from player.models import player
from ProfilCoach.models import ProfilCoach
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from collections import defaultdict


class RepoClub:
    @staticmethod
    def get_all():
        clubs = club.objects.all()
        return [
            {
                "club": club_data.club,
                "club_name": club_data.club_name,
                "club_logo": club_data.club_logo.url if club_data.club_logo else None,
                "total_teams": team.objects.filter(club=club_data).count(),
            }
            for club_data in clubs
        ]

    @staticmethod
    def get(club_id):
        club_data = club.objects.get(club=club_id)
        return {
            "club": club_data.club,
            "club_name": club_data.club_name,
            "club_logo": club_data.club_logo.url if club_data.club_logo else None,
        }

    @staticmethod
    def post(req):
        # print(req)
        allowed_extensions = ["jpg", "jpeg", "png", "gif"]
        if "club_logo" not in req:
            raise ValidationError("club logo is required.")

        logo_team = req["club_logo"]
        file_extension = logo_team.name.split(".")[-1].lower()

        if file_extension not in allowed_extensions:
            raise ValidationError(
                "Invalid file format. Only JPEG, PNG, and GIF are allowed."
            )

        club_instance = club.objects.create(
            club=req["club"], club_name=req["club_name"], club_logo=req["club_logo"]
        )
        return {
            "club": club_instance.club,
            "club_name": club_instance.club_name,
            "club_logo": (
                club_instance.club_logo.url if club_instance.club_logo else None
            ),
        }

    @staticmethod
    def put(req):
        club_instance = get_object_or_404(club, club=req["club"])

        club_instance.club_name = req.get("club_name", club_instance.club_name)

        if "club_logo" in req and req["club_logo"] is not None:
            allowed_extensions = ["jpg", "jpeg", "png", "gif"]
            club_logo = req["club_logo"]

            if not hasattr(club_logo, "name"):
                raise ValidationError("Invalid file upload.")

            file_extension = club_logo.name.split(".")[-1].lower()
            if file_extension not in allowed_extensions:
                raise ValidationError(
                    "Invalid file format. Only JPEG, PNG, and GIF are allowed."
                )

            club_instance.club_logo = club_logo

        club_instance.save()

        return {
            "club": club_instance.club,
            "club_name": club_instance.club_name,
            "club_logo": (
                club_instance.club_logo.url if club_instance.club_logo else None
            ),
        }

    @staticmethod
    def delete(req):
        club_instance = get_object_or_404(club, club=req["club"])
        club_instance.delete()

        return {"message": f"Club with id {req['club']} has been deleted."}

    @staticmethod
    def get_club_info_by_player_id(player_id):
        try:
            # 1. Ambil team berdasarkan ID
            player_instance = player.objects.get(player=player_id)
            team_instance = team.objects.get(team=player_instance.tim_id)

            # 2. Dapatkan club dari team tersebut
            club = team_instance.club

            if not club:
                return {"error": "Team tidak terkait dengan club manapun."}

            # 3. Ambil semua team di club tersebut
            teams_in_club = team.objects.filter(club=club)
            if not teams_in_club.exists():
                return {"error": "Tidak ada team yang terkait dengan club ini."}
            # 5. Hitung jumlah player di semua team tersebut
            players = player.objects.filter(tim_id__in=teams_in_club)

            # Ambil semua coach yang ditugaskan di team-team tersebut
            coachs = ProfilCoach.objects.filter(
                coach__in=teams_in_club.values_list("coach", flat=True).distinct()
            )
            # Siapkan data tim
            # teams_data = list(teams_in_club.values('team', 'nama_team', 'kategori_team'))

            # Data pemain (contoh field: id, nama, team_id)
            players_data = list(
                players.values("player", "nama", "posisi", "tim_id")
            )  # sesuaikan nama field

            coachs_data = []
            for c in coachs:
                coachs_data.append(
                    {
                        "coach": c.coach,
                        "nama_coach": c.user.nama,
                        "tanggal_bergabung": c.tanggal_bergabung,
                        "tanggal_lahir": c.tanggal_lahir,
                        "kewarganegaraan": c.kewarganegaraan,
                        "tinggi_badan": c.tinggi_badan,
                        "berat_badan": c.berat_badan,
                        "foto_profil": c.foto_profil.url if c.foto_profil else None,
                    }
                )  # sesuaikan nama field

            # 3. Kelompokkan pemain berdasarkan tim_id
            players_by_team = defaultdict(list)
            for p in players:
                players_by_team[p.tim_id].append(
                    {
                        "player": p.player,
                        "nama": p.nama,
                        "posisi": p.posisi,
                        "kewarganegaraan": p.kewarganegaraan,
                        "nomor_punggung": p.nomor_punggung,
                        "tinggi_badan": p.tinggi_badan,
                        "berat_badan": p.berat_badan,
                        "tanggal_gabung": p.tanggal_gabung,
                        "kelamin": p.kelamin,
                        "dob": p.dob,
                        "verification_status": p.verification_status,
                        "foto_profil": p.foto_profil.url if p.foto_profil else None,
                    }
                )

            teams_data = []
            for t in teams_in_club:
                teams_data.append(
                    {
                        "team": t.team,
                        "nama_team": t.nama_team,
                        "kategori_team": t.kategori_team,
                        "logo_team": t.logo_team.url if t.logo_team else None,
                        "players": players_by_team[t.team],
                    }
                )

            return {
                "club": club.club,
                "club_name": club.club_name,
                "club_logo": club.club_logo.url if club.club_logo else None,
                "player_status": player_instance.verification_status,
                "total_teams": teams_in_club.count(),
                "total_players": players.count(),
                "total_coaches": coachs.count(),
                "teams": teams_data,
                "coachs": coachs_data,
            }

        except team.DoesNotExist:
            return {"error": "Team dengan ID tersebut tidak ditemukan."}
