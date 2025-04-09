from django.shortcuts import render, redirect
from ProductFeed.models import Clothes
from django.contrib.auth.models import User
from UserProfile.models import Achievements, UserProfile, Baskets


# Create your views here.


def profile_show(request):
    all_clothes = Clothes.objects.all().order_by('-by_count')
    return render(request, "UserProfile/profile.html", {"all_title": all_clothes})


def show_page_trash(request):
    all_clothes = Clothes.objects.all().order_by('-by_count')
    try:
        basket = Baskets.objects.get(user=request.user)
        basket_items = basket.feeds.all()
    except Exception:
        basket_items = []
    return render(request, "UserProfile/trash.html",
                  {"all_title": all_clothes,
                   "basket_feeds": basket_items})


def remove_from_basket(request):
    try:
        if request.method == 'POST':
            product = Clothes.objects.get(pk=request.POST.get('item_id'))
            basket = Baskets.objects.get(user=request.user)
            basket.feeds.remove(product)
    except Exception:
        pass
    return redirect('trash')


def show_page_like(request):
    all_clothes = Clothes.objects.all().order_by('-by_count')
    return render(request, "UserProfile/like.html",
                  {"all_title": all_clothes})


def show_page_achievements(request):
    user_achievements = UserProfile.objects.get(user=request.user.pk).achievements.all()
    other_achievements = Achievements.objects.exclude(id__in=user_achievements.values_list('id', flat=True))

    return render(request, "UserProfile/achievements.html",
                  {"achievements": user_achievements,
                   "other_achievements": other_achievements})


def show_page_reviews(request):
    return render(request, "UserProfile/reviews.html")


def show_page_my_data(request):
    return render(request, "UserProfile/myData.html")
