from django.contrib import admin

# Register your models here.
from .models import PersonalProfile, Item

admin.site.register(PersonalProfile)
admin.site.register(Item)