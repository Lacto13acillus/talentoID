from django.db import models

# Create your models here.
class MetricCategory(models.Model):
	metric_category = models.CharField(max_length=50,primary_key=True, unique=True)
	name = models.CharField(max_length=255, unique=True)
	description = models.TextField(max_length=255, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
