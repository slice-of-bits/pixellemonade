from django_unicorn.components import UnicornView

from pixellemonade.canva.models import CanvaUser


class CanvaUsersView(UnicornView):
    users: CanvaUser = None

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)  # calling super is required
        self.users = CanvaUser.objects.all()
        
    def delete_user(self, pk):
        CanvaUser.objects.get(pk=pk).delete()
        self.users = CanvaUser.objects.all()



