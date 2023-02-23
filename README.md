# pixellemonade
The idea behind this project is to make system to store and manage photos on a central place.
And having a great api to serve the albums and images on multiple places easy.
All the images have basic exif metadata and tags which can be used to quickly find images for other uses.

Requirements:
- Use s3 for the image storage because it is cheap and easy to use
- Thumbnails need to be static generated for speed
- Use a background worker to make the thumbnails to keep the uploading fast
- Have an API and maybe widgets to include the albums on other sites/apps
- Offer a way to search through the back catalog of images by exif and tags

## Tech used
I saw this project as a way to learn some new cool things I have worked with django for a while but needed a 
opportunity to do something's with some cool stuff I heard a lot about.
- S3 as the storage backend for the photos
- Django as the backend and processing the images
- Celery for generating the thumbnails and extracting the exif data from the photo files
- Django unicorn for making an interactive dashboard
- Django ninja for the superfast api
- Uppy for the fileupload widget in the cms

## How to use
### Docker
Work in progres
### As a django package
Work in progres