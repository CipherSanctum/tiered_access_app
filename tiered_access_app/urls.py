from django.urls import path
from . import views


app_name = 'tiered_access_app'


urlpatterns = [
    # tiered_access_app/
    path('', views.home, name='home'),
    path('check_tier_level/', views.check_tier_level, name='check_tier_level'),
    path('check_tier_level/gain_access/', views.gain_access, name='gain_access'),
    path('special_file/little_csv/', views.little_csv, name='little_csv'),
    path('special_file/big_csv/', views.big_csv, name='big_csv'),
    path('special_file/zip_file/', views.zip_file, name='zip_file'),
]
