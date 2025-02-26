from django.db import models


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
    count_sizes = models.JSONField(default={"XS": 0,
                                            "S": 0,
                                            "M": 0,
                                            "L": 0,
                                            "XL": 0,
                                            "XXL": 0})
    gender = models.CharField(max_length=6, default="Male")
    count_in_stock = models.IntegerField(default=10)

    def __str__(self):
        return self.title
