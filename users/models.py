from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    auth_token_admin = models.CharField(max_length=100)
    is_admin_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username