from django.contrib import admin
from . models import profile, post, like_post, follows
# Register your models here.
admin.site.register(profile)
admin.site.register(post)
admin.site.register(like_post)
admin.site.register(follows)