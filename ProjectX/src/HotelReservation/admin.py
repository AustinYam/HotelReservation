from django.contrib import admin

# Register your models here.
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
	class Meta:
		model = UserProfile

admin.site.register(UserProfile, UserProfileAdmin)
