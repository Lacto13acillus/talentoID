from rest_framework.decorators import api_view
from rest_framework.response import Response
from .usecase import UsecaseTraining
from .models import training
from rest_framework import status as http_status
from django.utils.dateparse import parse_date
from django.core.exceptions import ValidationError
import re


@api_view(["POST", "GET", "PUT", "DELETE"])
def training_handler(request):
    def validate_time_format(time_str, field_name):
        """Validate time format as HH:MM or HH:MM:SS."""
        if not time_str:
            return
        pattern = r"^(?:[0-1][0-9]|2[0-3]):[0-5][0-9](?::[0-5][0-9])?$"
        if not re.match(pattern, time_str):
            raise ValidationError(
                f"Invalid {field_name} format. Use HH:MM or HH:MM:SS."
            )

    def validate_trainingcategory(trainingcategory):
        """Validate trainingcategory as a single string or non-empty list."""
        if not trainingcategory:
            raise ValidationError("trainingcategory is required")
        if isinstance(trainingcategory, list):
            if not trainingcategory:
                raise ValidationError("trainingcategory list cannot be empty")
            for category in trainingcategory:
                if not isinstance(category, str):
                    raise ValidationError("All trainingcategory IDs must be strings")
        elif not isinstance(trainingcategory, str):
            raise ValidationError(
                "trainingcategory must be a string or a list of strings"
            )

    try:
        if request.method == "POST":
            required_fields = [
                "nama_latihan",
                "team",
                "stadion",
                "trainingcategory",
                "start_time",
                "end_time",
                "deskripsi",
                "date",
            ]
            missing_fields = [
                field for field in required_fields if field not in request.data
            ]
            if missing_fields:
                return Response(
                    {
                        "code": 400,
                        "message": f"Missing required fields: {', '.join(missing_fields)}",
                    },
                    status=http_status.HTTP_400_BAD_REQUEST,
                )

            # Validate trainingcategory
            validate_trainingcategory(request.data["trainingcategory"])

            # Validate time fields
            validate_time_format(request.data["start_time"], "start_time")
            validate_time_format(request.data["end_time"], "end_time")

            # Validate date format
            if request.data["date"] == "0000-00-00":
                return Response(
                    {
                        "code": 400,
                        "message": "Invalid date: '0000-00-00' is not a valid date",
                    },
                    status=http_status.HTTP_400_BAD_REQUEST,
                )
            if not parse_date(request.data["date"]):
                return Response(
                    {"code": 400, "message": "Invalid date format. Use YYYY-MM-DD"},
                    status=http_status.HTTP_400_BAD_REQUEST,
                )

            data = UsecaseTraining.post(request)
            return Response(
                {"code": 201, "message": "Success", "data": data},
                status=http_status.HTTP_201_CREATED,
            )

        elif request.method == "GET":
            training_id = request.query_params.get("training")
            coach_id = request.query_params.get("coach")
            player_id = request.query_params.get("player")
            team_id = request.query_params.get("team")

            if training_id:
                data = UsecaseTraining.get(training_id)
                return Response(
                    {"code": 200, "message": "Success", "data": data},
                    status=http_status.HTTP_200_OK,
                )
            elif coach_id:
                data = UsecaseTraining.get_by_coach(coach_id)
                return Response(
                    {"code": 200, "message": "Success", "data": data},
                    status=http_status.HTTP_200_OK,
                )
            elif player_id:
                data = UsecaseTraining.get_by_player(player_id)
                return Response(
                    {"code": 200, "message": "Success", "data": data},
                    status=http_status.HTTP_200_OK,
                )
            elif team_id:
                data = UsecaseTraining.get_by_team(team_id)
                return Response(
                    {"code": 200, "message": "Success", "data": data},
                    status=http_status.HTTP_200_OK,
                )
            else:
                data = UsecaseTraining.get_all()
                return Response(
                    {"code": 200, "message": "Success", "data": data},
                    status=http_status.HTTP_200_OK,
                )

        elif request.method == "PUT":
            if "training" not in request.data:
                return Response(
                    {"code": 400, "message": "training is required"},
                    status=http_status.HTTP_400_BAD_REQUEST,
                )

            # Validate trainingcategory if provided
            if "trainingcategory" in request.data:
                validate_trainingcategory(request.data["trainingcategory"])

            # Validate time fields if provided
            if "start_time" in request.data:
                validate_time_format(request.data["start_time"], "start_time")
            if "end_time" in request.data:
                validate_time_format(request.data["end_time"], "end_time")

            # Validate date format if provided
            if "date" in request.data and request.data["date"]:
                if request.data["date"] == "0000-00-00":
                    return Response(
                        {
                            "code": 400,
                            "message": "Invalid date: '0000-00-00' is not a valid date",
                        },
                        status=http_status.HTTP_400_BAD_REQUEST,
                    )
                if not parse_date(request.data["date"]):
                    return Response(
                        {"code": 400, "message": "Invalid date format. Use YYYY-MM-DD"},
                        status=http_status.HTTP_400_BAD_REQUEST,
                    )

            data = UsecaseTraining.put(request)
            return Response(
                {"code": 200, "message": "Success", "data": data},
                status=http_status.HTTP_200_OK,
            )

        elif request.method == "DELETE":
            if "training" not in request.data:
                return Response(
                    {"code": 400, "message": "training is required"},
                    status=http_status.HTTP_400_BAD_REQUEST,
                )

            data = UsecaseTraining.delete(request)
            return Response(
                {"code": 200, "message": "Success", "data": data},
                status=http_status.HTTP_200_OK,
            )

    except ValidationError as ve:
        return Response(
            {"code": 400, "message": str(ve)}, status=http_status.HTTP_400_BAD_REQUEST
        )
    except training.DoesNotExist:
        return Response(
            {"code": 404, "message": "Training not found"},
            status=http_status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        return Response(
            {"code": 500, "message": f"Internal server error: {str(e)}"},
            status=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
