from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe
from django.contrib import messages



def change(modeladmin, request, queryset):
    # queryset.update(views = 1)
    print(str(request))
    print(str(queryset))
    user = User.objects.get(email = 'baek5@seunghyun.com')
    user.nickname = 'asdasd'
    user.save()
    messages.success(request, "배송상태로 변경")


class PhotoInline(admin.TabularInline):
    model = PostTag
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['pk','user_uid', 'joined_date', 'last_login', 'is_staff','is_active',]

# user = models.ForeignKey(User,on_delete=models.CASCADE, related_name= 'get_user') #get_post로 변경
# posts_image = models.ImageField(upload_to = 'post') #R
# back_image = models.ImageField(upload_to = 'postb') #R
# latitude = models.FloatField() #R
# longitude = models.FloatField() #R
# contents = models.TextField(verbose_name = '내용') #내용
# views = models.IntegerField(default = 0)
# created = models.DateTimeField(auto_now_add=True) #작성일
# modify_date = models.DateTimeField(null = True, blank = True) #게시글 수정일
# is_public = models.BooleanField(default = True) #공개여부
# report = models.BooleanField(default = False) #신고여부
# report_date = models.DateTimeField(null = True, blank = True) #신고 날짜
# problem = models.BooleanField(default = False)
# is_active = models.BooleanField(default = True)
# hashtag = models.ManyToManyField('HashTag', through='PostTag',related_name='get_hashtag')
# like_user = models.ManyToManyField('User', through = 'PostLike',related_name= 'get_like')
# comment = models.ManyToManyField('User', through='Comment',related_name='get_comment')
# scrap_users = models.ManyToManyField('User', through = 'Scrapt',related_name= 'get_scrap')
class PostsAdmin(admin.ModelAdmin):
    list_display = ['image_tag','pk', 'contents', 'views','problem', 'is_active']
    list_display_links = ['pk', 'contents', 'views', 'problem', 'is_active']
    list_filter = ['problem','contents']
    search_fields = ['report']
    date_hierarchy = 'created'
    readonly_fields = ['user', 'posts_image', 'back_image', 'latitude', 'longitude', 'contents', 'modify_date']
    actions = (change,)

    # inlines = [
    #     PhotoInline,
    # ]
    # def get_name(self, obj):
    #     print(str(obj.hashtag.))
    #     return obj.hashtag.name
    # # get_name.admin_order_field  = 'author'  #Allows column order sorting
    # # get_name.short_description = 'Author Name'  #Renames column head



class ReportAdmin(admin.ModelAdmin):
    list_display = ['image_post','reporter', 'post_owner', 'comment_owner', 'post', 'comment','post_caption','comment_contents','reason','detail']
    # list_display_links = ['pk', 'contents', 'views', 'problem', 'is_active']
    list_filter = ['reason']
    search_fields = ['post_owner', 'comment_owner', 'post_owner', 'detail', 'post_caption','comment_contents' ]
    date_hierarchy = 'created_date'
    # readonly_fields = ['user', 'posts_image', 'back_image', 'latitude', 'longitude', 'contents', 'modify_date']
    actions = (change,)

    # def change(modeladmin, request, queryset):
    #     # queryset.update(views = 1)
    #     print(str(request))
    #     print(str(queryset))
    #     user = User.objects.get(email = 'baek5@seunghyun.com')
    #     user.nickname = 'asdasd'
    #     user.save()
    #     messages.success(request, "배송상태로 변경")



admin.site.register(User, UserAdmin)
# admin.site.register(UserData)
admin.site.register(Post,PostsAdmin)
admin.site.register(HashTag)
admin.site.register(PostTag)
admin.site.register(Comment)
admin.site.register(PostLike)
admin.site.register(Scrapt)
admin.site.register(Report,ReportAdmin)
