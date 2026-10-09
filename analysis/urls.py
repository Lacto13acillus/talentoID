from django.urls import path, re_path
from analysis.views import (
    page_views,
    heading_views,
    passing_views,
    upload_views,
    process_views,
    results_views,
    download_views,
    manual_count_views,
    history_views,
    footprint_views,
    total_result_views,
    player_result_views,
    youtube_views,
)

urlpatterns = [
    # Pages
    path('', page_views.index_page, name='analysis_index'),
    re_path(r'^history/?$', page_views.history_page, name='analysis_history'),
    re_path(r'^integrations/?$', page_views.integrations_redirect, name='analysis_integrations'),

    # Heading
    path('api/heading/test', heading_views.test, name='heading_test'),
    path('api/heading/upload', heading_views.upload, name='heading_upload'),
    path('api/heading/upload-url', heading_views.upload_url, name='heading_upload_url'),
    path('api/heading/process/<str:job_id>', heading_views.process, name='heading_process'),
    path('api/heading/count/<str:job_id>', heading_views.process, name='heading_count'),
    path('api/heading/results/<str:job_id>', heading_views.results, name='heading_results'),
    path('api/heading/download/<str:job_id>', heading_views.download, name='heading_download'),
    path('api/heading/preview/<str:job_id>', heading_views.preview, name='heading_preview'),

    # Passing
    path('api/passing/test', passing_views.test, name='passing_test'),
    path('api/passing/upload', passing_views.upload, name='passing_upload'),
    path('api/passing/upload-url', passing_views.upload_url, name='passing_upload_url'),
    path('api/passing/process/<str:job_id>', passing_views.process, name='passing_process'),
    path('api/passing/count/<str:job_id>', passing_views.process, name='passing_count'),
    path('api/passing/results/<str:job_id>', passing_views.results, name='passing_results'),
    path('api/passing/download/<str:job_id>', passing_views.download, name='passing_download'),
    path('api/passing/preview/<str:job_id>', passing_views.preview, name='passing_preview'),

    # Generic Upload
    path('api/upload/', upload_views.upload_video, name='upload_video'),

    # Generic Process
    path('api/process/<str:job_id>', process_views.start_processing, name='start_processing'),
    path('api/process/<str:job_id>/status', process_views.get_status, name='get_status'),

    # Generic Results
    path('api/results/<str:job_id>', results_views.get_results, name='get_results'),

    # Generic Download & Stream
    path('api/download/<str:job_id>/video', download_views.download_video, name='download_video'),
    path('api/download/<str:job_id>/stream', download_views.stream_video, name='stream_video'),
    path('api/download/<str:job_id>/info', download_views.get_video_info, name='get_video_info'),

    # Manual Count
    path('api/manual-count/test', manual_count_views.test, name='manual_count_test'),
    path('api/manual-count/upload', manual_count_views.upload, name='manual_count_upload'),
    path('api/manual-count/upload-url', manual_count_views.upload_url, name='manual_count_upload_url'),
    path('api/manual-count/submit', manual_count_views.submit, name='manual_count_submit'),
    path('api/manual-count/save', manual_count_views.submit, name='manual_count_save'),
    path('api/manual-count/preview/<str:job_id>', manual_count_views.preview, name='manual_count_preview'),

    # History API
    path('api/history/results', history_views.get_results_by_footprint, name='history_results'),
    path('api/history/results/<str:footprint_id>', history_views.get_results_by_footprint, name='history_results_detail'),
    path('api/history/summary', history_views.get_summary, name='history_summary'),
    path('api/history/table', history_views.get_table_data, name='history_table'),

    # Footprint API
    path('api/footprint/', footprint_views.get_footprints, name='footprint_list'),
    path('api/footprint/counted', footprint_views.get_counted_footprints, name='footprint_counted'),

    # Total Result API
    path('api/total-result/', total_result_views.list_results, name='total_result_list'),
    path('api/total-result/<str:result_id>', total_result_views.get_result, name='total_result_detail'),
    path('api/total-result/<str:result_id>/history', total_result_views.get_history, name='total_result_history'),
    path('api/total-result/<str:result_id>/edit', total_result_views.edit_result, name='total_result_edit'),

    # Player Result API
    path('api/player-result/', player_result_views.list_results, name='player_result_list'),
    path('api/player-result/by-total/<str:total_result_id>', player_result_views.get_by_total_result, name='player_result_by_total'),
    path('api/player-result/<str:result_id>', player_result_views.get_result, name='player_result_detail'),
    path('api/player-result/<str:result_id>/edit', player_result_views.edit_result, name='player_result_edit'),
    path('api/player-result/batch-edit', player_result_views.batch_edit, name='player_result_batch_edit'),
    path('api/player-result/batch-save', player_result_views.batch_save, name='player_result_batch_save'),

    # YouTube API
    path('api/youtube/auth-status', youtube_views.auth_status, name='youtube_auth_status'),
    path('api/youtube/auth', youtube_views.trigger_auth, name='youtube_auth'),
    path('api/youtube/oauth2callback', youtube_views.oauth2_callback, name='youtube_oauth2callback'),
    path('api/youtube/auth/callback', youtube_views.auth_callback_manual, name='youtube_auth_callback'),
    path('api/youtube/upload', youtube_views.upload_video, name='youtube_upload'),
    path('api/youtube/upload-status/<str:job_id>', youtube_views.upload_status, name='youtube_upload_status'),
]
