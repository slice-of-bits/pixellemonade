from django.contrib import admin
from pixellemonade.core.tasks import process_upload
from pixellemonade.core.models import Album, Photo, PhotoTag, AlbumGroup


class AlbumAdmin(admin.ModelAdmin):
    list_filter = ['groups']

    class Meta:
        model = Album


@admin.action(description='Reprocess files using Celery')
def reprocess_with_celery(modeladmin, request, queryset):
    for obj in queryset:
        process_upload.delay(obj.id)


@admin.action(description='Reprocess files using Direct')
def reprocess_local(modeladmin, request, queryset):
    for obj in queryset:
        process_upload(obj.id)


class PhotoAdmin(admin.ModelAdmin):
    actions = [reprocess_with_celery, reprocess_local]
    list_display = ['pk', 'original_image', 'in_album', 'uploaded_at', 'exif_shot_date_time', 'owner']
    list_filter = ['in_album', 'owner']

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