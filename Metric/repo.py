from django.shortcuts import get_object_or_404
from .models import Metric
from django.core.exceptions import ValidationError
from MetricCategory.models import MetricCategory
from django.db import IntegrityError

class RepoMetric:
	@staticmethod
	def post(req):
		category_instance = get_object_or_404(MetricCategory, metric_category=req['metric_category'])
		if Metric.objects.filter(metric_category=category_instance, name=req['name']).exists():
			raise ValidationError("Metric with this name already exists in this category.")

		try:
			metric = Metric.objects.create(
				metric=req['metric'],
				metric_category=category_instance,
				name=req['name'],
				description=req.get('description', '')
			)
			return {
				"metric": metric.metric,
				"metric_category": {
					'metric_category': category_instance.metric_category,
					'name': category_instance.name,
					'description': category_instance.description
            	},
				"name": metric.name,
				"description": metric.description,
				"created_at": metric.created_at,
				"updated_at": metric.updated_at,
			}
		except ValidationError:
			raise
		except IntegrityError:
			raise ValidationError("Metric already exists or invalid data.")


	@staticmethod
	def get_all():
		metrics = Metric.objects.all().order_by('-created_at')
		return [
			{
				"metric": metric.metric,
				"metric_category": metric.metric_category.metric_category,
				"metric_category_name": metric.metric_category.name,
				"name": metric.name,
				"description": metric.description,
				"created_at": metric.created_at,
				"updated_at": metric.updated_at,
			} for metric in metrics
		]

	@staticmethod
	def get(metric_id):
		metric = Metric.objects.get(metric=metric_id)
		return {
			"metric": metric.metric,
			"metric_category": metric.metric_category.metric_category,
			"metric_category_name": metric.metric_category.name,
			"name": metric.name,
			"description": metric.description,
			"created_at": metric.created_at,
			"updated_at": metric.updated_at,
		}

	@staticmethod
	def put(req):
		metric = get_object_or_404(Metric, metric=req['metric'])
		if 'name' in req and req['name'] != metric.name:
			if Metric.objects.filter(metric_category=metric.metric_category, name=req['name']).exists():
				raise ValidationError("Metric with this name already exists in this category.")
			metric.name = req['name']
		if 'description' in req:
			metric.description = req['description']
		if 'category_id' in req and req['category_id'] != metric.metric_category.id:
			new_category = MetricCategory.objects.get(id=req['category_id'])
			metric.metric_category = new_category
		metric.save()
		return {
			'metric': metric.metric,
			'metric_category': {
				'metric_category': metric.metric_category.metric_category,
				'name': metric.metric_category.name,
				'description': metric.metric_category.description
			},
			'name': metric.name,
			'description': metric.description,
			'created_at': metric.created_at,
			'updated_at': metric.updated_at,
		}

	@staticmethod
	def delete(metric):
		metric_instance = get_object_or_404(Metric, metric=metric)
		metric_instance.delete()
		return {"message": "Metric deleted successfully."}
