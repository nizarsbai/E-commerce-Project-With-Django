from django.contrib import admin

# Register your models here.

from UserApp.models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
	list_display=['user','country']
	list_filter=['user',]


admin.site.register(UserProfile,UserProfileAdmin)