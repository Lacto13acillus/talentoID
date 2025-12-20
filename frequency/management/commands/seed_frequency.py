from django.core.management.base import BaseCommand
from frequency.models import frequency  # Adjust the import based on your app name


class Command(BaseCommand):
    help = "Seeds the frequency model with predefined values"

    def handle(self, *args, **kwargs):

        frequency.objects.all().delete()
        frequency.objects.all().delete()
        self.stdout.write(self.style.WARNING("Semua data frequency berhasil dihapus."))

        # Define the frequency data where name and value are the same
        frequencies = [
            "One Time",
            "Daily",
            "Weekly",
            "Monthly",
        ]

        for frequency_name in frequencies:
            # Create or get the frequency object to avoid duplicates
            frequency_obj, created = frequency.objects.get_or_create(
                frequency=frequency_name, defaults={"frequency_time": frequency_name}
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully created frequency: {frequency_name}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Frequency {frequency_name} already exists")
                )

        self.stdout.write(self.style.SUCCESS("Frequencies seeded successfully!"))
