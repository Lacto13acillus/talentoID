from django.core.management.base import BaseCommand
from status.models import status  # Adjust the import based on your app name


class Command(BaseCommand):
    help = "Seeds the status model"

    def handle(self, *args, **kwargs):

        status.objects.all().delete()
        status.objects.all().delete()
        self.stdout.write(self.style.WARNING("Semua data Status berhasil dihapus."))

        # Define the status data where name and value are the same
        statuses = [
            "Preparing",
            "Ready",
            "Finished",
        ]

        for status_name in statuses:
            # Create or get the status object to avoid duplicates
            status_obj, created = status.objects.get_or_create(
                status=status_name, defaults={"match_status": status_name}
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully created status: {status_name}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Status {status_name} already exists")
                )

        self.stdout.write(self.style.SUCCESS("Status seeded successfully!"))
