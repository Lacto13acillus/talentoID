import uuid
from django.db import models
from footprint.models import footprint as FootprintModel


class TotalResult(models.Model):
    """Model untuk tabel total_result di database Football_analysis."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    total_passing = models.IntegerField()
    passing_sukses = models.IntegerField()
    passing_gagal = models.IntegerField()
    akurasi_passing = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    parent_id = models.CharField(max_length=36, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    footprint = models.ForeignKey(
        FootprintModel,
        on_delete=models.SET_NULL,
        db_column='footprint',
        to_field='footprint',
        null=True,
        blank=True,
        related_name='analysis_total_results',
    )

    class Meta:
        db_table = 'total_result'
        managed = False

    def __str__(self):
        return f'<TotalResult {self.id} status={self.status}>'

    @staticmethod
    def calculate_accuracy(total_passing, passing_sukses):
        if total_passing and total_passing > 0:
            pct = round((passing_sukses / total_passing) * 100, 2)
            return f"{pct}%"
        return "0%"

    def to_dict(self):
        return {
            'id': str(self.id),
            'total_passing': self.total_passing,
            'passing_sukses': self.passing_sukses,
            'passing_gagal': self.passing_gagal,
            'akurasi_passing': self.akurasi_passing,
            'status': self.status,
            'parent_id': str(self.parent_id) if self.parent_id else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'footprint': self.footprint_id,
        }


class PlayerResult(models.Model):
    """Model untuk tabel player_result di database Football_analysis."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    total_result = models.ForeignKey(
        TotalResult,
        on_delete=models.SET_NULL,
        db_column='total_result_id',
        null=True,
        blank=True,
        related_name='player_results',
    )
    player = models.CharField(max_length=100, blank=True, null=True)
    total_passing = models.IntegerField(blank=True, null=True)
    passing_sukses = models.IntegerField(blank=True, null=True)
    passing_gagal = models.IntegerField(blank=True, null=True)
    akurasi_passing = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    parent_id = models.CharField(max_length=50, blank=True, null=True)
    footprint = models.ForeignKey(
        FootprintModel,
        on_delete=models.SET_NULL,
        db_column='footprint',
        to_field='footprint',
        null=True,
        blank=True,
        related_name='analysis_player_results',
    )

    class Meta:
        db_table = 'player_result'
        managed = False

    def __str__(self):
        return f'<PlayerResult {self.id} player={self.player}>'

    @staticmethod
    def calculate_accuracy(total_passing, passing_sukses):
        if total_passing and total_passing > 0:
            pct = round((passing_sukses / total_passing) * 100, 2)
            return f"{pct}%"
        return "0%"

    def to_dict(self):
        return {
            'id': str(self.id),
            'total_result_id': str(self.total_result_id) if self.total_result_id else None,
            'player': self.player,
            'total_passing': self.total_passing,
            'passing_sukses': self.passing_sukses,
            'passing_gagal': self.passing_gagal,
            'akurasi_passing': self.akurasi_passing,
            'status': self.status,
            'parent_id': str(self.parent_id) if self.parent_id else None,
            'footprint': self.footprint_id,
        }
