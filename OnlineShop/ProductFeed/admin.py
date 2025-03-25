from django.contrib import admin
from .models import *
from UserProfile.models import *

admin.site.register(Clothes)
admin.site.register(Achievements)
admin.site.register(UserProfile)
admin.site.register(Sizes)
admin.site.register(Seasons)
admin.site.register(Styles)
admin.site.register(Subcategories)
admin.site.register(Countries)
# Register your models here.
