# Album
A album is a collection of photos. The album is also the folder where the images are stored on the s3 server. Do to this reason photos can be only in one album.

# Album group
THe albums can be in a group these groups can be used to group the albums for example by year of edition of your event. 

But they also can be used to mange the place of there the albums wil be shown. Api keys can be limmited by album groups. Albums can be in multiple groups at the same time.

# Photo
A Photo exists of the original image file, and 3 thumbnails in different sizes these thumbnails are can de used not to serve to big images.
Photo objects also store the EXIF data of the images this can be used

# Photo tag
Photos can be taged with simple tags these are mostly used for search. These can be things like: cat, dog, gras, flower. Tags can be extracted from the meta data so they can be taged in programs like Lightroom

# Photo proccessing
Photos need to be proccesed for a few reasons:
1. Generating the thumbnails
2. Extracting the exif data and store it a json in the database
3. Setting tags based on the tags in the meta info in the file
4. (planed) set the uploader based on the copyright info in the file
The proccessing can be done direct when uploaded, or later trough Celery as a background job to speed up the uplaod speed because the processing can take a few secconds.

# Credit holder
This is the person or organisation that made the picture and holds the rights and the credits. This