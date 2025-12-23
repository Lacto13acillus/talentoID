from django.core.management.base import BaseCommand
from MetricCategory.models import MetricCategory
from Metric.models import Metric
import re


def normalize_metric(value: str) -> str:
    """
    Convert metric string into safe primary key:
    - lowercase
    - spaces → underscores
    """
    value = value.lower().strip()
    value = re.sub(r"\s+", "_", value)
    return value


class Command(BaseCommand):
    help = "Seed metric categories and metrics"

    def handle(self, *args, **kwargs):

        MetricCategory.objects.all().delete()
        Metric.objects.all().delete()
        self.stdout.write(self.style.WARNING("Semua data Metrics berhasil dihapus."))

        metrics_data = [
            # --- Technical Metrics ---
            {
                "category": "Technical",
                "metric": "Passes",
                "name": "Passes",
                "description": "Number of successful passes made by the player.",
            },
            {
                "category": "Technical",
                "metric": "Dribbles",
                "name": "Dribbles",
                "description": "Number of successful dribbles or attempts to maneuver past an opponent.",
            },
            {
                "category": "Technical",
                "metric": "Shots on Target",
                "name": "Shots on Target",
                "description": "Shots taken that are on target (directed at the goal).",
            },
            {
                "category": "Technical",
                "metric": "Crosses",
                "name": "Crosses",
                "description": "Number of times the player delivers the ball into the penalty area from the sides.",
            },
            {
                "category": "Technical",
                "metric": "Ball Touches",
                "name": "Ball Touches",
                "description": "Number of times the player makes contact with the ball during the match.",
            },
            {
                "category": "Technical",
                "metric": "Interceptions",
                "name": "Interceptions",
                "description": "Number of times the player intercepts the ball from the opposing team.",
            },
            {
                "category": "Technical",
                "metric": "Clearances",
                "name": "Clearances",
                "description": "Number of times the player clears the ball from a dangerous area, typically the defensive zone.",
            },
            # --- Psychological Metrics ---
            {
                "category": "Psychological",
                "metric": "Focus Rating",
                "name": "Focus Rating",
                "description": "A measure of the player's mental focus during the game, indicating concentration levels.",
            },
            {
                "category": "Psychological",
                "metric": "Post Error Positive Action",
                "name": "Post Error Positive Action",
                "description": "Number of positive actions the player takes immediately after making an error, showing resilience and mental strength.",
            },
            {
                "category": "Psychological",
                "metric": "Errors",
                "name": "Errors",
                "description": "Number of mistakes made by the player, such as mispasses, fouls, or misjudged tackles.",
            },
            {
                "category": "Psychological",
                "metric": "Motivation Score",
                "name": "Motivation Score",
                "description": "A score indicating the player's motivation levels during the game.",
            },
            {
                "category": "Psychological",
                "metric": "Team Command",
                "name": "Team Command",
                "description": "A metric measuring how effectively the player leads or commands the team on the field.",
            },
            {
                "category": "Psychological",
                "metric": "Key Communication",
                "name": "Key Communication",
                "description": "The number and quality of significant verbal or non-verbal communications made by the player during the game.",
            },
            # --- Social Metrics ---
            {
                "category": "Social",
                "metric": "Combination Passes",
                "name": "Combination Passes",
                "description": "Number of successful passes made in combination with a teammate, such as a one-two or quick passing exchange.",
            },
            {
                "category": "Social",
                "metric": "Cover Supports",
                "name": "Cover Supports",
                "description": "The number of times the player provides cover or defensive support for a teammate.",
            },
            {
                "category": "Social",
                "metric": "Verbal Comms",
                "name": "Verbal Communications",
                "description": "Number of verbal communications (shouts, instructions, calls) made by the player.",
            },
            {
                "category": "Social",
                "metric": "Nonverbal Gestures",
                "name": "Nonverbal Gestures",
                "description": "Non-verbal communication signals such as hand gestures, eye contact, or body language that support team play.",
            },
            {
                "category": "Social",
                "metric": "Total Fouls",
                "name": "Total Fouls",
                "description": "Total number of fouls committed by the player during the match.",
            },
            {
                "category": "Social",
                "metric": "Peer Review Scores",
                "name": "Peer Review Scores",
                "description": "Ratings given by teammates or coaches on the player's performance, attitude, and team collaboration.",
            },
            # --- Performance Metrics ---
            {
                "category": "Performance",
                "metric": "Goals Scored",
                "name": "Goals Scored",
                "description": "The total number of goals scored by the player.",
            },
            {
                "category": "Performance",
                "metric": "Assists",
                "name": "Assists",
                "description": "The number of assists provided by the player, contributing to a goal scored.",
            },
            {
                "category": "Performance",
                "metric": "Goals Conceded",
                "name": "Goals Conceded",
                "description": "The number of goals the team has conceded when the player is on the field.",
            },
            {
                "category": "Performance",
                "metric": "Fouls",
                "name": "Fouls",
                "description": "The total number of fouls committed by the player.",
            },
            {
                "category": "Performance",
                "metric": "Yellow Cards",
                "name": "Yellow Cards",
                "description": "The number of yellow cards received by the player as a cautionary punishment.",
            },
            {
                "category": "Performance",
                "metric": "Red Cards",
                "name": "Red Cards",
                "description": "The number of red cards received by the player, resulting in ejection from the game.",
            },
            {
                "category": "Performance",
                "metric": "Minutes Played",
                "name": "Minutes Played",
                "description": "Total minutes the player has been on the field during the game.",
            },
        ]

        # categories list
        categories = [
            "Technical",
            "Psychological",
            "Social",
            "Performance",
        ]

        # --- Seed categories ---
        for cat in categories:
            MetricCategory.objects.get_or_create(
                metric_category=cat, defaults={"name": cat}
            )
            self.stdout.write(self.style.SUCCESS(f"Category ensured: {cat}"))

        # --- Seed metrics with normalized PK ---
        for item in metrics_data:
            category = MetricCategory.objects.get(metric_category=item["category"])
            normalized_key = normalize_metric(item["metric"])  # convert HERE

            Metric.objects.update_or_create(
                metric=normalized_key,
                defaults={
                    "metric_category": category,
                    "name": item["name"],
                    "description": item["description"],
                },
            )

            self.stdout.write(self.style.SUCCESS(f"Metric ensured: {normalized_key}"))

        self.stdout.write(self.style.SUCCESS("Metrics seeding completed!"))
