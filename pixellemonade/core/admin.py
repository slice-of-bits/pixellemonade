from django.contrib import admin
from pixellemonade.core.tasks import process_upload
from pixellemonade.core.models import Album, Photo, PhotoTag, AlbumGroup


class AlbumAdmin(admin.ModelAdmin):
    list_filter = ['groups']

    class Meta:
        model = Album


@admin.action(description='Remake the thumbnails')
def generate_new_thumbs(modeladmin, request, queryset):
    for obj in queryset:
        process_upload.delay(obj.id)


class PhotoAdmin(admin.ModelAdmin):
    actions = [generate_new_thumbs]
    class Meta:
        model = Photo


class PhotoTagAdmin(admin.ModelAdmin):
    class Meta:
        model = PhotoTag


# Register your models here.
admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(PhotoTag, PhotoTagAdmin)
admin.site.register(AlbumGroup)