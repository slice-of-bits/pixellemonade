from ninja import NinjaAPI

from pixellemonade.canva.models import CanvaUser
from pixellemonade.canva.schemas import PhotoCanvaSearchIn, PhotoCanvaOut
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

    photos = Photo.objects.all()

    if body.query:
        photos = photos.filter(tags__name__contains=body.query).distinct('pk')

    response_json = {
        "type": "SUCCESS",
        "resources": [PhotoCanvaOut.from_orm(i).dict() for i in photos]
    }

    return response_json
