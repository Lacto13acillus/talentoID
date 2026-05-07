from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status as http_status
from django.core.exceptions import ValidationError
from .usecase import UsecaseFootprint
from .models import footprint
from training.models import training
import uuid
from .models import FootprintCategory


def parse_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() == "true"
    return None


@api_view(["POST", "GET", "PUT", "DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def footprint_handler(request):
    try:
        print(
            f"Received {request.method} request with data: {request.data} and files: {request.FILES}"
        )
        if request.method == "POST":
            training_id = request.data.get("training")

            if not training_id:
                return Response(
                    {"code": 400, "message": "training is required"}, status=400
                )

            # Extract categories from indexed fields
            categories = []
            i = 0
            while True:
                category = request.data.get(f"category[{i}]")
                if category is None:
                    break
                categories.append(category)
                i += 1

            # extract hasJerseyNumber
            hasJerseyNumbers = []
            i = 0
            while True:
                value = request.data.get(f"hasJerseyNumber[{i}]")
                if value is None:
                    break

                hasJerseyNumbers.append(parse_bool(value))  # 🔥 convert di sini
                i += 1

            # Extract media files from indexed fields
            media_files = []
            i = 0
            while True:
                media_file = request.FILES.get(f"media_{i}")
                if media_file is None:
                    break
                media_files.append(media_file)
                i += 1

            # Validasi jumlah
            if len(media_files) != len(categories):
                return Response(
                    {
                        "code": 400,
                        "message": f"Number of media ({len(media_files)}) must match number of categories ({len(categories)})",
                    },
                    status=400,
                )

            if len(media_files) == 0:
                return Response(
                    {
                        "code": 400,
                        "message": "At least one media and category required",
                    },
                    status=400,
                )

            # Proses pair by pair
            created = []
            for i in range(len(media_files)):
                req = {
                    "footprint": str(uuid.uuid4()),
                    "training": training_id,
                    "category": categories[i],
                    "media": media_files[i],
                    "hasJerseyNumber": (
                        hasJerseyNumbers[i] if hasJerseyNumbers else None
                    ),
                }
                result = UsecaseFootprint.post(req)
                created.append(result)

            return Response(
                {
                    "code": 201,
                    "message": f"{len(created)} footprints created successfully",
                    "data": created,
                },
                status=201,
            )

        elif request.method == "GET":
            training_id = request.query_params.get("training")
            if training_id:
                data = UsecaseFootprint.get(training_id)
            else:
                data = UsecaseFootprint.get_all()

            return Response(
                {
                    "code": 200,
                    "message": "Footprints retrieved successfully",
                    "data": data,
                },
                status=http_status.HTTP_200_OK,
            )

        elif request.method == "PUT":
            required_fields = ["footprint", "training"]
            if not all(key in request.data for key in required_fields):
                return Response(
                    {
                        "code": 400,
                        "message": f"{', '.join(required_fields)} are required",
                    },
                    status=http_status.HTTP_400_BAD_REQUEST,
                )

            data = UsecaseFootprint.put(request)
            return Response(
                {
                    "code": 200,
                    "message": "Footprint updated successfully",
                    "data": data,
                },
                status=http_status.HTTP_200_OK,
            )

        elif request.method == "DELETE":
            if "footprint" not in request.data:
                return Response(
                    {"code": 400, "message": "footprint id is required"},
                    status=http_status.HTTP_400_BAD_REQUEST,
                )

            data = UsecaseFootprint.delete(request)
            return Response(
                {
                    "code": 200,
                    "message": "Footprint deleted successfully",
                    "data": data,
                },
                status=http_status.HTTP_200_OK,
            )

    except ValidationError as e:
        return Response(
            {"code": 400, "message": str(e)}, status=http_status.HTTP_400_BAD_REQUEST
        )
    except footprint.DoesNotExist:
        return Response(
            {"code": 404, "message": "Footprint not found"},
            status=http_status.HTTP_404_NOT_FOUND,
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


@api_view(["GET", "POST"])
def footprint_category_list_handler(request):
    try:
        if request.method == "GET":
            categories = FootprintCategory.objects.all()
            data = [{"category": cat.category} for cat in categories]
            return Response(
                {
                    "code": 200,
                    "message": "Footprint categories retrieved successfully",
                    "data": data,
                },
                status=http_status.HTTP_200_OK,
            )

        elif request.method == "POST":
            category_name = request.data.get("category")
            if not category_name:
                return Response(
                    {"code": 400, "message": "Field 'category' is required"},
                    status=http_status.HTTP_400_BAD_REQUEST,
                )

            if FootprintCategory.objects.filter(category=category_name).exists():
                return Response(
                    {"code": 409, "message": "Category already exists"},
                    status=http_status.HTTP_409_CONFLICT,
                )

            cat = FootprintCategory.objects.create(category=category_name)
            return Response(
                {
                    "code": 201,
                    "message": "Footprint category created successfully",
                    "data": {"category": cat.category},
                },
                status=http_status.HTTP_201_CREATED,
            )

    except Exception as e:
        return Response(
            {"code": 500, "message": f"Internal server error: {str(e)}"},
            status=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def footprint_category_detail_handler(request, category):
    try:
        try:
            cat = FootprintCategory.objects.get(pk=category)
        except FootprintCategory.DoesNotExist:
            return Response(
                {"code": 404, "message": "Category not found"},
                status=http_status.HTTP_404_NOT_FOUND,
            )

        if request.method == "GET":
            return Response(
                {
                    "code": 200,
                    "message": "Footprint category retrieved successfully",
                    "data": {"category": cat.category},
                },
                status=http_status.HTTP_200_OK,
            )

        elif request.method in ["PUT", "PATCH"]:
            new_category = request.data.get("category")
            if not new_category:
                return Response(
                    {"code": 400, "message": "Field 'category' is required"},
                    status=http_status.HTTP_400_BAD_REQUEST,
                )

            if new_category == category:
                return Response(
                    {
                        "code": 200,
                        "message": "No changes made",
                        "data": {"category": cat.category},
                    },
                    status=http_status.HTTP_200_OK,
                )

            if FootprintCategory.objects.filter(category=new_category).exists():
                return Response(
                    {"code": 409, "message": "Category name already used"},
                    status=http_status.HTTP_409_CONFLICT,
                )

            # Karena category adalah primary key, harus delete lama lalu create baru
            cat.delete()
            new_cat = FootprintCategory.objects.create(category=new_category)
            return Response(
                {
                    "code": 200,
                    "message": "Footprint category updated successfully",
                    "data": {"category": new_cat.category},
                },
                status=http_status.HTTP_200_OK,
            )

        elif request.method == "DELETE":
            cat.delete()
            return Response(
                {
                    "code": 200,
                    "message": "Footprint category deleted successfully",
                },
                status=http_status.HTTP_200_OK,
            )

    except Exception as e:
        return Response(
            {"code": 500, "message": f"Internal server error: {str(e)}"},
            status=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
