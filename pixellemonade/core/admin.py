from django.contrib import admin

from pixellemonade.core.models import Album, Photo, PhotoTag


class AlbumAdmin(admin.ModelAdmin):
    list_filter = ['groups']

    class Meta:
        model = Album


class PhotoAdmin(admin.ModelAdmin):

    class Meta:
        model = Photo


class PhotoTagAdmin(admin.ModelAdmin):
    class Meta:
        model = PhotoTag


# Register your models here.
admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(PhotoTag, PhotoTagAdmin)