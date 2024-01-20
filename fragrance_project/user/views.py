import json
import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from .forms import (
    UserRegisterForm,
    UserUpdateForm,
    ProfileUpdateForm
)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # save the user
            username = form.cleaned_data.get('username')
            profile = user.profile
            profile.save()
            messages.success(request, f'Account created!')
            return redirect('login')
    else:
        form = UserRegisterForm()

    context = {'form': form}
    return render(request, 'user/register.html', context)



@login_required
def profile(request):
    context = {}
    profile = request.user.profile
    context['profile'] = profile
    return render(request, 'user/profile_detail.html', context)


@login_required
def profile_edit(request):
    context = {}

    if request.method == 'POST':
        # get path to old image
        dir = os.path.abspath(os.path.dirname(__name__))
        filename = [dir] + request.user.profile.image.url.split('/')
        old_image_url = os.path.join(*filename)

        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            # delete old image
            if os.path.isfile(old_image_url) and not old_image_url.endswith('default.jpg') and 'image' in request.FILES:
                os.remove(old_image_url)
            user_form.save()
            profile_form.save()
        else:
            print("\n\nUser form errors:")
            print(user_form.errors)
            print("profile:")
            print(profile_form.errors)
            print("\n\n")
        messages.success(request, f'Your account has been updated!')
        return redirect('profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        
    context['user_form'] = user_form
    context['profile_form'] = profile_form
    return render(request, 'user/profile.html', context)


def choose_account(request):
    return render(request, 'user/choose.html')

