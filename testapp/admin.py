from django.contrib import admin
from .models import *
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['user_uid', 'date_joined', 'last_login', 'is_staff']

admin.site.register(User, UserAdmin)
admin.site.register(Post)
admin.site.register(Hashtag)
admin.site.register(Comment)
admin.site.register(PostLike)
admin.site.register(Scrap)