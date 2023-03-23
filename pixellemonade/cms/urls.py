from django.urls import path
from .views import index_view, albums_index_view, album_new_view, album_detail_view, tagger_view, photos_list, \
    photo_details_view, canva_users_list_view


urlpatterns = [
    path('', photos_list),
    path('albums/', albums_index_view, name='albums_index'),
    path('album/new/', album_new_view, name='album_create'),
    path('album/<slug:id>/', album_detail_view, name='album_detail'),
    # path('album/<id:id>/edit/'),
    #
    path('photos/', photos_list, name='photos_list'),
    # path('photos/upload/'),
    path('photo/<slug:id>/', photo_details_view, name='photo_detail'),
    # path('photo/<id:id>/edit'),

    path('tagger/', tagger_view, name='tagger'),
    path('canva_users/', canva_users_list_view, name='canva_user_list')
]
