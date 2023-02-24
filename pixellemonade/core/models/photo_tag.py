from django.db import models
from django.contrib.auth import get_user_model


class LowerCaseField(models.CharField):
    def get_prep_value(self, value):
        return str(value).lower()


class PhotoTag(models.Model):
    name = LowerCaseField(max_length=128)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), null=True, blank=False, on_delete=models.SET_NULL)