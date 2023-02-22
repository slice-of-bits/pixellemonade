from django.urls import path
from .views import index_view, albums_index_view, album_new_view, album_detail_view


urlpatterns = [
    path('', index_view),
    path('albums/', albums_index_view, name='albums_index'),
    path('album/new/', album_new_view, name='album-create'),
    path('album/<slug:id>/', album_detail_view, name='album-detail'),
    # path('album/<id:id>/edit/'),
    #
    # path('photos/'),
    # path('photos/upload/'),
    # path('photo/<id:id>/'),
    # path('photo/<id:id>/edit'),
]
