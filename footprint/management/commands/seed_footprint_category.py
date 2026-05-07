from django.core.management.base import BaseCommand
from footprint.models import FootprintCategory


class Command(BaseCommand):
    help = "Seed FootprintCategory safely"

    def handle(self, *args, **kwargs):
        categories = ["passing", "heading", "dribbling"]

        for cat in categories:
            obj, created = FootprintCategory.objects.get_or_create(category=cat)

            self.stdout.write(
                self.style.SUCCESS(
                    f"{'Created' if created else 'Exists'}: {obj.category})"
                )
            )

        self.stdout.write(self.style.SUCCESS("Seeder completed safely."))
