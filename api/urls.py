from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.conf import settings

# === IMPORT VIEWS ===
from dashboard.views import activity_list_handler
from schedule.views import schedule_handler
from stadion.views import stadion_handler
from team.views import team_handler, total_team_handler
from status.views import status_handler
from pertandingan.views import pertandingan_handler, readiness_handler, total_handler
from TrainingCategory.views import trainingcategory_handler
from training.views import training_handler
from user.views import user_handler, login_handler, delete_account_handler
from group.views import group_handler
from message.views import message_handler
from notif.views import notif_handler
from PlayerSearch.views import player_search_handler
from analytics.views import analytics_handler
from player.views import player_handler, xendit_handler
from TeamReport.views import team_report_handler
from PlayerContact.views import player_contact_handler
from MedicalHistory.views import medical_history_handler
from PlayerDocument.views import player_document_handler
from ProfilCoach.views import profil_coach_handler
from iap.views import iap_handler
from stats.views import stats_handler
from medical.views import medical_handler
from PlayerUpdate.views import playerupdate_handler
from DeviceStats.views import devicestats_handler
from attendance.views import attendance_handler
from result.views import result_handler
from footprint.views import (
    footprint_category_list_handler,
    footprint_category_detail_handler,
    footprint_handler,
)
from formations.views import formation_handler
from LineUp.views import lineup_handler
from MatchFormation.views import matchformations_handler
from TrainingStats.views import trainingstats_handler
from TrainingFormation.views import trainingformation_handler
from MatchAttendance.views import match_attendance_handler
from PlayerActivity.views import player_activity_handler
from season.views import season_handler
from frequency.views import frequency_handler
from iaptraining.views import iaptraining_handler
from MatchAttendancePlayer.views import match_attendance_player_handler
from TrainingAttendancePlayer.views import training_attendance_player_handler
from MetricCategory.views import metric_category_handler
from Metric.views import metric_handler
from PlayerPerformance.views import player_performance_handler, player_standing_handler
from payments.views import get_payment_channels
from tournament.views.views import tournament_handler
from tournament.views.tournament_registration_view import (
    tournament_registration_handler,
)
from wilayah.views.wilayah_view import provinsi_handler, kabupaten_handler

API = "app/v2"

urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
    # 🔹 AUTH & USER
    re_path(rf"^{API}/auth/signin$", login_handler),
    re_path(rf"^{API}/users/remove-account$", delete_account_handler),
    re_path(rf"^{API}/users$", user_handler),
    # 🔹 REGION
    re_path(rf"^{API}/regions/provinces$", provinsi_handler),
    re_path(rf"^{API}/regions/cities$", kabupaten_handler),
    # 🔹 CLUB
    # re_path(rf"^{API}/clubs$", club_handler),
    # 🔹 ATHLETES
    re_path(rf"^{API}/athletes/search$", player_search_handler),
    re_path(rf"^{API}/athletes/contact-info$", player_contact_handler),
    re_path(rf"^{API}/athletes/medical-records$", medical_history_handler),
    re_path(rf"^{API}/athletes/documents$", player_document_handler),
    re_path(rf"^{API}/athletes/activities$", player_activity_handler),
    re_path(rf"^{API}/athletes/update$", playerupdate_handler),
    re_path(rf"^{API}/athletes/performance$", player_performance_handler),
    re_path(rf"^{API}/athletes$", player_handler),
    # 🔹 SQUADS
    re_path(rf"^{API}/squads/summary$", total_team_handler),
    re_path(rf"^{API}/squads/reports$", team_report_handler),
    re_path(rf"^{API}/squads$", team_handler),
    # 🔹 COACH
    re_path(rf"^{API}/coaches/profile$", profil_coach_handler),
    # 🔹 GAMES
    re_path(rf"^{API}/games/summary$", total_handler),
    re_path(rf"^{API}/games/readiness$", readiness_handler),
    re_path(rf"^{API}/games/stats$", stats_handler),
    re_path(rf"^{API}/games/attendance$", match_attendance_handler),
    re_path(rf"^{API}/games/lineup$", lineup_handler),
    re_path(rf"^{API}/games/formations$", matchformations_handler),
    re_path(rf"^{API}/games/attendance-players$", match_attendance_player_handler),
    re_path(rf"^{API}/games$", pertandingan_handler),
    # 🔹 SESSIONS
    re_path(rf"^{API}/sessions/categories$", trainingcategory_handler),
    re_path(rf"^{API}/sessions/stats$", trainingstats_handler),
    re_path(rf"^{API}/sessions/formations$", trainingformation_handler),
    re_path(
        rf"^{API}/sessions/attendance-players$", training_attendance_player_handler
    ),
    re_path(rf"^{API}/sessions$", training_handler),
    # 🔹 GENERAL
    re_path(rf"^{API}/schedule$", schedule_handler),
    re_path(rf"^{API}/status$", status_handler),
    re_path(rf"^{API}/groups$", group_handler),
    re_path(rf"^{API}/messages$", message_handler),
    re_path(rf"^{API}/notifications$", notif_handler),
    re_path(rf"^{API}/analytics$", analytics_handler),
    re_path(rf"^{API}/medical$", medical_handler),
    re_path(rf"^{API}/attendance$", attendance_handler),
    re_path(rf"^{API}/results$", result_handler),
    re_path(rf"^{API}/activity/footprint$", footprint_handler),
    re_path(rf"^{API}/activity/footprint/categories$", footprint_category_list_handler),
    re_path(
        rf"^{API}/activity/footprint/categories/<str:category>$",
        footprint_category_detail_handler,
    ),
    re_path(rf"^{API}/formations$", formation_handler),
    re_path(rf"^{API}/seasons$", season_handler),
    re_path(rf"^{API}/intensity$", frequency_handler),
    # 🔹 METRICS
    re_path(rf"^{API}/metrics/categories$", metric_category_handler),
    re_path(rf"^{API}/metrics$", metric_handler),
    # 🔹 DEVICE
    re_path(rf"^{API}/devices/stats$", devicestats_handler),
    # 🔹 PAYMENT
    re_path(rf"^{API}/billing/iap$", iap_handler),
    re_path(rf"^{API}/billing/iap-session$", iaptraining_handler),
    re_path(rf"^{API}/billing/channels$", get_payment_channels),
    # ❗ XENDIT (JANGAN DIUBAH)
    re_path(r"^api/xendit-callback$", xendit_handler),
    # 🔹 TOURNAMENT
    re_path(rf"^{API}/tournaments/registration$", tournament_registration_handler),
    re_path(rf"^{API}/tournaments$", tournament_handler),
    re_path(rf"^{API}/venues$", stadion_handler),
    re_path(rf"^{API}/standings$", player_standing_handler),
    # dashboard
    re_path(rf"^{API}/dashboard/activities$", activity_list_handler),
    # integrations
    re_path(rf"^{API}/integration/", include("integration.urls")),
    # analysis
    re_path(rf"^{API}/analysis/", include("analysis.urls")),
    path("", include("analysis.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

