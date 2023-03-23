
# storages
Pixellemonade uses two divergent storages they booth are s3 based but are used for divergent things.

## Public
This is storage is some kind of cache it holds all the thumbnails this storage needs to be fast but holds a lot less data.
The data in this storage also could be rebuild in the case of data lost or migration.

## Private storage
This is the storage with the original image files are stored this storage


# thumbnail settings
There are 3 sizes of thumbnails by default these thumbnails are made by django image kit.
These settings can de overwritten like this:

```python
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFit

from pixellemonade.core.models import Photo, get_small_thumbs_path
from pixellemonade.core.storages import PublicStorage


class CustomPhotoClass(Photo):
    small_thumbnail = ProcessedImageField(upload_to=get_small_thumbs_path,
                                          processors=[ResizeToFit(300, 300)],
                                          format='PNG',
                                          options={'quality': 50},
                                          height_field='small_thumbnail_height',
                                          width_field='small_thumbnail_width',
                                          null=True,
                                          storage=PublicStorage())
```

## Small
This is mostly used for small previews in the cms and could be used for progressive image loading
### settings
File format: jpg
Size 500px on the longest size
Quality: 60%

## Medium
This is size is ment to be used for the overview pages of albums
### settings
File format: jpg
Size 800px on the longest size
Quality: 60%

## Big
This is ment for the full screen preview of images and could be used for most things
### settings
File format: jpg
Size 3000px on the longest size
Quality: 85%
