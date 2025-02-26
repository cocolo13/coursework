from django.http import HttpResponse
from django.shortcuts import render
from .models import Clothes


# Create your views here.

def show_base_page(request):
    all_clothes = Clothes.objects.all().order_by('-by_count')
    only_clothes = Clothes.objects.filter(category="Одежда").order_by('?')[:30]
    only_shoes = Clothes.objects.filter(category="Обувь").order_by('?')[:30][:30]
    only_accessories = Clothes.objects.filter(category="Аксессуары").order_by('?')[:30][:30]
    return render(request, "ProductFeed/base.html",
                  {"all_title": all_clothes,
                   "all_clothes": only_clothes,
                   "all_shoes": only_shoes,
                   "all_accessories": only_accessories})


def show_clothes_page(request):
    only_clothes = Clothes.objects.filter(category="Одежда").order_by('?')
    return render(request, "ProductFeed/clothes.html",
                  {"all_clothes": only_clothes})


def show_shoes_page(request):
    only_shoes = Clothes.objects.filter(category="Обувь").order_by('?')
    return render(request, "ProductFeed/shoes.html",
                  {"all_shoes": only_shoes})


def show_accessories_page(request):
    only_accessories = Clothes.objects.filter(category="Аксессуары").order_by('?')
    return render(request, "ProductFeed/accessories.html",
                  {"all_accessories": only_accessories})
