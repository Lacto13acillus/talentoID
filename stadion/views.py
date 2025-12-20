from rest_framework.decorators import api_view
from rest_framework.response import Response
from .usecase import UsecaseStadion
from rest_framework import status
import json

@api_view(["POST", "GET", "PUT", "DELETE"])
def stadion_handler(request):
    if request.method == "POST":
        # Handle POST request
        if not all(key in request.data for key in ["nama_stadion", "lokasi"]):
            return Response({
                "code": 400,
                "message": "nama_stadion, and lokasi are required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        data = UsecaseStadion.post(request)
        return Response({
            "code": 200,
            "message": "sukses",
            "data": data
        }, status=status.HTTP_200_OK)

    elif request.method == "GET":
        # Handle GET request
        try:
            stadion_id = request.query_params.get("stadion")
            if stadion_id:
                # Existing single stadion GET
                data = UsecaseStadion.get(stadion_id)
                return Response({
                    "code": 200,
                    "message": "sukses",
                    "data": data
                }, status=status.HTTP_200_OK)
            else:
                # New GET ALL implementation
                data = UsecaseStadion.get_all()
                return Response({
                    "code": 200,
                    "message": "sukses",
                    "data": data
                }, status=status.HTTP_200_OK)
                
        except json.JSONDecodeError:
            return Response({
                "code": 400,
                "message": "Invalid JSON in request body"
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "code": 404,
                "message": str(e)
            }, status=status.HTTP_404_NOT_FOUND)

    elif request.method == "PUT":
        # Handle PUT request
        if "stadion" not in request.data:
            return Response({
                "code": 400,
                "message": "stadion is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        data = UsecaseStadion.put(request)
        return Response({
            "code": 200,
            "message": "sukses",
            "data": data
        }, status=status.HTTP_200_OK)

    elif request.method == "DELETE":
        # Handle DELETE request
        if "stadion" not in request.data:
            return Response({
                "code": 400,
                "message": "stadion is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        data = UsecaseStadion.delete(request)
        return Response({
            "code": 200,
            "message": "sukses",
            "data": data
        }, status=status.HTTP_200_OK)


