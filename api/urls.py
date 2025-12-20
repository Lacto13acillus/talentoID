"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import re_path
from django.conf.urls.static import static
from django.conf import settings
from schedule.views import schedule_handler
from team.views import team_handler, total_team_handler
from stadion.views import stadion_handler
from status.views import status_handler
from pertandingan.views import pertandingan_handler, readiness_handler
from TrainingCategory.views import trainingcategory_handler
from training.views import training_handler
from user.views import user_handler, login_handler
from group.views import group_handler
from message.views import message_handler
from notif.views import notif_handler
from PlayerSearch.views import player_search_handler
from analytics.views import analytics_handler
from player.views import player_handler
from TeamReport.views import team_report_handler
from PlayerPerform.views import player_perform_handler
from PlayerContact.views import player_contact_handler
from MedicalHistory.views import medical_history_handler
from PlayerDocument.views import player_document_handler
from ProfilCoach.views import profil_coach_handler
from iap.views import iap_handler
from stats.views import stats_handler
from session.views import session_handler
from medical.views import medical_handler
from PlayerUpdate.views import playerupdate_handler
from DeviceStats.views import devicestats_handler
from attendance.views import attendance_handler
from result.views import result_handler
from footprint.views import footprint_handler
from formations.views import formation_handler
from pertandingan.views import total_handler
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
from club.views import club_handler
from MetricCategory.views import metric_category_handler
from Metric.views import metric_handler
from PlayerPerformance.views import player_performance_handler
from player.views import xendit_handler
from user.views import delete_account_handler

urlpatterns = [
    re_path("admin/", admin.site.urls),
    re_path("api/schedule", schedule_handler),
    re_path("api/team", team_handler),
    re_path("api/totalteam", total_team_handler),
    re_path("api/stadion", stadion_handler),
    re_path("api/status", status_handler),
    re_path("api/pertandingan", pertandingan_handler),
    re_path("api/readiness", readiness_handler),
    re_path("api/total", total_handler),
    re_path("api/TrainingCategory", trainingcategory_handler),
    re_path("api/training", training_handler),
    re_path("api/user/delete", delete_account_handler),
    re_path("api/user", user_handler),
    re_path("api/login", login_handler),
    re_path("api/group", group_handler),
    re_path("api/message", message_handler),
    re_path("api/notif", notif_handler),
    re_path("api/PlayerSearch", player_search_handler),
    re_path("api/analytics", analytics_handler),
    re_path(r"^api/player$", player_handler),
    re_path("api/TeamReport", team_report_handler),
    re_path("api/PlayerPerform", player_perform_handler),
    re_path("api/PlayerContact", player_contact_handler),
    re_path("api/MedicalHistory", medical_history_handler),
    re_path("api/PlayerDocument", player_document_handler),
    re_path("api/ProfilCoach", profil_coach_handler),
    re_path(r"^api/iap$", iap_handler),
    re_path("api/stats", stats_handler),
    re_path("api/session", session_handler),
    re_path("api/medical", medical_handler),
    re_path("api/PlayerUpdate", playerupdate_handler),
    re_path("api/DeviceStats", devicestats_handler),
    re_path("api/attendance", attendance_handler),
    re_path("api/result", result_handler),
    re_path("api/footprint", footprint_handler),
    re_path("api/formations", formation_handler),
    re_path("api/LineUp", lineup_handler),
    re_path("api/MatchFormation", matchformations_handler),
    re_path("api/TrainingStats", trainingstats_handler),
    re_path("api/TrainingFormation", trainingformation_handler),
    re_path(r"^api/MatchAttendance$", match_attendance_handler),
    re_path("api/PlayerActivity", player_activity_handler),
    re_path("api/PlayerActivity", player_activity_handler),
    re_path("api/season", season_handler),
    re_path("api/frequency", frequency_handler),
    re_path(r"^api/iaptraining$", iaptraining_handler),
    re_path(r"^api/MatchAttendancePlayer$", match_attendance_player_handler),
    re_path("api/TrainingAttendancePlayer", training_attendance_player_handler),
    re_path("api/club", club_handler),
    re_path("api/metric-category", metric_category_handler),
    re_path("api/metric", metric_handler),
    re_path(r"^api/player-performance$", player_performance_handler),
    re_path(r"^api/xendit-callback$", xendit_handler),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
