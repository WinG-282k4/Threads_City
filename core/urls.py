"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie

def custom_404(request):
    return JsonResponse({
        "status": "error",
        "message": "Endpoint không tồn tại. Vui lòng kiểm tra lại URL."
    }, status=404)

@ensure_csrf_cookie
def get_csrf_token(request):
    """Get CSRF token from cookie or generate new one if not exists"""
    token = request.COOKIES.get('csrftoken')
    if not token:
        # If no token in cookie, generate new one
        token = get_token(request)
    return JsonResponse({
        'status': 'success',
        'data': {
            'csrfToken': token
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/csrf/', get_csrf_token, name='csrf_token'),  # Add CSRF endpoint
    path('api/', include('thread.urls')),
    path('api/auth/', include('accounts.urls')),
    re_path(r'^.*$', custom_404),  # Catch all URLs
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
