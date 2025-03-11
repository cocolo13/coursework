from django.contrib import admin
from .models import *
from UserProfile.models import *

admin.site.register(Clothes)
admin.site.register(Achievements)
admin.site.register(UserProfile)
admin.site.register(Sizes)
# Register your models here.
