from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()


class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField()
    location = models.TextField()
    email = models.EmailField(null=True)
    profile_image = models.ImageField(upload_to='profile_images', default='fav.png')

    def __str__(self):
        return self.user.username

    # In the following lines, we customize the display name of models for the Django admin interface.
    class Meta:
        verbose_name_plural = "Profile"


class post(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    caption = models.TextField()
    likes = models.IntegerField(default=0)
    image = models.ImageField(upload_to='post_images')
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user

    class Meta:
        verbose_name_plural = "post"


class like_post(models.Model):
    post_id = models.CharField(max_length=100)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "like_post"


class follows(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.follower

    class Meta:
        verbose_name_plural = "follows"
