# ProfilCoach/views.py
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from .usecase import UsecaseProfilCoach
from rest_framework import status as http_status
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import ProfilCoach


@api_view(["POST", "GET", "PUT", "DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def profil_coach_handler(request):
    try:
        if request.method == "POST":
            print(request.data)
            required_fields = [
                "password",
                "email",
                "nomor_telepon",
                "nama_coach",
                "tanggal_bergabung",
                "tanggal_lahir",
                "kewarganegaraan",
                "tinggi_badan",
                "berat_badan",
            ]
            if not all(key in request.data for key in required_fields):
                return Response(
                    {
                        "code": 400,
                        "message": f"{', '.join(required_fields)} are required",
                    },
                    status=http_status.HTTP_400_BAD_REQUEST,
                )

            data = UsecaseProfilCoach.post(request)
            return Response(
                {"code": 200, "message": "sukses", "data": data},
                status=http_status.HTTP_200_OK,
            )

        elif request.method == "GET":
            coach_id = request.query_params.get("coach")
            if coach_id:
                data = UsecaseProfilCoach.get(coach_id)
            else:
                data = UsecaseProfilCoach.get_all()

            return Response(
                {"code": 200, "message": "sukses", "data": data},
                status=http_status.HTTP_200_OK,
            )

        elif request.method == "PUT":
            print("FILES:", request.FILES)
            print("DATA:", request.data)

            if "coach" not in request.data:
                return Response(
                    {"code": 400, "message": "coach id is required"},
                    status=http_status.HTTP_400_BAD_REQUEST,
                )

            # Pastikan pengguna yang login adalah coach yang bersangkutan
            # profil_coach = ProfilCoach.objects.get(coach=request.data['coach'])
            # if profil_coach.user != request.user:
            #     return Response({
            #         "code": 403,
            #         "message": "Anda tidak memiliki izin untuk mengubah data coach ini."
            #     }, status=http_status.HTTP_403_FORBIDDEN)

            data = UsecaseProfilCoach.put(request)
            message = "Data coach berhasil diperbarui."
            if "password" in request.data:
                message += " Kata sandi juga berhasil diubah."
            if "foto_profil" in request.FILES:
                message += " Foto profil juga berhasil diubah."

            return Response(
                {"code": 200, "message": message, "data": data},
                status=http_status.HTTP_200_OK,
            )

        elif request.method == "DELETE":
            if "coach" not in request.data:
                return Response(
                    {"code": 400, "message": "coach id is required"},
                    status=http_status.HTTP_400_BAD_REQUEST,
                )

            data = UsecaseProfilCoach.delete(request)
            return Response(
                {"code": 200, "message": "sukses", "data": data},
                status=http_status.HTTP_200_OK,
            )

    except ProfilCoach.DoesNotExist:
        return Response(
            {"code": 404, "message": "Coach tidak ditemukan."},
            status=http_status.HTTP_404_NOT_FOUND,
        )
    except ValidationError as e:
        return Response(
            {"code": 400, "message": str(e)}, status=http_status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {"code": 500, "message": str(e)},
            status=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
