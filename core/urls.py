from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name="index"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('logout', views.logout, name="logout"),
    path('settings', views.settings, name="settings"),
    path('upload', views.uploads, name="upload"),
    path('likepost', views.likepost, name="like_post"),
    path('profile/<username>/', views.profiles, name="user_profile"),
    path('follows', views.follow, name="follows")
]
