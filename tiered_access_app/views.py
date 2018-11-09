from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.utils.text import slugify
from .models import TieredAppUser


# Create your views here.
@login_required(login_url='/accounts/signup')
def home(request, special_message=None):
    return render(request, 'tiered_access_app/home.html', {'special_message': special_message})


@login_required(login_url='/accounts/signup')
def check_tier_level(request):
    current_user = request.user
    try:
        find_user = TieredAppUser.objects.get(user=current_user)
        # REALISTICALLY: For each level, you'd query database for a Model a User should get (RewardLevelOne, RewardLevelTwo, etc), get it, and
        # add that in the dictionary for each level depending on what they deserve, instead of adding a raw string value.
        if find_user.tier_choice == 'tier3':
            return render(request, 'tiered_access_app/check_tier_level.html', {'level_3': 'You have access to ALL LEVELS.'})
        elif find_user.tier_choice == 'tier2':
            return render(request, 'tiered_access_app/check_tier_level.html', {'level_2': 'You have access to level 2.'})
        elif find_user.tier_choice == 'tier1':
            return render(request, 'tiered_access_app/check_tier_level.html', {'level_1': 'You have access to level 1.'})
        elif find_user.tier_choice == 'none':
            return render(request, 'tiered_access_app/check_tier_level.html', {'enabled_no_access': 'You don\'t have access yet, but you have enabled it\'s use.'})
    except ObjectDoesNotExist:
        pass
    return render(request, 'tiered_access_app/check_tier_level.html', {'no_access': 'You don\'t have access to the content here yet.'})


@login_required(login_url='/accounts/signup')
def gain_access(request):
    current_user = request.user
    if request.method == 'POST':
        try:
            find_user = TieredAppUser.objects.get(user=current_user)
            tier_level = request.POST.get('tier_level', False)
            if tier_level == '3':
                find_user.tier_choice = 'tier3'
                find_user.save()
                return redirect('tiered_access_app:home_special_message', special_message=slugify('Tier 3 granted!'))
            elif tier_level == '2':
                find_user.tier_choice = 'tier2'
                find_user.save()
                return redirect('tiered_access_app:home_special_message', special_message=slugify('Tier 2 granted!'))
            elif tier_level == '1':
                find_user.tier_choice = 'tier1'
                find_user.save()
                return redirect('tiered_access_app:home_special_message', special_message=slugify('Tier 1 granted!'))
            elif tier_level == '0':
                find_user.tier_choice = 'none'
                find_user.save()
                return redirect('tiered_access_app:home_special_message', special_message=slugify('Usage enabled, reset.'))
        except ObjectDoesNotExist:
            new_tiered_user = TieredAppUser()
            new_tiered_user.user = current_user  # tier_choice is already defaulted to 'none'
            new_tiered_user.save()
            return redirect('tiered_access_app:home_special_message', special_message=slugify('Usage enabled, now click buttons to gain access'))
    return redirect('tiered_access_app:home_special_message', special_message=slugify('Usage already enabled '))
