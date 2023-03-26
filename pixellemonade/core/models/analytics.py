from django.db import models


class BasicAnalytics(models.Model):
    from_ip = models.GenericIPAddressField()
    of_album = models.ForeignKey('core.Album', on_delete=models.CASCADE)
    photo = models.ForeignKey('core.Photo', on_delete=models.CASCADE)
    photo_size = models.CharField(max_length=3,
                                  choices=[('sm', 'small'), ('mid', 'medium'), ('big', 'big'), ('ori', 'original')])
    browser = models.CharField(max_length=128)
    datetime = models.DateTimeField(auto_now_add=True)

    user_agent_browser_family = models.CharField(max_length=32, null=True)
    user_agent_browser_version = models.CharField(max_length=8, null=True)

    user_agent_os_family = models.CharField(max_length=32, null=True)
    user_agent_os_version = models.CharField(max_length=8, null=True)

    user_agent_device_family = models.CharField(max_length=32, null=True)
    user_agent_device_brand = models.CharField(max_length=32, null=True)
    user_agent_device_model = models.CharField(max_length=32, null=True)

    class Meta:
        abstract = True


class PhotoView(BasicAnalytics):
    pass


class PhotoDownload(BasicAnalytics):
    pass
