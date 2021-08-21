from django.contrib.auth.models import User
from django.db import models


class Twitte(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.CharField(max_length=140, null=True, blank=True)
    created_ts = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    twitte = models.ForeignKey(Twitte, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username + "--------" +self.twitte.text