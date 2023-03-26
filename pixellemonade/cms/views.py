from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from pixellemonade.core.models import Album, Photo


@login_required
def index_view(request):
    return render(request=request,
                  template_name='cms/base.html',
                  context={})


@login_required
def albums_index_view(request):
    return render(request=request,
                  template_name='cms/albums/albums.html')


@login_required
def album_new_view(request):
    return render(request=request,
                  template_name='cms/albums/new.html')


@login_required
def album_detail_view(request, id):
    album = Album.objects.get(pk=id)
    return render(request=request,
                  template_name='cms/albums/album.html',
                  context={'album': album})


@login_required
def tagger_view(request):
    return render(request=request,
                  template_name='cms/tagger.html')


@login_required
def photos_list(request):
    return render(request=request,
                  template_name='cms/photos_list.html')


@login_required
def photo_details_view(request, id):
    return render(request=request,
                  template_name='cms/photo_details.html',
                  context={'photo': Photo.objects.get(pk=id)})


@login_required
def canva_users_list_view(request):
    return render(request=request,
                  template_name='cms/canva/users.html')