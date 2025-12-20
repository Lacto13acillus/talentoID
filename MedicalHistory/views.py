# views/medical_history_views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .usecase import UsecaseMedicalHistory
from rest_framework import status as http_status
from django.core.exceptions import ValidationError

@api_view(["POST", "GET", "PUT", "DELETE"])
def medical_history_handler(request):
    try:
        if request.method == "POST":
            required_fields = ["player", "jenis_pemeriksaan"]
            if not all(field in request.POST for field in required_fields):
                return Response({
                    "code": 400,
                    "message": f"{', '.join(required_fields)} are required"
                }, status=http_status.HTTP_400_BAD_REQUEST)
            
            data = UsecaseMedicalHistory.post(request)
            return Response({
                "code": 200,
                "message": "Medical history created successfully",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "GET":
            medical_history_id = request.query_params.get("medicalhistory")
            player_id = request.query_params.get("player")  # Ubah ke "player" seperti attendance

            if medical_history_id:
                data = UsecaseMedicalHistory.get(medical_history_id)
                return Response({
                    "code": 200,
                    "message": "Medical history retrieved successfully",
                    "data": data
                }, status=http_status.HTTP_200_OK)
            elif player_id:
                data = UsecaseMedicalHistory.get_by_player(player_id)
                return Response({
                    "code": 200,
                    "message": "Medical histories by player retrieved successfully",
                    "data": data
                }, status=http_status.HTTP_200_OK)
            else:
                data = UsecaseMedicalHistory.get_all()
                return Response({
                    "code": 200,
                    "message": "All medical histories retrieved successfully",
                    "data": data
                }, status=http_status.HTTP_200_OK)

        elif request.method == "PUT":
            if "medicalhistory" not in request.POST:
                return Response({
                    "code": 400,
                    "message": "medicalhistory id is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseMedicalHistory.put(request)
            return Response({
                "code": 200,
                "message": "Medical history updated successfully",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "DELETE":
            if "medicalhistory" not in request.POST:
                return Response({
                    "code": 400,
                    "message": "medicalhistory id is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseMedicalHistory.delete(request)
            return Response({
                "code": 200,
                "message": "Medical history deleted successfully",
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