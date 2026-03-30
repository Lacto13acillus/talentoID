import uuid
from django.db import models
import team.models as team


class Tournament(models.Model):

    id_tournament = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )

    name = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    start_date = models.DateField()
    end_date = models.DateField()

    registration_open = models.DateField()
    registration_close = models.DateField()

    max_teams = models.IntegerField()

    location = models.CharField(max_length=255, blank=True)

    entry_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    status = models.CharField(
        max_length=20,
        choices=[
            ("draft", "Draft"),
            ("open", "Open"),
            ("closed", "Closed"),
            ("ongoing", "Ongoing"),
            ("finished", "Finished"),
        ],
        default="draft",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TournamentRegistration(models.Model):

    id_registration = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )

    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    team = models.ForeignKey(team.team, on_delete=models.CASCADE)

    external_id = models.CharField(max_length=100, null=True, blank=True)

    registration_date = models.DateTimeField(auto_now_add=True)
    paid_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    base_amount = models.IntegerField(null=True, blank=True)
    fee_amount = models.IntegerField(null=True, blank=True)
    tax_amount = models.IntegerField(null=True, blank=True)
    total_amount = models.IntegerField(null=True, blank=True)

    payment_channel = models.CharField(max_length=50, null=True, blank=True)
    payment_method = models.CharField(max_length=50, null=True, blank=True)
    invoice_id = models.CharField(max_length=255, null=True, blank=True)
    invoice_url = models.TextField(null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, blank=True)

    payment_status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("paid", "Paid"),
            ("expired", "Expired"),
            ("cancelled", "Cancelled"),
        ],
        default="pending",
    )

    class Meta:
        unique_together = ["tournament", "team"]
