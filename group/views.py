from rest_framework.decorators import api_view
from rest_framework.response import Response
from .usecase import UsecaseGroup
from rest_framework import status as http_status
from django.core.exceptions import ValidationError
import json

@api_view(["POST", "GET", "PUT", "DELETE"])
def group_handler(request):
    try:
        if request.method == "POST":
            # Handle POST request
            required_fields = ["nama_group", "team", "anggota"]
            if not all(key in request.data for key in required_fields):
                return Response({
                    "code": 400,
                    "message": f"{', '.join(required_fields)} are required"
                }, status=http_status.HTTP_400_BAD_REQUEST)
            
            data = UsecaseGroup.post(request)
            return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "GET":
            # Handle GET request
            try:
                group_id = request.query_params.get("id")
                if group_id:
                    # Existing single group GET
                    data = UsecaseGroup.get(group_id)
                    return Response({
                        "code": 200,
                        "message": "sukses",
                        "data": data
                    }, status=http_status.HTTP_200_OK)
                else:
                    # New GET ALL implementation
                    data = UsecaseGroup.get_all()
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
            if "id" not in request.data:
                return Response({
                    "code": 400,
                    "message": "id is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseGroup.put(request)
            return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "DELETE":
            # Handle DELETE request
            if "id" not in request.data:
                return Response({
                    "code": 400,
                    "message": "id is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseGroup.delete(request)
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
