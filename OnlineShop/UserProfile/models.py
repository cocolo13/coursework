from django.db import models
from django.contrib.auth.models import User
from django.db.models import CASCADE
from ProductFeed.models import *

from ProductFeed.models import Clothes


class Achievements(models.Model):
    description = models.CharField(max_length=500)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")

    def __str__(self):
        return self.description


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    gender = models.CharField(max_length=10, default="Мужской")
    achievements = models.ManyToManyField(Achievements)

    def __str__(self):
        return self.user.last_name

    @property
    def email(self):
        return self.user.email


class Baskets(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    feeds = models.ManyToManyField(Clothes)

    def __str__(self):
        return self.user.last_name
