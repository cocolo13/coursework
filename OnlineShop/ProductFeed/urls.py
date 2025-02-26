from django.urls import path
from .views import *

urlpatterns = [
    path("feed", show_base_page, name="feed"),
    path("clothes", show_clothes_page, name="clothes"),
    path("shoes", show_shoes_page, name="shoes"),
    path("accessories", show_accessories_page, name="accessories")
]