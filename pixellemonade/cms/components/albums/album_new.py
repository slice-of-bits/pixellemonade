from django_unicorn.components import UnicornView
from pixellemonade.core.models import AlbumGroup, Album
from django.shortcuts import redirect
from django.urls import reverse


class AlbumNewView(UnicornView):
    album_name = None
    album_groups = None
    new_group_name = None

    def groups(self):
        return AlbumGroup.objects.all()

    def add_new_group(self):
        AlbumGroup.objects.create(name=self.new_group_name)

    def save_new_album(self):
        a = Album.objects.create(name=self.album_name)
        if self.album_groups:
            a.groups.add(*self.album_groups)

        return redirect(reverse('albums_index'))
