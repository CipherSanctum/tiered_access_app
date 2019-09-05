from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
import csv
import zipfile
from django.http import HttpResponse
from .models import TieredAppCustomUser
from forum_app.models import Reply


# Create your views here.
@login_required(login_url='/accounts/signup')
def home(request):
    return render(request, 'tiered_access_app/home.html')


@login_required(login_url='/accounts/signup')
def check_tier_level(request):
    current_user = request.user
    try:
        level = TieredAppCustomUser.objects.get(user=current_user)
        if level.tier_choice == 'tier3':
            return render(request, 'tiered_access_app/check_tier_level.html', {'level_3': 'You have access to LEVEL 3.', 'level': level})
        elif level.tier_choice == 'tier2':
            return render(request, 'tiered_access_app/check_tier_level.html', {'level_2': 'You have access to LEVEL 2.', 'level': level})
        elif level.tier_choice == 'tier1':
            return render(request, 'tiered_access_app/check_tier_level.html', {'level_1': 'You have access to LEVEL 1.', 'level': level})
    except ObjectDoesNotExist:
        pass
    return render(request, 'tiered_access_app/check_tier_level.html', {'no_access': 'You don\'t have access yet.'})


@login_required(login_url='/accounts/signup')
def little_csv(request):
    try:
        level = TieredAppCustomUser.objects.get(user=request.user.id)
        if (level.tier_choice == 'tier1') or (level.tier_choice == 'tier2') or (level.tier_choice == 'tier3'):
            response = HttpResponse(content_type='text/csv')
            # This HTTP header tells browser to treat it as a file that will be downloaded
            response['Content-Disposition'] = 'attachment; filename=forum-title-and-reply-dates-only-from-user-id-{}.csv'.format(request.user.id)
            replies = Reply.objects.filter(user=request.user.id)
            if replies:
                writer = csv.writer(response)   # create file
                writer.writerow(['Title', 'Created', 'Updated'])    # create first row / COLUMNS
                for reply in replies:
                    writer.writerow([reply.title, reply.created, reply.updated])     # create each rows contents
            else:
                response = HttpResponse('<h1>You never made any replies on the forum, so go make some now. There is a link 2 pages ago, and again on your dashboard.</h1>')
            return response
        else:
            return render(request, 'tiered_access_app/check_tier_level.html', {'no_access': 'You don\'t have access yet.'})
    except ObjectDoesNotExist:
        response = HttpResponse('<h1>You don\'t have access to this yet.</h1>')
    return response


@login_required(login_url='/accounts/signup')
def big_csv(request):
    try:
        level = TieredAppCustomUser.objects.get(user=request.user.id)
        if (level.tier_choice == 'tier2') or (level.tier_choice == 'tier3'):
            # give csv file with the body
            response = HttpResponse(content_type='text/csv')
            # This HTTP header tells browser to treat it as a file that will be downloaded
            response['Content-Disposition'] = 'attachment; filename=forum-all-reply-content-from-user-id-{}.csv'.format(request.user.id)
            replies = Reply.objects.filter(user=request.user.id)
            if replies:
                writer = csv.writer(response)   # create file
                writer.writerow(['Topic', 'User', 'Title', 'Body', 'Created', 'Updated', 'Active?']) # create first row / COLUMNS
                for reply in replies:
                    writer.writerow([reply.forum_topic, reply.user, reply.title, reply.body, reply.created, reply.updated, reply.active])     # create each rows contents
            else:
                response = HttpResponse('<h1>You never made any replies on the forum, so go make some now. There is a link 2 pages ago, and again on your dashboard.</h1>')
            return response
        else:
            return render(request, 'tiered_access_app/check_tier_level.html', {'no_access': 'You don\'t have access yet.'})
    except ObjectDoesNotExist:
        response = HttpResponse('<h1>You don\'t have access to this yet.</h1>')
    return response


@login_required(login_url='/accounts/signup')
def zip_file(request):
    try:
        level = TieredAppCustomUser.objects.get(user=request.user.id)
        if level.tier_choice == 'tier3':
            # give multi text file all in a zip file.
            response = HttpResponse(content_type='application/zip')
            zf = zipfile.ZipFile(response, 'w')
            replies = Reply.objects.filter(user=request.user.id)
            if replies:
                for reply in replies:
                    zf.writestr(str(reply.created.year) + '-' + str(reply.created.month) + '-' + str(reply.created.day) + '-' + reply.forum_topic.title + '-' + reply.title + '.txt', reply.body)
                response['Content-Disposition'] = 'attachment; filename=my-replies-as-zip.zip'
            else:
                response = HttpResponse('<h1>You never made any replies on the forum, so go make some now. There is a link 2 pages ago, and again on your dashboard.</h1>')
            return response
        else:
            return render(request, 'tiered_access_app/check_tier_level.html', {'no_access': 'You don\'t have access yet.'})
    except ObjectDoesNotExist:
        response = HttpResponse('<h1>You don\'t have access to this yet.</h1>')
    return response


@login_required(login_url='/accounts/signup')
def gain_access(request):
    current_user = request.user
    if request.method == 'POST':
        try:
            level = TieredAppCustomUser.objects.get(user=current_user)
            tier_level = request.POST.get('tier_level', False)
            if tier_level == '3':
                level.tier_choice = 'tier3'
                level.save()
                messages.success(request, 'Level 3 granted!')
                return redirect('tiered_access_app:home')
            elif tier_level == '2':
                level.tier_choice = 'tier2'
                level.save()
                messages.success(request, 'Level 2 granted!')
                return redirect('tiered_access_app:home')
            elif tier_level == '1':
                level.tier_choice = 'tier1'
                level.save()
                messages.success(request, 'Level 1 granted!')
                return redirect('tiered_access_app:home')
            elif tier_level == '0':
                level.tier_choice = 'none'
                level.save()
                messages.success(request, 'Reset')
                return redirect('tiered_access_app:home')
        except ObjectDoesNotExist:
            new_tiered_user = TieredAppCustomUser()
            new_tiered_user.user = current_user  # tier_choice is defaulted to 'tier1' upon creation
            new_tiered_user.save()
            messages.success(request, 'Level 1 enabled!')
            return redirect('tiered_access_app:home')
    return redirect('tiered_access_app:home')
