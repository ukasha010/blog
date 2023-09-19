from django.contrib import admin
from blog.models import *
# Register your models here.
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(comment)
admin.site.register(notification)