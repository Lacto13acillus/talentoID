# views/analytics_views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .usecase import UsecaseAnalytics
from rest_framework import status as http_status
from django.core.exceptions import ValidationError
import json

@api_view(["POST", "GET", "PUT", "DELETE"])
def analytics_handler(request):
    try:
        if request.method == "POST":
            # Handle POST request
            required_fields = ["team", "kick_test", "tactical", "shoot_focus", "analyst"]
            if not all(key in request.data for key in required_fields):
                return Response({
                    "code": 400,
                    "message": f"{', '.join(required_fields)} are required"
                }, status=http_status.HTTP_400_BAD_REQUEST)
            
            data = UsecaseAnalytics.post(request)
            return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "GET":
            # Handle GET request
            try:
                analytics_id = request.query_params.get("analytics")
                if analytics_id:
                    # Existing single analytics GET
                    data = UsecaseAnalytics.get(analytics_id)
                    return Response({
                        "code": 200,
                        "message": "sukses",
                        "data": data
                    }, status=http_status.HTTP_200_OK)
                else:
                    # New GET ALL implementation
                    data = UsecaseAnalytics.get_all()
                    return Response({
                        "code": 200,
                        "message": "sukses",
                        "data": data
                    }, status=http_status.HTTP_200_OK)
            except Exception as e:
                return Response({
                    "code": 404,
                    "message": str(e)
                }, status=http_status.HTTP_404_NOT_FOUND)

        elif request.method == "PUT":
            # Handle PUT request
            if "analytics" not in request.data:
                return Response({
                    "code": 400,
                    "message": "analytics id is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseAnalytics.put(request)
            return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "DELETE":
            # Handle DELETE request
            if "analytics" not in request.data:
                return Response({
                    "code": 400,
                    "message": "analytics id is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseAnalytics.delete(request)
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
        return Response({
            "code": 500,
            "message": str(e)
        }, status=http_status.HTTP_500_INTERNAL_SERVER_ERROR)
