from django.contrib import admin
from .models import TieredAppUser


# Register your models here.


@admin.register(TieredAppUser)
class TieredAppUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'tier_choice']
    list_filter = ['tier_choice']
    list_editable = ['tier_choice']
