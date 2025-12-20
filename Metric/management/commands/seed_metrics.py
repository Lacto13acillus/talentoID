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
            {"category": "Technical", "metric": "Passes", "name": "Passes"},
            {"category": "Technical", "metric": "Dribbles", "name": "Dribbles"},
            {
                "category": "Technical",
                "metric": "Shots on Target",
                "name": "Shots on Target",
            },
            {"category": "Technical", "metric": "Crosses", "name": "Crosses"},
            {"category": "Technical", "metric": "Ball Touches", "name": "Ball Touches"},
            {
                "category": "Technical",
                "metric": "Interceptions",
                "name": "Interceptions",
            },
            {"category": "Technical", "metric": "Clearances", "name": "Clearances"},
            # --- Psychological ---
            {
                "category": "Psychological",
                "metric": "Focus Rating",
                "name": "Focus Rating",
            },
            {
                "category": "Psychological",
                "metric": "Post Error Positive Action",
                "name": "Post Error Positive Action",
            },
            {"category": "Psychological", "metric": "Errors", "name": "Errors"},
            {
                "category": "Psychological",
                "metric": "Motivation Score",
                "name": "Motivation Score",
            },
            {
                "category": "Psychological",
                "metric": "Team Command",
                "name": "Team Command",
            },
            {
                "category": "Psychological",
                "metric": "Key Communication",
                "name": "Key Communication",
            },
            # --- Social ---
            {
                "category": "Social",
                "metric": "Combination Passes",
                "name": "Combination Passes",
            },
            {
                "category": "Social",
                "metric": "Cover Supports",
                "name": "Cover Supports",
            },
            {
                "category": "Social",
                "metric": "Verbal Comms",
                "name": "Verbal Communications",
            },
            {
                "category": "Social",
                "metric": "Nonverbal Gestures",
                "name": "Nonverbal Gestures",
            },
            {"category": "Social", "metric": "Total Fouls", "name": "Total Fouls"},
            {
                "category": "Social",
                "metric": "Peer Review Scores",
                "name": "Peer Review Scores",
            },
            # --- Performance ---
            {
                "category": "Performance",
                "metric": "Goals Scored",
                "name": "Goals Scored",
            },
            {"category": "Performance", "metric": "Assists", "name": "Assists"},
            {
                "category": "Performance",
                "metric": "Goals Conceded",
                "name": "Goals Conceded",
            },
            {"category": "Performance", "metric": "Fouls", "name": "Fouls"},
            {
                "category": "Performance",
                "metric": "Yellow Cards",
                "name": "Yellow Cards",
            },
            {"category": "Performance", "metric": "Red Cards", "name": "Red Cards"},
            {
                "category": "Performance",
                "metric": "Minutes Played",
                "name": "Minutes Played",
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
                    "description": item["name"],
                },
            )

            self.stdout.write(self.style.SUCCESS(f"Metric ensured: {normalized_key}"))

        self.stdout.write(self.style.SUCCESS("Metrics seeding completed!"))
