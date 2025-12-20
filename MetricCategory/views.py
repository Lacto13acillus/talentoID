from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status as http_status
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .usecase import UsecaseMetricCategory


@api_view(["POST", "GET", "PUT", "DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def metric_category_handler(request):
    try:
        if request.method == "POST":
            if "name" not in request.data:
                return Response({
                    "code": 400,
                    "message": "Name is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseMetricCategory.post(request)
            return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "GET":
            metric_category = request.query_params.get("metric_category")
            if metric_category:
                data = UsecaseMetricCategory.get(metric_category)
            else:
                data = UsecaseMetricCategory.get_all()

            return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "PUT":
            if "metric_category" not in request.data:
                return Response({
                    "code": 400,
                    "message": "metric_category is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseMetricCategory.put(request)
            return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "DELETE":
            if "metric_category" not in request.data:
                return Response({
                    "code": 400,
                    "message": "metric_category is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseMetricCategory.delete(request)
            return Response({
                "code": 200,
                "message": "sukses",
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
