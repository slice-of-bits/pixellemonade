"""
pixellemonade URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from pixellemonade.api.api import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
    path('cms/', include('pixellemonade.cms.urls')),
    path("unicorn/", include("django_unicorn.urls")),
]
