from django.db import models
import training.models as training

class result(models.Model):
    result = models.CharField(max_length=60, primary_key=True, unique=True)
    training = models.ForeignKey(training.training, on_delete=models.CASCADE)
    attendance_summary = models.TextField(max_length=200)
    footprint_summary = models.TextField(max_length=200)
    overall_evaluation = models.TextField(max_length=200)

