from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status as http_status
from django.core.exceptions import ValidationError
from .usecase import UsecaseFootprint
from .models import footprint
from training.models import training
import uuid

@api_view(["POST", "GET", "PUT", "DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def footprint_handler(request):
    try:
        if request.method == "POST":
            required_fields = ["training", "media"]
            missing_fields = [field for field in required_fields if field not in request.POST and field not in request.FILES]
            if missing_fields:
                return Response({
                    "code": 400,
                    "message": f"{', '.join(missing_fields)} are required"
                }, status=http_status.HTTP_400_BAD_REQUEST)
            training_id = request.data.get('training')
            if not training_id:
                 raise ValidationError("training ID is required.")
            media_files = request.FILES.getlist('media')
            for media in media_files:
                 req = {
					'footprint': str(uuid.uuid4()),
					'training': training_id,
					'media': media
				}
                 UsecaseFootprint.post(req)  # Usecase call per media
            return Response({
                "code": 201,
                "message": "Footprint created successfully"
            }, status=http_status.HTTP_201_CREATED)

        elif request.method == "GET":
            training_id = request.query_params.get("training")
            if training_id:
                data = UsecaseFootprint.get(training_id)
            else:
                data = UsecaseFootprint.get_all()

            return Response({
                "code": 200,
                "message": "Footprints retrieved successfully",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "PUT":
            required_fields = ["footprint", "training"]
            if not all(key in request.data for key in required_fields):
                return Response({
                    "code": 400,
                    "message": f"{', '.join(required_fields)} are required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseFootprint.put(request)
            return Response({
                "code": 200,
                "message": "Footprint updated successfully",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "DELETE":
            if "footprint" not in request.data:
                return Response({
                    "code": 400,
                    "message": "footprint id is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseFootprint.delete(request)
            return Response({
                "code": 200,
                "message": "Footprint deleted successfully",
                "data": data
            }, status=http_status.HTTP_200_OK)

    except ValidationError as e:
        return Response({
            "code": 400,
            "message": str(e)
        }, status=http_status.HTTP_400_BAD_REQUEST)
    except footprint.DoesNotExist:
        return Response({
            "code": 404,
            "message": "Footprint not found"
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
