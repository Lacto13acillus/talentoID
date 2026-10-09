import logging
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)


def index_page(request):
    """Render main analysis web page."""
    return render(request, 'index.html')


def history_page(request):
    """Render history dashboard page."""
    return render(request, 'history.html')


def integrations_redirect(request):
    """Redirect /integrations to integration dashboard."""
    return redirect('/app/v2/integration/dashboard/')
