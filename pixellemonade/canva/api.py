from django.core.paginator import Paginator
from ninja import NinjaAPI

from pixellemonade.canva.models import CanvaUser
from pixellemonade.canva.schemas import PhotoCanvaSearchIn, PhotoCanvaOut, CanvaResourcesOut
from pixellemonade.core.models import Photo

api = NinjaAPI(urls_namespace='canva_api')


def canva_user_auth(request, body):
    try:
        CanvaUser.objects.get(canva_user_id=body.user)
    except CanvaUser.DoesNotExist:
        return False
    return True


@api.post("/content/resources/find", url_name='canva_find')
def canva_resources_find(request, body: PhotoCanvaSearchIn):
    if not canva_user_auth(request, body):
        return {"type": "ERROR", "errorCode": "CONFIGURATION_REQUIRED"}

    if body.query:
        photos = Photo.objects.search(body.query)
    else:
        photos = Photo.objects.all()

    page_nr = request.GET.get('page', 1)
    paginator = Paginator(photos, per_page=100)
    page = paginator.get_page(page_nr)

    response_json = {
        "type": "SUCCESS",
        "resources": [CanvaResourcesOut.from_orm(i).dict() for i in page]
    }

    if page.has_next():
        response_json['continuation'] = page.next_page_number()

    return response_json
