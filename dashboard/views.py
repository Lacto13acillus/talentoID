from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status as http_status
from django.utils import timezone
from django.utils.timesince import timesince

from tournament.models import Tournament
from team.models import team as Team
from training.models import training as Training
from player.models import player as Player


@api_view(["GET"])
def activity_list_handler(request):
    try:
        team_id = request.query_params.get("team")

        print(f"Received request for activities with team_id: {team_id}")

        activities = []

        # Base Querysets
        teams = Team.objects.all()
        trainings = Training.objects.all()
        players = Player.objects.all()
        tournaments = Tournament.objects.all()

        # Filter by team if provided
        if team_id:
            teams = teams.filter(team=team_id)
            trainings = trainings.filter(tim=team_id)
            players = players.filter(tim=team_id)

            # Uncomment jika Tournament punya field team_id
            # tournaments = tournaments.filter(team_id=team_id)

        # Order & Limit
        teams = teams.order_by("-created_at")[:10]
        trainings = trainings.order_by("-created_at")[:10]
        players = players.order_by("-created_at")[:10]
        tournaments = tournaments.order_by("-created_at")[:10]

        # Teams
        for team in teams:
            activities.append(
                {
                    "type": "team",
                    "icon": "🆕",
                    "description": f'Team "{team.nama_team}" was created',
                    "created_at": team.created_at,
                }
            )

        # Trainings
        for training in trainings:
            activities.append(
                {
                    "type": "training",
                    "icon": "🏋️",
                    "description": f'Training "{training.nama_latihan}" was scheduled',
                    "created_at": training.created_at,
                }
            )

        # Players
        for player in players:
            activities.append(
                {
                    "type": "player",
                    "icon": "📝",
                    "description": f'New player registered: "{player.nama}"',
                    "created_at": player.created_at,
                }
            )

        # Tournaments
        for tournament in tournaments:
            activities.append(
                {
                    "type": "tournament",
                    "icon": "🏆",
                    "description": f'Tournament "{tournament.name}" was created',
                    "created_at": tournament.created_at,
                }
            )

        # Sort all activities
        activities.sort(
            key=lambda x: x["created_at"],
            reverse=True,
        )

        # Top 20 activities
        activities = activities[:20]

        data = [
            {
                "type": activity["type"],
                "icon": activity["icon"],
                "description": activity["description"],
                "timeAgo": timesince(
                    activity["created_at"],
                    timezone.now(),
                ),
            }
            for activity in activities
        ]

        return Response(
            {
                "code": 200,
                "message": "Activities retrieved successfully",
                "data": data,
            },
            status=http_status.HTTP_200_OK,
        )

    except Exception as e:
        return Response(
            {
                "code": 500,
                "message": f"Internal server error: {str(e)}",
            },
            status=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
