from django.http import HttpResponse
from django.shortcuts import render

from pixellemonade.core.models import Photo


# Create your views here.
def start_order_view(request):
    photo_ids = request.GET.get('ids')
    if not photo_ids:
        return HttpResponse(status=500, details="No photo ids found")

    return render(request=request,
                  template_name='prodigi/order.html')