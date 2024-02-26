from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import profile
from django.contrib.auth.decorators import login_required


@login_required(login_url='signin')
def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm password']

        if password == confirm_password:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Exist')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                login_user = auth.authenticate(username=username, password=password)
                auth.login(request, login_user)

                new_profile = profile(user=user, id_user=user.id, email=user.email)
                user.save()
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Password Does Not Match')
            return redirect('signup')

    return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'credential invalid')
            return redirect('signin')

    return render(request, 'signin.html')


def logout(request):
    auth.logout(request)
    return redirect('signin')


@login_required(login_url='signin')
def settings(request):
    user_profile = profile.objects.get(user=request.user)
    if request.method == 'POST':
        user_profile.profile_image = request.FILES.get('image')
        user_profile.bio = request.POST['bio']
        user_profile.email = request.POST['email']
        user_profile.location = request.POST['location']
        user_profile.save()

    return render(request, 'setting.html', {'user_profile': user_profile})
