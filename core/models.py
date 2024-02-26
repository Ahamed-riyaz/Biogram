from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.f

class profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField()
    location = models.TextField()
    email = models.EmailField(null=True)
    profile_image = models.ImageField(upload_to='profile_images', default='user-simple-flat-icon-illustration-vector.jpg')

    def __str__(self):
        return self.user.username

