from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from wilayah.usecases.wilayah_usecase import WilayahUsecase


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def provinsi_handler(request):
    try:
        data = WilayahUsecase.get_provinsi()

        return Response({"code": 200, "message": "success", "data": data})

    except Exception as e:
        return Response({"code": 500, "message": str(e)})


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def kabupaten_handler(request):
    try:
        kode_provinsi = request.GET.get("kode_provinsi")

        if not kode_provinsi:
            return Response({"code": 400, "message": "kode_provinsi wajib diisi"})

        data = WilayahUsecase.get_kabupaten(kode_provinsi)

        return Response({"code": 200, "message": "success", "data": data})

    except Exception as e:
        return Response({"code": 500, "message": str(e)})
