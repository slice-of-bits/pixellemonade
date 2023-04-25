from django.urls import path
from pixellemonade.core.views import view_photo, download_photo

urlpatterns = [
    path('photo/<slug:id>/<slug:size>/', view_photo, name='view_photo'),
    path('photo/<slug:id>/<slug:size>/download/', download_photo, name='download_photo'),
]
