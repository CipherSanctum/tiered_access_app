from django.contrib import admin
from .models import TieredAppCustomUser


# Register your models here.


@admin.register(TieredAppCustomUser)
class TieredAppCustomUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'tier_choice']
    list_filter = ['tier_choice']
    list_editable = ['tier_choice']
