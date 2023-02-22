from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'hashid_field.BigHashidAutoField'
    name = 'pixellemonade.core'
