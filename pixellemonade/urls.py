"""
pixellemonade URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from pixellemonade.pixellemonade_api.api import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pixellemonade.core.urls')),
    path('api/', api.urls),
    path('cms/', include('pixellemonade.pixellemonade_cms.urls')),
    path('canva/', include('pixellemonade.canva.urls')),
    path("unicorn/", include("django_unicorn.urls")),
    path('__debug__/', include('debug_toolbar.urls')),
]
