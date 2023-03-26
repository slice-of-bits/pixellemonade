from django.urls import path

urlpatterns = [
    path('photo/<slug:id>/<slug:size>',),
    path('photo/<slug:id>/<slug:size>/download/',),
]
