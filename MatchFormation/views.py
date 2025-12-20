from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .usecase import UsecaseMatchFormations

@api_view(["POST", "GET", "PUT", "DELETE"])
def matchformations_handler(request):
    try:
        if request.method == "POST":
            required_fields = ["id_formations"]
            if not all(key in request.data for key in required_fields):
                return Response({
                    "code": 400,
                    "message": "id_formations is required"
                }, status=status.HTTP_400_BAD_REQUEST)

            data = UsecaseMatchFormations.post(request)
            return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=status.HTTP_200_OK)

        elif request.method == "GET":
            matchformation_id = request.query_params.get("id_matchformations")
            if matchformation_id:
                data = UsecaseMatchFormations.get(matchformation_id)
                return Response({
                    "code": 200,
                    "message": "sukses",
                    "data": data
                }, status=status.HTTP_200_OK)
            else:
                data = UsecaseMatchFormations.get_all()
                return Response({
                    "code": 200,
                    "message": "sukses",
                    "data": data
                }, status=status.HTTP_200_OK)

        elif request.method == "PUT":
            required_fields = ["id_matchformations", "id_formations"]
            if not all(key in request.data for key in required_fields):
                return Response({
                    "code": 400,
                    "message": "id_matchformations and id_formations are required"
                }, status=status.HTTP_400_BAD_REQUEST)

            data = UsecaseMatchFormations.put(request)
            return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=status.HTTP_200_OK)

        elif request.method == "DELETE":
            if "id_matchformations" not in request.data:
                return Response({
                    "code": 400,
                    "message": "id_matchformations is required"
                }, status=status.HTTP_400_BAD_REQUEST)

            data = UsecaseMatchFormations.delete(request)
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