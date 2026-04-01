from .models import PlayerPerformance
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from Metric.models import Metric
from player.models import player
from team.models import team
from pertandingan.models import pertandingan
from training.models import training
from collections import defaultdict
from django.db.models import Avg
from django.db.models import Q
from datetime import datetime


class RepoPlayerPerformance:
    @staticmethod
    def get_all():
        performances = PlayerPerformance.objects.select_related(
            "player", "match", "metric"
        )
        grouped_data = defaultdict(
            lambda: defaultdict(
                lambda: {
                    "player_name": "",
                    "foto_profil": "",
                    # "kewarganegaraan": "",
                    "foto_profil": "",
                    "posisi": "",
                    "metrics": [],
                }
            )
        )

        match_infos = {}

        for perf in performances:
            match_id = str(perf.match.match)
            player_id = str(perf.player.player)
            if match_id not in match_infos:
                match_infos[match_id] = {
                    "match": match_id,
                    "nama_pertandingan": perf.match.nama_pertandingan,
                    "team_home": {
                        "team": perf.match.tim_home.team,
                        "nama_team": perf.match.tim_home.nama_team,
                        "kategori_team": perf.match.tim_home.kategori_team,
                        "logo_team": perf.match.tim_home.logo_team.url,
                    },
                    "team_away": {
                        "team": perf.match.tim_away.team,
                        "nama_team": perf.match.tim_away.nama_team,
                        "kategori_team": perf.match.tim_away.kategori_team,
                        "logo_team": perf.match.tim_away.logo_team.url,
                    },
                }
            grouped_data[match_id][player_id]["player_name"] = perf.player.nama
            grouped_data[match_id][player_id][
                "foto_profil"
            ] = perf.player.foto_profil.url
            grouped_data[match_id][player_id]["posisi"] = perf.player.posisi
            # grouped_data[match_id][player_id][
            #     "kewarganegaraan"
            # ] = perf.player.kewarganegaraan

            grouped_data[match_id][player_id]["metrics"].append(
                {
                    "metric_category_name": perf.metric.metric_category.name,
                    "metric_name": perf.metric.name,
                    "value": perf.value,
                }
            )

        result = []
        for match_id, players in grouped_data.items():
            result.append(
                {
                    "match": match_infos[match_id],
                    "players": [
                        {
                            "player_id": player_id,
                            "player_name": data["player_name"],
                            "foto_profil": data["foto_profil"],
                            # "kewarganegaraan": data["kewarganegaraan"],
                            "posisi": data["posisi"],
                            "metrics": data["metrics"],
                        }
                        for player_id, data in players.items()
                    ],
                }
            )

        return result

    @staticmethod
    def calculate_accuracy(metrics, success_key, attempted_key):
        success = None
        attempted = None

        for m in metrics:
            if m["metric_name"] == success_key:
                success = m["value"]
            elif m["metric_name"] == attempted_key:
                attempted = m["value"]

        if success is not None and attempted:
            return round((success / attempted) * 100, 2)
        return None

    @staticmethod
    def get_by_match_id(match_id_target=None):
        performances = PlayerPerformance.objects.select_related(
            "player", "match", "metric"
        )

        if match_id_target:
            performances = performances.filter(match__match=match_id_target)

        if not performances.exists():
            return None if match_id_target else []

        players_data = defaultdict(
            lambda: {
                "player_name": "",
                "foto_profil": "",
                # "kewarganegaraan": "",
                "posisi": "",
                "metrics": [],
            }
        )

        match_info = None
        if match_id_target:
            first_perf = performances[0]
            match_info = {
                "id": str(first_perf.match.match),
                "name": first_perf.match.nama_pertandingan,
                "team_home": first_perf.match.tim_home.nama_team,
                "team_home_logo": first_perf.match.tim_home.logo_team.url,
                "team_away": first_perf.match.tim_away.nama_team,
                "team_away_logo": first_perf.match.tim_away.logo_team.url,
            }

        for perf in performances:
            player_id = str(perf.player.player)

            players_data[player_id]["player_name"] = perf.player.nama
            players_data[player_id]["foto_profil"] = (
                perf.player.foto_profil.url if perf.player.foto_profil else ""
            )
            # players_data[player_id]["kewarganegaraan"] = perf.player.kewarganegaraan
            players_data[player_id]["posisi"] = perf.player.posisi

            players_data[player_id]["metrics"].append(
                {
                    "metric_category_name": perf.metric.metric_category.name,
                    "metric_name": perf.metric.name,
                    "value": perf.value,
                }
            )

        result = [
            {
                "player_id": player_id,
                "player_name": data["player_name"],
                "foto_profil": data["foto_profil"],
                # "kewarganegaraan": data["kewarganegaraan"],
                "posisi": data["posisi"],
                "passing_accuracy": RepoPlayerPerformance.calculate_accuracy(
                    data["metrics"], "Pass Success", "Pass Attempted"
                ),
                "dribble_accuracy": RepoPlayerPerformance.calculate_accuracy(
                    data["metrics"], "Dribble Success", "Dribble Attempted"
                ),
                "cross_accuracy": RepoPlayerPerformance.calculate_accuracy(
                    data["metrics"], "Cross Success", "Cross Total"
                ),
                "shots_on_target": RepoPlayerPerformance.calculate_accuracy(
                    data["metrics"], "Shots on Target", "Shots Total"
                ),
                "metrics": data["metrics"],
            }
            for player_id, data in players_data.items()
        ]

        if match_info:
            return {"match": match_info, "players": result}

        return result

    @staticmethod
    def get_by_team_id(team_id):
        team_instance = get_object_or_404(team, pk=team_id)
        performances = PlayerPerformance.objects.select_related(
            "player__tim",
            "metric",
            "metric__metric_category",
        ).filter(player__tim=team_instance)

        metrics_group = defaultdict(
            lambda: {
                "values": [],
                "category": "",
                "description": "",
                "player_values": defaultdict(lambda: {"total": 0.0, "count": 0}),
            }
        )

        for perf in performances:
            metric = perf.metric.metric
            metric_name = perf.metric.name
            metric_category_name = perf.metric.metric_category.name
            metric_description = perf.metric.description or ""

            player_name = perf.player.nama

            try:
                value = float(perf.value)
            except (TypeError, ValueError):
                continue

            metrics_group[metric_name]["values"].append(value)
            metrics_group[metric_name]["metric"] = metric
            metrics_group[metric_name]["category"] = metric_category_name
            metrics_group[metric_name]["description"] = metric_description
            metrics_group[metric_name]["player_values"][player_name]["total"] += value
            metrics_group[metric_name]["player_values"][player_name]["count"] += 1

        metrics_grouped = defaultdict(list)

        for metric_name, data in metrics_group.items():
            player_values = data["player_values"]
            if not player_values:
                continue
            values = data["values"]
            if not values:
                continue

            contributions = []
            for player_name, pv in player_values.items():
                total_value = pv["total"]
                count = pv["count"]
                avg_value = total_value / count if count > 0 else 0

                contributions.append(
                    {
                        "player_name": player_name,
                        "total_value": round(total_value, 2),
                        "average_value": round(avg_value, 2),
                        "count": count,
                    }
                )

            # Sort contributions descending by total_value
            contributions.sort(key=lambda x: x["total_value"], reverse=True)

            metrics_grouped[data["category"]].append(
                {
                    "name": metric_name,
                    "metric_description": data["description"],
                    "metric": data["metric"],
                    "metric_category_name": data["category"],
                    "average": round(sum(values) / len(values), 2),
                    "total": round(sum(values), 2),
                    "contributions": contributions,
                }
            )

        return {
            "team": team_instance.team,
            "team_name": team_instance.nama_team,
            "team_category": team_instance.kategori_team,
            "team_logo": team_instance.logo_team.url,
            "team_coach_name": (
                team_instance.coach.user.nama if team_instance.coach else None
            ),
            # "team_club_name": (
            #     team_instance.club.club_name if team_instance.club else None
            # ),
            "metrics_grouped": metrics_grouped,
        }

    @staticmethod
    def get_by_match_id_summary(match_id_target: str):
        performances = PlayerPerformance.objects.select_related(
            "player", "match", "metric"
        ).filter(match__match=match_id_target)

        if not performances.exists():
            return None

        first_perf = performances[0]
        match_info = {
            "id": str(first_perf.match.match),
            "name": first_perf.match.nama_pertandingan,
            "team_home": first_perf.match.tim_home.nama_team,
            "team_home_logo": first_perf.match.tim_home.logo_team.url,
            "team_away": first_perf.match.tim_away.nama_team,
            "team_away_logo": first_perf.match.tim_away.logo_team.url,
        }

        # Ini bagian penting: grup berdasarkan metric
        metrics_data = defaultdict(list)
        metric_categories = {}

        for perf in performances:
            metric_name = perf.metric.name
            metric_category_name = perf.metric.metric_category.name
            if metric_name not in metric_categories:
                metric_categories[metric_name] = metric_category_name
            metrics_data[metric_name].append(
                {
                    "player_id": str(perf.player.player),
                    "player_name": perf.player.nama,
                    "value": perf.value,
                }
            )

        # Format akhir jadi list
        formatted_metrics = [
            {
                "metric_category_name": metric_categories[metric_name],
                "metric_name": metric_name,
                "players": players,
            }
            for metric_name, players in metrics_data.items()
        ]

        return {"match": match_info, "metrics": formatted_metrics}

    @staticmethod
    def get_by_player_id(
        player_id_target=None, match_id_target=None, start_date=None, end_date=None
    ):
        performances = PlayerPerformance.objects.select_related(
            "player", "match", "training", "metric", "metric__metric_category"
        )
        if player_id_target:
            performances = performances.filter(player__player=player_id_target)

        if start_date or end_date:
            date_filter = Q()

            if start_date:
                start = datetime.fromisoformat(start_date).date()
                date_filter &= Q(match__date__gte=start) | Q(training__date__gte=start)

            if end_date:
                end = datetime.fromisoformat(end_date).date()
                date_filter &= Q(match__date__lte=end) | Q(training__date__lte=end)

            performances = performances.filter(date_filter)

        kkm_global = RepoPlayerPerformance.get_kkm_global_by_category(
            start_date, end_date
        )
        kkm_player = RepoPlayerPerformance.get_kkm_player_by_category(
            player_id_target, start_date, end_date
        )

        # Simpan: {category: {context: {metric_name: value}}}
        breakdown_map = defaultdict(lambda: defaultdict(dict))

        # Grouping: {category -> {match_or_training_key -> {metric_name: value}}}
        grouped = defaultdict(lambda: defaultdict(dict))

        for perf in performances:
            category = perf.metric.metric_category.name
            metric_name = perf.metric.name

            # Tentukan context key
            if perf.match:
                context_key = f"match_{perf.match.match}"
            elif perf.training:
                context_key = f"training_{perf.training.training}"
            else:
                continue

            value = float(perf.value)
            breakdown_map[category][context_key][metric_name] = value

        for perf in performances:
            category = perf.metric.metric_category.name
            metric_name = perf.metric.name.lower().replace(" ", "_")

            # Tentukan key grouping berdasarkan match atau training
            if perf.match:
                context_key = f"match_{perf.match.match}"
                context_type = "match"
                context_name = getattr(
                    perf.match,
                    "nama_pertandingan",
                )  # Sesuaikan field name
                context_date = perf.match.date
            elif perf.training:
                context_key = f"training_{perf.training.training}"
                context_type = "training"
                context_name = getattr(
                    perf.training,
                    "nama_latihan",
                )  # Sesuaikan field name
                context_date = perf.training.date
            else:
                continue  # Skip kalau tidak ada match/training

            # Simpan metadata (hanya sekali per context)
            if "metadata" not in grouped[category][context_key]:
                grouped[category][context_key]["metadata"] = {
                    "type": context_type,
                    "name": context_name,
                    "date": context_date.isoformat() if context_date else None,
                }

            # Simpan metric values
            if "metrics" not in grouped[category][context_key]:
                grouped[category][context_key]["metrics"] = {}

            grouped[category][context_key]["metrics"][metric_name] = float(perf.value)

        result = defaultdict(list)

        result = {}

        for category, contexts in grouped.items():
            items = []

            for context_key, data in contexts.items():
                metrics = data["metrics"]
                values = list(metrics.values())

                # Category score per match (average metric)
                category_score = round(sum(values) / len(values), 2) if values else None

                items.append(
                    {
                        "context": context_key,
                        "type": data["metadata"]["type"],
                        "name": data["metadata"]["name"],
                        "date": data["metadata"]["date"],
                        "category_score": category_score,
                        "passed_global": (
                            category_score >= kkm_global.get(category)
                            if category_score is not None
                            and kkm_global.get(category) is not None
                            else None
                        ),
                        "passed_player": (
                            category_score >= kkm_player.get(category)
                            if category_score is not None
                            and kkm_player.get(category) is not None
                            else None
                        ),
                        "metrics": metrics,
                    }
                )

            result[category] = {
                "kkm": {
                    "global": kkm_global.get(category),
                    "player": kkm_player.get(category),
                },
                "items": items,
            }

        return result

    @staticmethod
    def get_kkm_global_by_category(start_date=None, end_date=None):
        qs = PlayerPerformance.objects.all()

        if start_date or end_date:
            qs = qs.filter(RepoPlayerPerformance._date_filter_q(start_date, end_date))

        qs = qs.values("metric__metric_category__name").annotate(kkm=Avg("value"))

        return {
            row["metric__metric_category__name"]: round(float(row["kkm"]), 2)
            for row in qs
        }

    @staticmethod
    def get_kkm_player_by_category(player_id, start_date=None, end_date=None):
        qs = PlayerPerformance.objects.filter(player__player=player_id)

        if start_date or end_date:
            qs = qs.filter(RepoPlayerPerformance._date_filter_q(start_date, end_date))

        qs = qs.values("metric__metric_category__name").annotate(kkm=Avg("value"))

        return {
            row["metric__metric_category__name"]: round(float(row["kkm"]), 2)
            for row in qs
        }

    def _date_filter_q(start_date=None, end_date=None):
        q = Q()

        if start_date:
            start = datetime.fromisoformat(start_date).date()
            q &= Q(match__date__gte=start) | Q(training__date__gte=start)

        if end_date:
            end = datetime.fromisoformat(end_date).date()
            q &= Q(match__date__lte=end) | Q(training__date__lte=end)

        return q

    @staticmethod
    def get_by_id(performance_id):
        return (
            PlayerPerformance.objects.filter(player_performance=performance_id)
            .values()
            .first()
        )

    @staticmethod
    def put(data):
        try:
            performance_id = data.get("player_performance")
            if not performance_id:
                raise ValidationError("player_performance ID is required.")

            performance = get_object_or_404(
                PlayerPerformance, player_performance=performance_id
            )

            if "metric" in data:
                performance.metric = get_object_or_404(
                    Metric, metric=data.get("metric")
                )

            if "player" in data:
                performance.player = get_object_or_404(
                    player, player=data.get("player")
                )

            if "value" in data:
                performance.value = data.get("value")

            # Reset both to None first
            performance.match = None
            performance.training = None

            # Set match or training, not both
            if "match" in data and data["match"]:
                performance.match = get_object_or_404(
                    pertandingan, match=data.get("match")
                )

            if "training" in data and data["training"]:
                if performance.match:
                    raise ValidationError(
                        "Only one of match or training can be provided."
                    )
                performance.training = get_object_or_404(
                    training, training=data.get("training")
                )

            if not performance.match and not performance.training:
                raise ValidationError("Either match or training must be provided.")

            performance.save()

            return {
                "player_performance": str(performance.player_performance),
                "message": "Player performance updated successfully.",
            }

        except ValidationError as e:
            raise e

    @staticmethod
    def post(player_id, training_id, match_id, metric_id, value):
        try:

            # Ambil objek metric dan player
            metric = get_object_or_404(Metric, metric=metric_id)
            player_obj = get_object_or_404(player, player=player_id)

            if match_id and training_id:
                raise ValidationError("Only one of match or training can be provided.")
            if not match_id and not training_id:
                raise ValidationError("Either match or training must be provided.")

            # Ambil objek match/training jika ada
            match = (
                get_object_or_404(pertandingan, match=match_id) if match_id else None
            )
            training_instance = (
                get_object_or_404(training, training=training_id)
                if training_id
                else None
            )

            # Cek apakah kombinasi sudah ada
            already_exists = PlayerPerformance.objects.filter(
                player=player_obj,
                metric=metric,
                match=match,
                training=training_instance,
            ).exists()

            if already_exists:
                raise ValidationError(
                    "Performance with this player, metric, and match/training already exists."
                )

            # Buat instance baru
            performance = PlayerPerformance.objects.create(
                metric=metric,
                player=player_obj,
                value=value,
                match=match,
                training=training_instance,
            )

            return {
                "id": performance.player_performance,
                "metric_id": performance.metric.metric,
                "category_id": performance.metric.metric_category.metric_category,
                "player_id": performance.player.player,
                "value": performance.value,
            }

        except ValidationError as e:
            raise e

    @staticmethod
    def delete(performance_id):
        performance = PlayerPerformance.objects.filter(
            player_performance=performance_id
        ).first()
        if not performance:
            raise ValidationError("Player performance not found.")
        performance.delete()
        return {"message": "Player performance deleted successfully."}

    @staticmethod
    def group_by_metric(performances):
        grouped = defaultdict(list)

        for match in performances:
            for player in match["players"]:
                for metric in player["metrics"]:
                    grouped[metric["metric_name"]].append(
                        {
                            "player_name": player["player_name"],
                            "foto_profil": player["foto_profil"],
                            # "kewarganegaraan": player["kewarganegaraan"],
                            "value": metric["value"],
                        }
                    )

        return grouped
