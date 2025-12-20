from rest_framework.decorators import api_view
from rest_framework.response import Response
from .usecase import UsecaseTrainingCategory
from rest_framework import status
import json

@api_view(["POST", "GET", "PUT", "DELETE"])
def trainingcategory_handler(request):
    if request.method == "POST":
        # Handle POST request
        if not all(key in request.data for key in ["nama_category"]):
            return Response({
                "code": 400,
                "message": "nama_category are required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        data = UsecaseTrainingCategory.post(request)
        return Response({
            "code": 200,
            "message": "sukses",
            "data": data
        }, status=status.HTTP_200_OK)

    elif request.method == "GET":
        # Handle GET request
        try:
            trainingcategory_id = request.query_params.get("trainingcategory")
            if trainingcategory_id:
                # Existing single trainingcategory GET
                data = UsecaseTrainingCategory.get(trainingcategory_id)
                return Response({
                    "code": 200,
                    "message": "sukses",
                    "data": data
                }, status=status.HTTP_200_OK)
            else:
                # New GET ALL implementation
                data = UsecaseTrainingCategory.get_all()
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
        if "trainingcategory" not in request.data:
            return Response({
                "code": 400,
                "message": "trainingcategory is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        data = UsecaseTrainingCategory.put(request)
        return Response({
            "code": 200,
            "message": "sukses",
            "data": data
        }, status=status.HTTP_200_OK)

    elif request.method == "DELETE":
        # Handle DELETE request
        if "trainingcategory" not in request.data:
            return Response({
                "code": 400,
                "message": "trainingcategory is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        data = UsecaseTrainingCategory.delete(request)
        return Response({
            "code": 200,
            "message": "sukses",
            "data": data
        }, status=status.HTTP_200_OK)




