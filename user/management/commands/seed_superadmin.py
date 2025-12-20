from django.core.management.base import BaseCommand
from user.models import user  # sesuaikan dengan nama aplikasi kamu


class Command(BaseCommand):
    help = "Seed default superadmin user"

    def handle(self, *args, **kwargs):
        admin_data = {
            "id_user": "superadmin001",
            "nama": "Administrator",
            "email": "superadmin@champion.com",
            "password": "1sampai8X",  # Bisa diganti
            "role": "superadmin",  # bebas, sesuai ROLE_CHOICES
        }

        if user.objects.filter(id_user=admin_data["id_user"]).exists():
            self.stdout.write(self.style.WARNING("Admin user already exists."))
            return

        # Create superuser
        user.objects.create_superuser(
            id_user=admin_data["id_user"],
            nama=admin_data["nama"],
            email=admin_data["email"],
            password=admin_data["password"],
            role=admin_data["role"],
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )

        self.stdout.write(self.style.SUCCESS("Admin user created successfully!"))
