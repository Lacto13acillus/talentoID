from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from .usecase import UsecaseTeamReport
from rest_framework import status as http_status
from django.core.exceptions import ValidationError
import json

@api_view(["POST", "GET", "PUT", "DELETE"])
@authentication_classes([JWTAuthentication])  # Tambahkan autentikasi JWT
@permission_classes([IsAuthenticated])       # Hanya user yang terautentikasi yang bisa mengakses
def team_report_handler(request):
    try:
        if request.method == "POST":
            # Handle POST request
            required_fields = ["team", "schedule", "hasil_pertandingan", "catatan"]
            if not all(key in request.data for key in required_fields):
                return Response({
                    "code": 400,
                    "message": f"{', '.join(required_fields)} are required"
                }, status=http_status.HTTP_400_BAD_REQUEST)
            
            data = UsecaseTeamReport.post(request)
            return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "GET":
            team_report_id = request.query_params.get("teamreport")
            team_id = request.query_params.get("team")
            
            if team_report_id:
                data = UsecaseTeamReport.get(team_report_id)
            elif team_id:
                data = UsecaseTeamReport.get_all_team_reports_by_team_id(team_id)
            else:
                data = UsecaseTeamReport.get_all()
            
            return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "PUT":
            # Handle PUT request
            if "teamreport" not in request.data:
                return Response({
                    "code": 400,
                    "message": "teamreport id is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseTeamReport.put(request)
            return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "DELETE":
            # Handle DELETE request
            if "teamreport" not in request.data:
                return Response({
                    "code": 400,
                    "message": "teamreport id is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseTeamReport.delete(request)
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
