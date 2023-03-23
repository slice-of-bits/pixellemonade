from django.contrib import admin

from pixellemonade.canva.models import CanvaUser


class CanvaUserAdmin(admin.ModelAdmin):
    class Meta:
        model = CanvaUser

    list_display = ['user', 'canva_user_id', 'added_on']


admin.site.register(CanvaUser, CanvaUserAdmin)