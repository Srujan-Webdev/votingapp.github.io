from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Polls_Create(models.Model):
    poll_name = models.TextField(max_length=50)
    option_one = models.CharField(max_length=20)
    option_two = models.CharField(max_length=20)
    option_three = models.CharField(max_length=20)
    option_one_count = models.IntegerField(default=0)
    option_two_count = models.IntegerField(default=0)
    option_three_count = models.IntegerField(default=0)

    voted = models.BooleanField(default=False)

    is_current_user_voted = models.BooleanField(default=False)
    is_poll_created_user_voted = models.BooleanField(default=False)

    user = models.ForeignKey(User, null=True, default=True, on_delete=models.CASCADE)

    # voted_list3 = models.IntegerField(default=0)

    # print("voted_list3: ",voted_list3)

    #voted_info = models.TextField(default=0,max_length=500)

    def total(self):
        return self.option_one_count+self.option_two_count+self.option_three_count

    class Meta:
        ordering = ['-poll_name']

    def __str__(self):
        return self.poll_name
