from django.urls import path
from pixellemonade.canva.api import api
from pixellemonade.canva.views import canva_login_view

urlpatterns = [
    path('auth/login/', canva_login_view, name='canva_login'),
    # path('auth/logout/', ),
    path('api/', api.urls),
]
