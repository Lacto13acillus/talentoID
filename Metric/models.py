from django.db import models
import MetricCategory.models as MetricCategory

# Create your models here.
class Metric(models.Model):
	metric = models.CharField(max_length=60, primary_key=True, unique=True)
	metric_category = models.ForeignKey(MetricCategory.MetricCategory, on_delete=models.CASCADE, related_name='metrics')
	name = models.CharField(max_length=255, unique=True)
	description = models.TextField(max_length=255, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
