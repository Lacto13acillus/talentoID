from rest_framework.decorators import api_view
from rest_framework.response import Response
from .usecase import UsecaseUser
from rest_framework import status
from django.core.exceptions import ValidationError


@api_view(["POST", "GET", "PUT", "DELETE"])
def user_handler(request):
    try:
        if request.method == "POST":
            required_fields = ["nama", "email", "password"]
            if not all(key in request.data for key in required_fields):
                return Response(
                    {
                        "code": 400,
                        "message": f"{', '.join(required_fields)} are required",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            data = UsecaseUser.post(request)
            return Response(
                {"code": 200, "message": "sukses", "data": data},
                status=status.HTTP_200_OK,
            )

        elif request.method == "GET":
            try:
                user_id = request.query_params.get("id_user")
                print(user_id)
                if user_id:
                    # Existing single user GET
                    data = UsecaseUser.get(user_id)
                    return Response(
                        {"code": 200, "message": "sukses by user id", "data": data},
                        status=status.HTTP_200_OK,
                    )
                else:
                    # New GET ALL implementation
                    data = UsecaseUser.get_all()
                    return Response(
                        {"code": 200, "message": "sukses get all", "data": data},
                        status=status.HTTP_200_OK,
                    )
            except Exception as e:
                return Response(
                    {"code": 404, "message": str(e)}, status=status.HTTP_404_NOT_FOUND
                )

        elif request.method == "PUT":
            if "id_user" not in request.data:
                return Response(
                    {"code": 400, "message": "id_user is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            data = UsecaseUser.put(request)
            return Response(
                {"code": 200, "message": "sukses", "data": data},
                status=status.HTTP_200_OK,
            )

        elif request.method == "DELETE":
            if "id_user" not in request.data:
                return Response(
                    {"code": 400, "message": "id is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            data = UsecaseUser.delete(request)
            return Response(
                {"code": 200, "message": "sukses", "data": data},
                status=status.HTTP_200_OK,
            )

    except ValidationError as e:
        return Response(
            {"code": 400, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        print(e)
        return Response(
            {"code": 500, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
def login_handler(request):
    try:
        if request.method == "POST":
            required_fields = ["email", "password"]
            if not all(key in request.data for key in required_fields):
                return Response(
                    {
                        "code": 400,
                        "message": f"{', '.join(required_fields)} are required",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            data = UsecaseUser.login(request)
            return Response(
                {"code": 200, "message": "sukses", "data": data},
                status=status.HTTP_200_OK,
            )

    except ValidationError as e:
        message = e.messages[0] if hasattr(e, "messages") and e.messages else str(e)
        return Response(
            {"code": 400, "message": message}, status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        message = e.messages[0] if hasattr(e, "messages") and e.messages else str(e)
        return Response(
            {"code": 500, "message": message},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
def delete_account_handler(request):
    try:
        if request.method == "GET":
            user_id = request.query_params.get("user_id")
            if not user_id:
                return Response(
                    {"code": 400, "message": "user_id is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            delete_response = UsecaseUser.delete_account(user_id)
            return Response(
                {
                    "code": 200,
                    "message": "Akun berhasil dihapus",
                    "data": delete_response,
                },
                status=status.HTTP_200_OK,
            )

    except ValidationError as e:
        message = e.messages[0] if hasattr(e, "messages") and e.messages else str(e)
        return Response(
            {"code": 400, "message": message}, status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        message = e.messages[0] if hasattr(e, "messages") and e.messages else str(e)
        return Response(
            {"code": 500, "message": message},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
