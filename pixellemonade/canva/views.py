from django.contrib.auth.decorators import login_required
from django.http import HttpResponseServerError
from django.shortcuts import render, redirect

from pixellemonade.canva.models import CanvaUser


# Create your views here.
@login_required
def canva_login_view(request):
    canva_user_id = request.GET.get('user')

    # If the canva userid is not found in the query parms return a http500
    if not canva_user_id:
        return HttpResponseServerError()

    # Check if the user does not exists already this should not happen but you never know
    if CanvaUser.objects.filter(canva_user_id=canva_user_id).exists():
        return redirect(f"https://canva.com/apps/configured?success=true&state={request.GET.get('state')}")

    if request.method == 'POST':
        CanvaUser.objects.create(canva_user_id=canva_user_id, user_id=request.user.id)
        return redirect(f"https://canva.com/apps/configured?success=true&state={request.GET.get('state')}")

    return render(request=request,
                  template_name='canva/auth.html',
                  context={})