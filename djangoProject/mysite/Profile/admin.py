from django.contrib import admin

# Register your models here.
from .models import PersonalProfile, Item

class PProfile(admin.ModelAdmin):
    list_display = ["f_name","l_name"]
    class Meta:
        model = PersonalProfile



admin.site.register(PersonalProfile,PProfile)
admin.site.register(Item)