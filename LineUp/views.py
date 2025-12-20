from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .usecase import UsecaseLineUp

@api_view(["POST", "GET", "PUT", "DELETE"])
def lineup_handler(request):
    try:
        if request.method == "POST":
            required_fields = ["player_id", "index", "status"]
            if not all(key in request.data for key in required_fields):
                return Response({
                    "code": 400,
                    "message": "player_id, index, and status are required"
                }, status=status.HTTP_400_BAD_REQUEST)

            data = UsecaseLineUp.post(request)
            return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=status.HTTP_200_OK)

        elif request.method == "GET":
            lineup_id = request.query_params.get("id_lineup")
            if lineup_id:
                data = UsecaseLineUp.get(lineup_id)
                return Response({
                    "code": 200,
                    "message": "sukses",
                    "data": data
                }, status=status.HTTP_200_OK)
            else:
                data = UsecaseLineUp.get_all()
                return Response({
                    "code": 200,
                    "message": "sukses",
                    "data": data
                }, status=status.HTTP_200_OK)

        elif request.method == "PUT":
            required_fields = ["id_lineup", "player_id", "index", "status"]
            if not all(key in request.data for key in required_fields):
                return Response({
                    "code": 400,
                    "message": "id_lineup, player_id, index, and status are required"
                }, status=status.HTTP_400_BAD_REQUEST)

            data = UsecaseLineUp.put(request)
            return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=status.HTTP_200_OK)

        elif request.method == "DELETE":
            if "id_lineup" not in request.data:
                return Response({
                    "code": 400,
                    "message": "id_lineup is required"
                }, status=status.HTTP_400_BAD_REQUEST)

            data = UsecaseLineUp.delete(request)
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