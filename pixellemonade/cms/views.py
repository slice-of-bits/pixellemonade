from django.shortcuts import render

from pixellemonade.core.models import Album


def index_view(request):
    return render(request=request,
                  template_name='cms/base.html',
                  context={})


def albums_index_view(request):
    return render(request=request,
                  template_name='cms/albums/albums.html')


def album_new_view(request):
    return render(request=request,
                  template_name='cms/albums/new.html')


def album_detail_view(request, id):
    album = Album.objects.get(pk=id)
    return render(request=request,
                  template_name='cms/albums/album.html',
                  context={'album': album})


def tagger_view(request):
    return render(request=request,
                  template_name='cms/tagger.html')


def photos_list(request):
    return render(request=request,
                  template_name='cms/photos_list.html')