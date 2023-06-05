from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from pixellemonade.core.models import Album, Photo, Photographer


@login_required
def index_view(request):
    return render(request=request,
                  template_name='cms/base.html',
                  context={})


@login_required
def albums_index_view(request):
    return render(request=request,
                  template_name='cms/albums/albums.html')


@login_required
def album_new_view(request):
    return render(request=request,
                  template_name='cms/albums/new.html')


@login_required
def album_detail_view(request, id):
    album = Album.objects.get(pk=id)
    return render(request=request,
                  template_name='cms/albums/album.html',
                  context={'album': album})


@login_required
def tagger_view(request):
    return render(request=request,
                  template_name='cms/tagger.html')


@login_required
def photos_list(request):
    return render(request=request,
                  template_name='cms/photos_list.html')


@login_required
def photo_details_view(request, id):
    return render(request=request,
                  template_name='cms/photo_details.html',
                  context={'photo': Photo.objects.get(pk=id)})


@login_required
def canva_users_list_view(request):
    return render(request=request,
                  template_name='cms/canva/users.html')


@login_required
def shop_products_list_view(request):
    return render(request=request,
                  template_name='cms/shop/products.html')


@login_required
def shop_carts_list_view(request):
    return render(request=request,
                  template_name='cms/shop/carts.html')


@login_required
def shop_orders_list_view(request):
    return render(request=request,
                  template_name='cms/shop/orders.html')


@login_required
def shop_cart_details_view(request, id):
    return render(request=request,
                  template_name='cms/shop/cart.html',
                  context={'cart_id': id})

@login_required
def photographer_list_view(request):
    return render(request=request,
                  template_name='cms/photographer/photographers.html')


@login_required
def photographer_detail_view(request, id):
    return render(request=request,
                  template_name='cms/photographer/photographer.html',
                  context={'photographer': Photographer.objects.get(pk=id)})