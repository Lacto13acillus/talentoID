from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from .usecase import UsecaseFrequency
from rest_framework import status
from django.core.exceptions import ValidationError
from .models import frequency

@api_view(["POST", "GET", "PUT", "DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def frequency_handler(request):
    def validate_frequency_time(frequency_time, field_name):
        """Validate frequency_time against allowed choices."""
        if not frequency_time:
            return
        valid_choices = [choice[1] for choice in frequency.STATUS_CHOICES]
        if frequency_time not in valid_choices:
            raise ValidationError(
                f"Invalid {field_name}: {frequency_time}. Must be one of {', '.join(valid_choices)}."
            )

    try:
        if request.method == "POST":
            required_fields = ["frequency_time"]
            if not all(key in request.data for key in required_fields):
                return Response({
                    "code": 400,
                    "message": f"{', '.join(required_fields)} are required"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Validate frequency_time
            validate_frequency_time(request.data['frequency_time'], 'frequency_time')

            data = UsecaseFrequency.post(request)
            return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=status.HTTP_200_OK)

        elif request.method == "GET":
            frequency_id = request.query_params.get("frequency")
            if frequency_id:
                data = UsecaseFrequency.get(frequency_id)
                return Response({
                    "code": 200,
                    "message": "sukses",
                    "data": data
                }, status=status.HTTP_200_OK)
            else:
                data = UsecaseFrequency.get_all()
                return Response({
                    "code": 200,
                    "message": "sukses",
                    "data": data
                }, status=status.HTTP_200_OK)

        elif request.method == "PUT":
            if "frequency" not in request.data:
                return Response({
                    "code": 400,
                    "message": "frequency is required"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Validate frequency_time if provided
            if 'frequency_time' in request.data:
                validate_frequency_time(request.data['frequency_time'], 'frequency_time')

            data = UsecaseFrequency.put(request)
            return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=status.HTTP_200_OK)

        elif request.method == "DELETE":
            if "frequency" not in request.data:
                return Response({
                    "code": 400,
                    "message": "frequency is required"
                }, status=status.HTTP_400_BAD_REQUEST)

            data = UsecaseFrequency.delete(request)
            return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=status.HTTP_200_OK)

    except ValidationError as e:
        return Response({
            "code": 400,
            "message": str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            "code": 500,
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)