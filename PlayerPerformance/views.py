from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status as http_status
from .usecase import UsecasePlayerPerformance
from django.core.exceptions import ValidationError


@api_view(["POST", "GET", "PUT", "DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def player_performance_handler(request):
    try:
        if request.method == "POST":
            if "player" not in request.data or "metrics" not in request.data:
                return Response(
                    {"code": 400, "message": "player, metric, and value are required."},
                    status=http_status.HTTP_400_BAD_REQUEST,
                )
            # Cek minimal salah satu: training atau match harus ada
            if not request.data.get("training") and not request.data.get("match"):
                return Response(
                    {
                        "code": 400,
                        "message": "Either training or match must be provided.",
                    },
                    status=http_status.HTTP_400_BAD_REQUEST,
                )

            # Cek jika dua-duanya diisi (tidak boleh)
            if request.data.get("training") and request.data.get("match"):
                return Response(
                    {
                        "code": 400,
                        "message": "Only one of training or match should be provided, not both.",
                    },
                    status=http_status.HTTP_400_BAD_REQUEST,
                )

            player = request.data["player"]
            training = request.data.get("training")
            match = request.data.get("match")
            metrics = request.data["metrics"]
            saved_records = []
            for metric in metrics:
                category_id = metric.get("category_id")
                metric_id = metric.get("metric_id")
                value = metric.get("value")

                if not all([category_id, metric_id, value]):
                    continue  # Skip invalid entries

                result = UsecasePlayerPerformance.post(
                    player_id=player,
                    training_id=training,
                    match_id=match,
                    metric_id=metric_id,
                    value=value,
                )
                saved_records.append(result)
            return Response(
                {"code": 200, "message": "success", "data": saved_records},
                status=http_status.HTTP_200_OK,
            )

        elif request.method == "GET":
            match_id = request.query_params.get("match_id")
            metric = request.query_params.get("metric")
            team_id = request.query_params.get("team")
            player_id = request.query_params.get("player_id")
            start_date = request.query_params.get("start_date")
            end_date = request.query_params.get("end_date")

            if metric:
                if metric == "player":
                    if not match_id:
                        return Response(
                            {
                                "code": 400,
                                "message": "match_id is required for player metric",
                            },
                            status=http_status.HTTP_400_BAD_REQUEST,
                        )
                    data = UsecasePlayerPerformance.get_by_match_id(match_id)

                elif metric == "summary":
                    if not match_id:
                        return Response(
                            {
                                "code": 400,
                                "message": "match_id is required for summary metric",
                            },
                            status=http_status.HTTP_400_BAD_REQUEST,
                        )
                    data = UsecasePlayerPerformance.get_by_match_id_summary(match_id)

                elif metric == "team":
                    if not team_id:
                        return Response(
                            {
                                "code": 400,
                                "message": "team is required for team metric",
                            },
                            status=http_status.HTTP_400_BAD_REQUEST,
                        )
                    data = UsecasePlayerPerformance.get_by_team_id(team_id)

                else:
                    return Response(
                        {"code": 400, "message": f"Unsupported metric type: {metric}"},
                        status=http_status.HTTP_400_BAD_REQUEST,
                    )

            elif player_id:
                if match_id:
                    data = UsecasePlayerPerformance.get_by_player_id_and_match_id(
                        player_id, match_id
                    )
                else:
                    data = UsecasePlayerPerformance.get_by_player_id(
                        player_id, start_date, end_date
                    )

            else:
                data = UsecasePlayerPerformance.get_all()

            return Response(
                {"code": 200, "message": "success", "data": data},
                status=http_status.HTTP_200_OK,
            )
        elif request.method == "PUT":
            if "player_performance" not in request.data:
                return Response(
                    {"code": 400, "message": "player_performance ID is required"},
                    status=http_status.HTTP_400_BAD_REQUEST,
                )
            data = UsecasePlayerPerformance.put(request)
            return Response(
                {"code": 200, "message": "success", "data": data},
                status=http_status.HTTP_200_OK,
            )

        elif request.method == "DELETE":
            if "player_performance" not in request.data:
                return Response(
                    {"code": 400, "message": "player_performance ID is required"},
                    status=http_status.HTTP_400_BAD_REQUEST,
                )
            data = UsecasePlayerPerformance.delete(request)
            return Response(
                {"code": 200, "message": "success", "data": data},
                status=http_status.HTTP_200_OK,
            )

    except ValidationError as e:
        message = e.messages[0] if hasattr(e, "messages") and e.messages else str(e)
        return Response(
            {"code": 400, "message": message}, status=http_status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        message = e.messages[0] if hasattr(e, "messages") and e.messages else str(e)
        return Response(
            {"code": 500, "message": message},
            status=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
def player_standing_handler(request):
    if request.method == "GET":
        limit = request.query_params.get("limit")

        return Response(
            {
                "code": 200,
                "message": "success",
                "data": UsecasePlayerPerformance.get_standings(request),
            },
            status=http_status.HTTP_200_OK,
        )
