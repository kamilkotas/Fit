from django.contrib import admin
from .models import FoodItem, Profile

# Register your models here.

admin.site.register(FoodItem)
admin.site.register(Profile)