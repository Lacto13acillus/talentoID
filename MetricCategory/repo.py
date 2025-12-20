from django.core.exceptions import ValidationError
from .models import MetricCategory
from django.shortcuts import get_object_or_404
from django.db import IntegrityError

class RepoMetricCategory:

    @staticmethod
    def get_all():
        categories = MetricCategory.objects.prefetch_related('metrics').all()
        return [
            {
                'metric_category': cat.metric_category,
                'name': cat.name,
                'description': cat.description,
                'created_at': cat.created_at,
                'updated_at': cat.updated_at,
                'metrics': [
                {
                    'metric': metric.metric,
                    'name': metric.name,
                    'description': metric.description,
                    'created_at': metric.created_at,
                    'updated_at': metric.updated_at
                } for metric in cat.metrics.all()
            ]
            } for cat in categories
        ]

    @staticmethod
    def get(metric_category_id):
        cat = MetricCategory.objects.get(metric_category=metric_category_id)
        return {
            'metric_category': cat.metric_category,
            'name': cat.name,
            'description': cat.description,
            'created_at': cat.created_at,
            'updated_at': cat.updated_at
        }

    @staticmethod
    def post(req):
        try:
            # Cek duplikasi berdasarkan 'name'
            if MetricCategory.objects.filter(name=req['name']).exists():
                raise ValidationError("Metric category with this name already exists.")

            cat = MetricCategory.objects.create(
                metric_category=req['metric_category'],
                name=req['name'],
                description=req.get('description', '')
            )
            return {
                "metric_category": cat.metric_category,
                "name": cat.name,
                "description": cat.description,
                "created_at": cat.created_at,
                "updated_at": cat.updated_at,
            }
        except ValidationError:
            raise
        except IntegrityError:
            raise ValidationError("Metric category already exists or invalid data.")
    @staticmethod
    def put(req):
        cat = get_object_or_404( MetricCategory, metric_category=req['metric_category'])
        cat.name = req['name']
        cat.description = req.get('description', '')
        cat.save()
        return {
            'metric_category': cat.metric_category,
            'name': cat.name,
            'description': cat.description,
            'created_at': cat.created_at,
            'updated_at': cat.updated_at
        }
    @staticmethod
    def delete(req):
        print(req)
        cat = get_object_or_404( MetricCategory, metric_category=req['metric_category'])
        cat.delete()

        return {'message': f"MetricCategory with id {req['metric_category']} has been deleted."}
