from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework.reverse import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import logout
from .forms import RegisterUserForm, LoginUserForm, AddToBasketForm
from .models import Clothes, Sizes, Brands
from UserProfile.models import UserProfile, Achievements
from django.contrib.auth.models import User
from ML.views import preprocessing
from UserProfile.models import *


def show_base_page(request):
    all_clothes = Clothes.objects.all().order_by('-by_count')
    only_clothes = Clothes.objects.filter(category="Одежда").order_by('?')[:30]
    only_shoes = Clothes.objects.filter(category="Обувь").order_by('?')[:30][:30]
    only_accessories = Clothes.objects.filter(category="Аксессуары").order_by('?')[:30][:30]
    all_brand = Brands.objects.all()
    return render(request, "ProductFeed/base.html",
                  {"all_title": all_clothes,
                   "all_clothes": only_clothes,
                   "all_shoes": only_shoes,
                   "all_accessories": only_accessories,
                   "brand": all_brand})


def show_clothes_page(request):
    only_clothes = Clothes.objects.filter(category="Одежда").order_by('?')
    all_brand = Brands.objects.all()
    return render(request, "ProductFeed/clothes.html",
                  {"all_clothes": only_clothes,
                   "brand": all_brand})


def show_shoes_page(request):
    only_shoes = Clothes.objects.filter(category="Обувь").order_by('?')
    all_brand = Brands.objects.all()
    return render(request, "ProductFeed/shoes.html",
                  {"all_shoes": only_shoes,
                   "brand": all_brand})


def show_accessories_page(request):
    only_accessories = Clothes.objects.filter(category="Аксессуары").order_by('?')
    all_brand = Brands.objects.all()
    return render(request, "ProductFeed/accessories.html",
                  {"all_accessories": only_accessories,
                   "brand": all_brand})


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = "ProductFeed/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save()
        try:
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            user_profile = UserProfile.objects.create(user=user)
        try:
            achievement = Achievements.objects.get(pk=5)
            user_profile.achievements.add(achievement)
        except Achievements.DoesNotExist:
            print("Achievements with id 5 does not exist")
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "ProductFeed/login.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))


def logout_user(request):
    logout(request)
    return redirect('login')


def rec_feed(feed_id):
    feed = Clothes.objects.get(pk=feed_id)
    g = feed.gender
    all_feed = Clothes.objects.exclude(pk=feed_id).filter(gender=g)
    return all_feed


def show_product_info(request, product_id):
    current_product = Clothes.objects.filter(pk=product_id)
    all_clothes = Clothes.objects.all().order_by('-by_count')
    sizes = Clothes.objects.get(pk=product_id).size.all()
    rec_pk = preprocessing(feed_id=product_id)
    rec = Clothes.objects.filter(pk__in=rec_pk)
    brand = Clothes.objects.get(pk=product_id).brand.all()[0]
    try:
        if request.method == 'POST':
            form = AddToBasketForm(request.POST)
            if form.is_valid():
                basket, created = Baskets.objects.get_or_create(user=request.user)
                product = Clothes.objects.get(pk=product_id)
                basket.feeds.add(product)
                return redirect("product", product_id=product_id)
        else:
            form = AddToBasketForm()
    except:
        pass

    return render(request, "ProductFeed/product.html",
                  {"product": current_product,
                   "all_title": all_clothes,
                   "sizes": sizes,
                   "rec_feed": rec,
                   "brand": brand,
                   "form": form})


def show_male_feeds(request):
    male_feeds = Clothes.objects.filter(gender="Male").order_by('?')
    all_brand = Brands.objects.all()
    return render(request, "ProductFeed/MaleFeeds.html",
                  {"feeds": male_feeds,
                   "brand": all_brand})


def show_female_feeds(request):
    female_feeds = Clothes.objects.filter(gender="Female").order_by('?')
    all_brand = Brands.objects.all()
    return render(request, "ProductFeed/FemaleFeeds.html",
                  {"feeds": female_feeds,
                   "brand": all_brand})


def show_brand(request, brand_id):
    current_brand = Brands.objects.get(pk=brand_id)
    feeds_clothes = Clothes.objects.filter(brand=brand_id)

    return render(request, "ProductFeed/brand.html",
                  {"all_feeds": feeds_clothes,
                   "brand": current_brand})


def show_premium_feeds(request):
    premium_feeds = Clothes.objects.filter(is_premium=True)
    return render(request, "ProductFeed/premium_feeds.html",
                  {"premium_feeds": premium_feeds})