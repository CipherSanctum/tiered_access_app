from django.urls import path
from . import views


app_name = 'tiered_access_app'


urlpatterns = [
    # tiered_access_app/
    path('', views.home, name='home'),
    path('check_tier_level/', views.check_tier_level, name='check_tier_level'),
    path('check_tier_level/gain_access/', views.gain_access, name='gain_access'),
    path('<slug:special_message>/', views.home, name='home_special_message'),
]
