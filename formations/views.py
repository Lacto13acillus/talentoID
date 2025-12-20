from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .usecase import UsecaseFormation

@api_view(["POST", "GET", "PUT", "DELETE"])
def formation_handler(request):
    try:
        if request.method == "POST":
            required_fields = ["formasi"]
            if not all(key in request.data for key in required_fields):
                return Response({
                    "code": 400,
                    "message": "formasi are required"
                }, status=status.HTTP_400_BAD_REQUEST)

            data = UsecaseFormation.post(request)
            return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=status.HTTP_200_OK)

        elif request.method == "GET":
            id_formasi = request.query_params.get("id_formasi")
            if id_formasi:
                # GET by ID
                data = UsecaseFormation.get_by_id(id_formasi)
                return Response({
                    "code": 200,
                    "message": "sukses",
                    "data": data
                }, status=status.HTTP_200_OK)
            
            else:
                # GET ALL
                data = UsecaseFormation.get_all()
                return Response({
                    "code": 200,
                    "message": "sukses",
                    "data": data
                }, status=status.HTTP_200_OK)

        elif request.method == "PUT":
            required_fields = ["id_formasi", "formasi"]
            if not all(key in request.data for key in required_fields):
                return Response({
                    "code": 400,
                    "message": "id_formasi and formasi are required"
                }, status=status.HTTP_400_BAD_REQUEST)

            data = UsecaseFormation.put(request)
            return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=status.HTTP_200_OK)

        elif request.method == "DELETE":
            if "id_formasi" not in request.data:
                return Response({
                    "code": 400,
                    "message": "id_formasi is required"
                }, status=status.HTTP_400_BAD_REQUEST)

            data = UsecaseFormation.delete(request)
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