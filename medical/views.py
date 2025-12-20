# views/medical_views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .usecase import UsecaseMedical
from rest_framework import status as http_status
from django.core.exceptions import ValidationError
import json

@api_view(["POST", "GET", "PUT", "DELETE"])
def medical_handler(request):
    try:
        if request.method == "POST":
            # Handle POST request
            required_fields = ["player", "medical_history", "session"]
            if not all(key in request.data for key in required_fields):
                return Response({
                    "code": 400,
                    "message": f"{', '.join(required_fields)} are required"
                }, status=http_status.HTTP_400_BAD_REQUEST)
            
            data = UsecaseMedical.post(request)
            return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "GET":
            medical_id = request.query_params.get("medical")
            if medical_id:
                # Jika ada medical_id, ambil data spesifik
                data = UsecaseMedical.get(medical_id)
            else:
                # Jika tidak ada medical_id, ambil semua data
                data = UsecaseMedical.get_all()
            
            return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "PUT":
            # Handle PUT request
            if "medical" not in request.data:
                return Response({
                    "code": 400,
                    "message": "medical id is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseMedical.put(request)
            return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "DELETE":
            # Handle DELETE request
            if "medical" not in request.data:
                return Response({
                    "code": 400,
                    "message": "medical id is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseMedical.delete(request)
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
