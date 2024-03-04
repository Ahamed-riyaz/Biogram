from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User, auth
from .models import profile, post, like_post, follows
from django.contrib.auth.decorators import login_required


# The @login_required decorator ensures that only authenticated users can access this view.
# If the user is not authenticated, they will be redirected to the 'signin' page for login.

@login_required(login_url='signin')
def index(request):
    user_profile = profile.objects.get(user=request.user)
    # get_profile = profile.objects.get(user=user_profile)
    posts = post.objects.all()
    # print(posts)
    profile_image = []
    for i in posts:
        user_id = User.objects.get(username=i.user).id
        profile_user = profile.objects.get(user=user_id).profile_image
        # print(profile_user.profile_image)
        profile_image.append(profile_user)
    # print(posts, profile_image)
    return render(request, 'index.html',
                  {'user_profile': user_profile, 'posts': zip(posts, profile_image)})


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


@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')


@login_required(login_url='signin')
def settings(request):
    user_profile = profile.objects.get(user=request.user)
    if request.method == 'POST':
        bio = request.POST['bio']
        email = request.POST['email']
        location = request.POST['location']

        if request.FILES.get('image'):
            user_profile.profile_image = request.FILES.get('image')

        user_profile.bio = bio
        user_profile.email = email
        user_profile.location = location
        user_profile.save()

    return render(request, 'setting.html', {'user_profile': user_profile})


@login_required(login_url='signin')
def uploads(request):
    if request.method == 'POST':
        user = request.user.username
        caption = request.POST['caption']
        image = request.FILES.get('post_image')

        new_post = post(user=user, caption=caption, image=image)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')


@login_required(login_url='signin')
def likepost(request):
    if request.user.is_authenticated:
        username = request.user.username
        post_id = request.GET.get('post_id')

        Post = post.objects.get(user_id=post_id)
        like_filter = like_post.objects.filter(post_id=post_id, username=username)

        if not like_filter.exists():
            new_like = like_post(post_id=post_id, username=username)
            new_like.save()
            Post.likes += 1
            Post.save()
            return redirect('/')
        else:
            like_filter.delete()
            Post.likes = Post.likes - 1
            Post.save()
            return redirect('/')


@login_required(login_url='signin')
def profiles(request, username):
    # print(username)
    user_profile = profile.objects.get(user__username=username)
    posts = post.objects.filter(user=username)
    length_of_posts = len(posts)
    # print(user_profile.user)
    # print(user_profile.profile_image)
    follow_check = follows.objects.filter(follower=request.user.username, user=username).first()
    user_follower = len(follows.objects.filter(user=request.user.username))
    user_following = len(follows.objects.filter(follower=request.user.username))

    if follow_check:
        button = "UnFollow"
    else:
        button = "Follow"
    context = {
        'user_profile': user_profile,
        'length_of_posts': length_of_posts,
        'posts': posts,
        'button': button,
        'user_follower': user_follower,
        'user_following': user_following,
        'current_user': request.user.username
    }
    return render(request, 'profile.html', {'user_profile': context})


@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        # current user want to follow that user so current user is a follower
        follower = request.user.username
        # print("sdfg", follower)
        user = request.POST['user_profile']
        # print(user)
        is_following = follows.objects.filter(follower=follower, user=user).first()
        if is_following:
            is_following.delete()
            return redirect(reverse('user_profile', args=[user]))
        else:
            create_follow = follows(follower=follower, user=user)
            create_follow.save()
            # Use reverse to dynamically generate the URL for the user's profile.
            # this will check the url named user_profile
            return redirect(reverse('user_profile', args=[user]))
