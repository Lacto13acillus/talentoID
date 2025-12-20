from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .usecase import UsecaseClub
from rest_framework.response import Response
from rest_framework import status as http_status
from django.core.exceptions import ValidationError

# Create your views here.

@api_view(["POST", "GET", "PUT", "DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def club_handler(request):
	try:
		if request.method == "POST":
			print(request.POST)
			print(request.FILES)
			if "club_name" not in request.POST:
				return Response({
                    "code": 400,
                    "message": "Club name is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)
			data = UsecaseClub.post(request)
			return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=http_status.HTTP_200_OK)

		elif request.method == "GET":
			club = request.query_params.get("club")
			player = request.query_params.get("player")

			if player:
				data = UsecaseClub.get_club_info_by_player_id(player)
				if not data:
					return Response({
						"code": 404,
						"message": "Player not found"
					}, status=http_status.HTTP_404_NOT_FOUND)
				return Response({
					"code": 200,
					"message": "sukses",
					"data": data
				}, status=http_status.HTTP_200_OK)

			elif club:
				data = UsecaseClub.get(club)
				return Response({
					"code": 200,
					"message": "sukses",
					"data": data
				}, status=http_status.HTTP_200_OK)

			else:
				data = UsecaseClub.get_all()
				return Response({
					"code": 200,
					"message": "sukses",
					"data": data
				}, status=http_status.HTTP_200_OK)

		elif request.method == "PUT":
			if "club" not in request.data:
				return Response({
                    "code": 400,
                    "message": "player id is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)

			data = UsecaseClub.put(request)
			return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=http_status.HTTP_200_OK)
		elif request.method == "DELETE":
			if "club" not in request.data:
				return Response({
                    "code": 400,
                    "message": "club id is required"
                }, status=http_status.HTTP_400_BAD_REQUEST)
			data = UsecaseClub.delete(request)
			return Response({
                "code": 200,
                "message": "sukses",
                "data": data
            }, status=http_status.HTTP_200_OK)
	except ValidationError as e:
		return Response({
            "code": 400,
            "message": str(e)
        }, status=http_status.HTTP_400_BAD_REQUEST)
	except Exception as e:
		return Response({
            "code": 500,
            "message": str(e)
        }, status=http_status.HTTP_500_INTERNAL_SERVER_ERROR)
