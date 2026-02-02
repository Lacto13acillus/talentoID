from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import status as http_status
from player.models import player

from .constants import PAYMENT_CHANNELS


@api_view(["GET"])
def get_payment_channels(request):
    return Response(
        {"code": 200, "message": "success", "data": PAYMENT_CHANNELS},
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
def check_payment_status(request, external_id):
    playerModel = get_object_or_404(player, external_id=external_id)

    return Response(
        {
            "external_id": playerModel.external_id,
            "status": playerModel.payment_status,
            "amount": playerModel.amount,
            "paid_at": playerModel.paid_at.isoformat() if playerModel.paid_at else None,
        },
        status=http_status.HTTP_200_OK,
    )
