from rest_framework.decorators import api_view
from rest_framework.response import Response
from .usecase import UsecaseStatus
from rest_framework import status as http_status
from .models import status

@api_view(["POST", "GET", "PUT", "DELETE"])
def status_handler(request):
    try:
        if request.method == "POST":
            # Validate required fields
            if "match_status" not in request.data:
                return Response({
                    "code": 400,
                    "message": "match_status is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)
            
            # Normalize and validate match_status
            input_status = request.data['match_status']
            valid_choices = [choice[0] for choice in status.STATUS_CHOICES]
            choice_map = {choice.lower(): choice for choice in valid_choices}
            if input_status.lower() not in choice_map:
                return Response({
                    "code": 400,
                    "message": f"match_status must be one of {valid_choices}"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            data = UsecaseStatus.post(request)
            return Response({
                "code": 201,
                "message": "Success",
                "data": data
            }, status=http_status.HTTP_201_CREATED)

        elif request.method == "GET":
            status_id = request.query_params.get("status")
            if status_id:
                data = UsecaseStatus.get(status_id)
                return Response({
                    "code": 200,
                    "message": "Success",
                    "data": data
                }, status=http_status.HTTP_200_OK)
            else:
                data = UsecaseStatus.get_all()
                return Response({
                    "code": 200,
                    "message": "Success",
                    "data": data
                }, status=http_status.HTTP_200_OK)

        elif request.method == "PUT":
            if "status" not in request.data:
                return Response({
                    "code": 400,
                    "message": "status is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)
            
            # Normalize and validate match_status if provided
            if 'match_status' in request.data and request.data['match_status']:
                input_status = request.data['match_status']
                valid_choices = [choice[0] for choice in status.STATUS_CHOICES]
                choice_map = {choice.lower(): choice for choice in valid_choices}
                if input_status.lower() not in choice_map:
                    return Response({
                        "code": 400,
                        "message": f"match_status must be one of {valid_choices}"
                    }, status=http_status.HTTP_400_BAD_REQUEST)

            usecase = UsecaseStatus()
            data = usecase.put(request)
            return Response({
                "code": 200,
                "message": "Success",
                "data": data
            }, status=http_status.HTTP_200_OK)

        elif request.method == "DELETE":
            if "status" not in request.data:
                return Response({
                    "code": 400,
                    "message": "status is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

            usecase = UsecaseStatus()
            data = usecase.delete(request)
            return Response({
                "code": 200,
                "message": "Success",
                "data": data
            }, status=http_status.HTTP_200_OK)

    except ValueError as ve:
        return Response({
            "code": 400,
            "message": str(ve)
        }, status=http_status.HTTP_400_BAD_REQUEST)
    except status.DoesNotExist:
        return Response({
            "code": 404,
            "message": "Status not found"
        }, status=http_status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            "code": 500,
            "message": f"Internal server error: {str(e)}"
        }, status=http_status.HTTP_500_INTERNAL_SERVER_ERROR)