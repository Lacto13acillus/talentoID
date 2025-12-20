from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status as http_status
from django.core.exceptions import ValidationError
from .usecase import UsecaseResult
from .models import result
from training.models import training

@api_view(["POST", "GET", "PUT", "DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def result_handler(request):
    try:
        if request.method == "POST":
            required_fields = ["training", "attendance_summary", "footprint_summary", "overall_evaluation"]
            missing_fields = [field for field in required_fields if field not in request.data]
            if missing_fields:
                return Response({
                    "code": 400,
                    "message": f"{', '.join(missing_fields)} are required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseResult.post(request)
            return Response({
                "code": 201,
                "message": "Result created successfully",
                "data": data
            }, status=http_status.HTTP_201_CREATED)

        elif request.method == "GET":
            result_id = request.query_params.get("result")
            if result_id:
                data = UsecaseResult.get(result_id)
            else:
                data = UsecaseResult.get_all()

            return Response({
                "code": 200,
                "message": "Results retrieved successfully",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "PUT":
            required_fields = ["result", "training"]
            missing_fields = [field for field in required_fields if field not in request.data]
            if missing_fields:
                return Response({
                    "code": 400,
                    "message": f"{', '.join(missing_fields)} are required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseResult.put(request)
            return Response({
                "code": 200,
                "message": "Result updated successfully",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "DELETE":
            if "result" not in request.data:
                return Response({
                    "code": 400,
                    "message": "result id is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseResult.delete(request)
            return Response({
                "code": 200,
                "message": "Result deleted successfully",
                "data": data
            }, status=http_status.HTTP_200_OK)

    except ValidationError as e:
        return Response({
            "code": 400,
            "message": str(e)
        }, status=http_status.HTTP_400_BAD_REQUEST)
    except result.DoesNotExist:
        return Response({
            "code": 404,
            "message": "Result not found"
        }, status=http_status.HTTP_404_NOT_FOUND)
    except training.DoesNotExist:
        return Response({
            "code": 404,
            "message": "Training not found"
        }, status=http_status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            "code": 500,
            "message": f"Internal server error: {str(e)}"
        }, status=http_status.HTTP_500_INTERNAL_SERVER_ERROR)