from django.db import models
from django.urls import reverse


# Create your models here.

class Clothes(models.Model):
    title = models.CharField(max_length=255)
    cost = models.IntegerField()
    category = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")
    brand = models.CharField(max_length=255, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    by_count = models.IntegerField(default=0)
    is_premium = models.BooleanField(null=True)
    gender = models.CharField(max_length=6, default="Male")
    count_in_stock = models.IntegerField(default=10)
    size = models.ManyToManyField('Sizes')
    season = models.ManyToManyField('Seasons')
    style = models.ManyToManyField("Styles")
    subcategory = models.ManyToManyField("Subcategories")
    country = models.ManyToManyField("Countries")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product', kwargs={'product_id': self.pk})


class Sizes(models.Model):
    size = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.size


class Seasons(models.Model):
    season = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.season


class Styles(models.Model):
    style = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.style


class Subcategories(models.Model):
    subcategory = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.subcategory


class Countries(models.Model):
    country = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.country


class Brands(models.Model):
    brand = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.brand
