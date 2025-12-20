from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status as http_status
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .usecase import UsecaseMetric
# Create your views here.

@api_view(["POST", "GET", "PUT", "DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def metric_handler(request):
    try:
        if request.method == "POST":
            if "metric_category" not in request.data or "name" not in request.data:
                return Response({
                    "code": 400,
                    "message": "metric_category and name are required."
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseMetric.post(request)
            return Response({
                "code": 200,
                "message": "Success creating metric.",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "GET":
            metric_id = request.query_params.get("metric")

            if metric_id:
                data = UsecaseMetric.get(metric_id)
                return Response({
                    "code": 200,
                    "message": "Success retrieving metric.",
                    "data": data
                }, status=http_status.HTTP_200_OK)
            else:
                data = UsecaseMetric.get_all()
                return Response({
                    "code": 200,
                    "message": "Success retrieving all metrics.",
                    "data": data
                }, status=http_status.HTTP_200_OK)

        elif request.method == "PUT":
            if "metric" not in request.data:
                return Response({
                    "code": 400,
                    "message": "Metric ID is required."
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseMetric.put(request)
            return Response({
                "code": 200,
                "message": "Success updating metric.",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "DELETE":
            if "metric" not in request.data:
                return Response({
                    "code": 400,
                    "message": "Metric ID is required."
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseMetric.delete(request)
            return Response({
                "code": 200,
                "message": "Success deleting metric.",
                "data": data
            }, status=http_status.HTTP_200_OK)

    except ValidationError as e:
        return Response({
            "code": 400,
            "message": str(e)
        }, status=http_status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        message = e.messages[0] if hasattr(e, 'messages') and e.messages else str(e)
        return Response({
            "code": 500,
            "message": message
        }, status=http_status.HTTP_500_INTERNAL_SERVER_ERROR)
