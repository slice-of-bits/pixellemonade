from ninja import Schema

class CanvaResourcesOut(Schema):
    id: str
    name: str
    contentType: str
    thumbnail: dict = None
    type: str = "IMAGE"
    url: str

    def resolve_name(self, obj):
        return obj.filename

    def resolve_contentType(self, obj):
        return "image/jpeg"

    def resolve_thumbnail(self, obj):
        return {"url": obj.medium_thumbnail.url}

    def resolve_url(self, obj):
        return obj.original_image.url


class PhotoCanvaOut(Schema):
    type: str = "SUCCESS",
    resources: CanvaResourcesOut = None
    continuation: int = None


class PhotoCanvaSearchIn(Schema):
    user: str
    brand: str
    label: str
    limit: int
    type: str
    locale: str
    query: str = None