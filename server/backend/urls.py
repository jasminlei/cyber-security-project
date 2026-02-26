"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


# FLAW 2 Demo: Test endpoint to demonstrate DEBUG=True vulnerability
# In real applications, this could be a health check endpoint or any endpoint where an error occurs
# When DEBUG=True, Django shows detailed error pages with sensitive data like database credentials, API keys, etc.
# Change DEBUG to true/false in settings.py
def test_error(request):
    # these variables simulate sensitive data that would be in a real application
    database_connection = (
        "postgresql://admin:MyS3cr3tP@ssw0rd@db.example.com:5432/production"
    )
    api_key = "sk_live_51234567890abcdef"

    # intentionally cause an error to demonstrate the vulnerability
    raise Exception("Connection failed: Unable to connect to database")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("users.urls")),
    path("api/items/", include("items.urls")),
    path("test-error/", test_error, name="test-error"),  # demo endpoint for FLAW 2
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
