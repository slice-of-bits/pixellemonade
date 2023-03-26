from django.urls import path
from pixellemonade.prodigi.views import start_order_view

urlpatterns = [
    path('order/', start_order_view),
]
