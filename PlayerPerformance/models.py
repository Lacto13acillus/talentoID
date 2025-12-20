from django.db import models
import Metric.models as Metric
import pertandingan.models as pertandingan
import training.models as training
import player.models as player
import uuid


# Create your models here.
class PlayerPerformance(models.Model):
	player_performance = models.UUIDField(max_length=60, primary_key=True, default=uuid.uuid4, editable=False)
	player = models.ForeignKey(player.player, on_delete=models.CASCADE)
	metric = models.ForeignKey(Metric.Metric, on_delete=models.CASCADE)
	value = models.DecimalField(max_digits=6, decimal_places=2)

	# Salah satu dari ini harus diisi
	match = models.ForeignKey(pertandingan.pertandingan, on_delete=models.CASCADE, null=True, blank=True)
	training = models.ForeignKey(training.training, on_delete=models.CASCADE, null=True, blank=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def clean(self):
		from django.core.exceptions import ValidationError
		if not self.match and not self.training:
			raise ValidationError("Either match or training must be provided.")
		if self.match and self.training:
			raise ValidationError("Only one of match or training can be provided.")


	def __str__(self):
		return f"{self.player} - {self.metric} - {self.value}"
