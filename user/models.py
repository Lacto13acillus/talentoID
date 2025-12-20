from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Group,
    Permission,
)
from django.db import models
from django.core.validators import FileExtensionValidator

# from team.models import team


class UserManager(BaseUserManager):
    def create_user(self, id_user, nama, email, password=None, **extra_fields):
        if not id_user:
            raise ValueError("The id_user must be set")
        if not email:
            raise ValueError("The email must be set")

        email = self.normalize_email(email)
        user = self.model(id_user=id_user, nama=nama, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id_user, nama, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(id_user, nama, email, password, **extra_fields)


class user(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ("superadmin", "Superadmin"),
        ("admin", "admin"),
        ("coach", "Coach"),
        ("coach", "Coach"),
    ]

    id_user = models.CharField(max_length=60, primary_key=True, unique=True, default="")
    nama = models.CharField(max_length=60)
    email = models.EmailField(max_length=200, unique=True)
    nomor_telepon = models.CharField(max_length=25, null=True, blank=True)
    password = models.CharField(max_length=100, default="")
    foto_profil = models.ImageField(
        upload_to="user/",  # Direktori penyimpanan gambar
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "gif"])
        ],
        blank=True,
        default="",
    )
    role = models.CharField(
        max_length=10,  # Panjang maksimal untuk role
        choices=ROLE_CHOICES,  # Pilihan role
        default="player",  # Role default
    )
    is_staff = models.BooleanField(default=False)  # Diperlukan untuk admin Django
    is_active = models.BooleanField(default=True)  # Diperlukan untuk autentikasi

    # 🔑 Relasi ke team (HANYA untuk admin)
    team = models.ForeignKey(
        "team.team",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="admins",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Tambahkan related_name yang unik untuk groups dan user_permissions
    groups = models.ManyToManyField(
        Group,
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        related_name="user_groups",  # Nama unik untuk related_name
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="user_user_permissions",  # Nama unik untuk related_name
        related_query_name="user",
    )

    objects = UserManager()

    USERNAME_FIELD = "id_user"  # Field yang digunakan untuk login
    REQUIRED_FIELDS = ["nama", "email"]  # Field yang diperlukan saat membuat user

    def __str__(self):
        return self.nama
