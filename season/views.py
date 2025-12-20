from rest_framework.decorators import api_view
from rest_framework.response import Response
from .usecase import UsecaseSeason
from rest_framework import status as http_status
from django.core.exceptions import ValidationError

@api_view(["POST", "GET", "PUT", "DELETE"])
def season_handler(request):
    try:
        if request.method == "POST":
            required_fields = ["nama_season"]
            if not all(key in request.data for key in required_fields):
                return Response({
                    "code": 400,
                    "message": f"{', '.join(required_fields)} are required"
                }, status=http_status.HTTP_400_BAD_REQUEST)
            
            data = UsecaseSeason.post(request)
            return Response({
                "code": 200,
                "message": "Season created successfully",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "GET":
            season_id = request.query_params.get("season")

            if season_id:
                data = UsecaseSeason.get(season_id)
                return Response({
                    "code": 200,
                    "message": "Season retrieved successfully",
                    "data": data
                }, status=http_status.HTTP_200_OK)
            else:
                data = UsecaseSeason.get_all()
                return Response({
                    "code": 200,
                    "message": "All seasons retrieved successfully",
                    "data": data
                }, status=http_status.HTTP_200_OK)

        elif request.method == "PUT":
            required_fields = ["season"]
            if not all(key in request.data for key in required_fields):
                return Response({
                    "code": 400,
                    "message": f"{', '.join(required_fields)} are required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseSeason.put(request)
            return Response({
                "code": 200,
                "message": "Season updated successfully",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "DELETE":
            if "season" not in request.data:
                return Response({
                    "code": 400,
                    "message": "season id is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseSeason.delete(request)
            return Response({
                "code": 200,
                "message": "Season deleted successfully",
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
