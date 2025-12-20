from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "Seeds all data (status, superadmin, products, etc.)"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Starting to seed all data..."))

        # Call the individual seeder commands for each app
        try:
            call_command("seed_superadmin")  # Seeder from user app
            self.stdout.write(self.style.SUCCESS("Superadmin seeded successfully."))

            call_command("seed_status")  # Seeder from status app
            self.stdout.write(self.style.SUCCESS("Status seeded successfully."))

            call_command("seed_metrics")  # Seeder from product app
            self.stdout.write(self.style.SUCCESS("Products seeded successfully."))

            # Add any other seeder commands here

            self.stdout.write(self.style.SUCCESS("All seeding completed successfully!"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error during seeding: {e}"))
