Why did I make this?

For a project I had to write a synchronization with flickr albums trough there api.
And not to speak bad of flickr but there api is not perfect and there prices keep increasing more and more.
So halfway through and after missing some features the idea came to my to make my own alternative.

The requirements I had in mind where:

- Use S3 for the original image files because then I can use something like backblaze b2 for the storage. 
Because the original images are not accessed that much and speed is less of a concern here.
- Generate small thumbnails of all the photo files and store them somewhere els with fast access times. Maybe even with CDN caching.
- Make it an option to install it standalone like a headless cms for images but also as a package for existing Django projects. The project will mosty be focused on the stand alone option.
- Have a great api and docs/openAPI spec
- Store all the Exif data from the images a specially the tags that images already have in the meta data.
- Use this opportunity to learn some new Django stuff (Django ninja, Django Unicorn)
- Photos always need to be in an album so the album can be used to store the images i a folder witht the album name on s3
- 

And some cool things if have a lot of time to spear:

- A print to order integration with something like [prodigi.com](https://www.prodigi.com/)
- View and download analytics
- AI based search tags
- Person detection and tagging