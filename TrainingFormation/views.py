# trainingformation/views/trainingformation_views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .usecase import UsecaseTrainingFormation

@api_view(["POST", "GET", "PUT", "DELETE"])
def trainingformation_handler(request):
    try:
        if request.method == "POST":
            required_fields = ["id_formations", "id_lineup"]
            if not all(key in request.data for key in required_fields):
                return Response({
                    "code": 400,
                    "message": "id_formations and id_lineup are required"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Validate that id_lineup is a list
            if not isinstance(request.data['id_lineup'], list):
                return Response({
                    "code": 400,
                    "message": "id_lineup must be a list of lineup IDs"
                }, status=status.HTTP_400_BAD_REQUEST)

            data = UsecaseTrainingFormation.post(request)
            return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=status.HTTP_200_OK)

        elif request.method == "GET":
            trainingformation_id = request.query_params.get("id_trainingformation")
            if trainingformation_id:
                data = UsecaseTrainingFormation.get(trainingformation_id)
                return Response({
                    "code": 200,
                    "message": "sukses",
                    "data": data
                }, status=status.HTTP_200_OK)
            else:
                data = UsecaseTrainingFormation.get_all()
                return Response({
                    "code": 200,
                    "message": "sukses",
                    "data": data
                }, status=status.HTTP_200_OK)

        elif request.method == "PUT":
            required_fields = ["id_trainingformation", "id_formations", "id_lineup"]
            if not all(key in request.data for key in required_fields):
                return Response({
                    "code": 400,
                    "message": "id_trainingformation, id_formations, and id_lineup are required"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Validate that id_lineup is a list
            if not isinstance(request.data['id_lineup'], list):
                return Response({
                    "code": 400,
                    "message": "id_lineup must be a list of lineup IDs"
                }, status=status.HTTP_400_BAD_REQUEST)

            data = UsecaseTrainingFormation.put(request)
            return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=status.HTTP_200_OK)

        elif request.method == "DELETE":
            if "id_trainingformation" not in request.data:
                return Response({
                    "code": 400,
                    "message": "id_trainingformation is required"
                }, status=status.HTTP_400_BAD_REQUEST)

            data = UsecaseTrainingFormation.delete(request)
            return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            "code": 500,
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)