from django.db import models
from user_agents import parse


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
        print(ip)
    else:
        ip = request.META.get('REMOTE_ADDR')
        print(ip)
    return ip


class BasicAnalytics(models.Model):
    from_ip = models.GenericIPAddressField()
    session = models.CharField(max_length=32, null=True)
    of_album = models.ForeignKey('core.Album', on_delete=models.CASCADE,)
    photo = models.ForeignKey('core.Photo', on_delete=models.CASCADE,)
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

    def process_request(self, request):
        self.from_ip = get_client_ip(request)
        self.browser = request.META['HTTP_USER_AGENT']
        self.session = request.session.session_key
        user_agent = parse(request.META.get('HTTP_USER_AGENT'))
        self.user_agent_browser_family = user_agent.browser.family
        self.user_agent_browser_version = user_agent.browser.version_string

        self.user_agent_os_family = user_agent.os.family
        self.user_agent_os_version = user_agent.os.version_string

        self.user_agent_device_family = user_agent.device.family
        self.user_agent_device_brand = user_agent.device.brand
        self.user_agent_device_model = user_agent.device.model

    class Meta:
        abstract = True


class PhotoView(BasicAnalytics):
    pass


class PhotoDownload(BasicAnalytics):
    pass
