from django.urls import path
from .views import *
from UserProfile.views import *
urlpatterns = [
    path("", show_base_page, name="feed"),
    path("clothes", show_clothes_page, name="clothes"),
    path("shoes", show_shoes_page, name="shoes"),
    path("accessories", show_accessories_page, name="accessories"),
    path("male", show_male_feeds, name="male"),
    path("female", show_female_feeds, name="female"),
    path("register", RegisterUser.as_view(), name="register"),
    path("login", LoginUser.as_view(), name="login"),
    path("logout", logout_user, name="logout"),
    path("profile", profile_show, name="profile"),
    path("profile/trash", show_page_trash, name="trash"),
    path("profile/like", show_page_like, name="like"),
    path("profile/achievements", show_page_achievements, name="achievements"),
    path("profile/reviews", show_page_reviews, name="reviews"),
    path("profile/myData", show_page_my_data, name="myData"),
    path("product/<int:product_id>/", show_product_info, name="product"),
]
