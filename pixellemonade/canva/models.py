from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.


class CanvaUser(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    canva_user_id = models.CharField(unique=True, db_index=True, max_length=50)
    added_on = models.DateTimeField(auto_now_add=True)
