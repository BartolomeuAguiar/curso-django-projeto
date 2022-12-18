from django.contrib import admin

from authors.models import Profile

# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    ...
