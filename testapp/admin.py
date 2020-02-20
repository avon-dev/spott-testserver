from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe
from django.contrib import messages

detail_reason = [\
                "사진의 위치정보가 정확하지 않습니다. 다시 위치를 확인하여 업로드 해 주시길 바랍니다.",\
                "가이드 라인에 위배되는 부적절한 사진을 업로드하여 사진이 반려 되었습니다.",\
                "가이드 라인에 위배되는 부적절한 내용의 설명을 첨부하여 사진이 반려 되었습니다."
                ]

def change(modeladmin, request, queryset):
    # queryset.update(views = 1)
    print(str(request))
    print(str(queryset))
    user = User.objects.get(email = 'baek5@seunghyun.com')
    user.nickname = 'asdasd'
    user.save()
    messages.success(request, "배송상태로 변경")


class PhotoInline(admin.TabularInline):
    model = Report
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
    list_display = ['posts_image','image_tag','pk','latitude','longitude','contents', 'views','problem', 'is_active', 'handling']
    list_display_links = ['pk', 'contents', 'views', 'problem', 'is_active']
    list_filter = ['problem','is_active', 'handling']
    search_fields = ['id','contents',]
    date_hierarchy = 'created'
    readonly_fields = ['user', 'posts_image', 'back_image', 'latitude', 'longitude', 'contents', 'modify_date']
    actions = ('action_bad_location','action_bad_image', 'action_bad_caption', 'action_no_problem')
    # inlines = [
    #     PhotoInline,
    # ]
    def action_bad_location(modeladmin, request, queryset):
        print(f"asdasdasdasdasd{request}")
        for obj in queryset:
            obj.handling = 22002
            obj.problem = True
            obj.is_active = False
            obj.save()
            Notice.objects.create(receiver_id = obj.user.id, post = obj, kind = 22001, reason_detail = detail_reason[0])
        messages.success(request, "게시물 반려(부정확한 위치)")

    def action_bad_image(modeladmin, request, queryset):
        print(f"asdasdasdasdasd{request}")
        for obj in queryset:
            obj.handling = 22003
            obj.problem = True
            obj.is_active = False
            obj.save()
            Notice.objects.create(receiver_id = obj.user.id, post = obj, kind = 22001, reason_detail = reason_detail[1])
        messages.success(request, "게시물 반려(부적절한 사진)")

    def action_bad_caption(modeladmin, request, queryset):
        print(f"asdasdasdasdasd{request}")
        for obj in queryset:
            obj.handling = 22004
            obj.problem = True
            obj.is_active = False
            obj.save()
            Notice.objects.create(receiver_id = obj.user.id, post = obj, kind = 22001, reason_detail = reason_detail[2])
        messages.success(request, "게시물 반려(부적절한 내용)")

    def action_no_problem(modeladmin, request, queryset):
        print(f"asdasdasdasdasd{request}")
        for obj in queryset:
            obj.handling = 22001
            obj.save()
            Notice.objects.create(receiver_id = obj.user.id, post = obj, kind = 22002)
        messages.success(request, "문제 없는 게시물")

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    # def get_name(self, obj):
    #     print(str(obj.hashtag.))
    #     return obj.hashtag.name
    # # get_name.admin_order_field  = 'author'  #Allows column order sorting
    # # get_name.short_description = 'Author Name'  #Renames column head
class VillainInline(admin.StackedInline):
    model = Notice

detail_reason2 = {"spam":"스팸광고가 포함되어 있는 게시물 입니다","욕설 및 비방":"사진의 설명에 욕설 및 비방 문구가 포함되어 있습니다.",\
                    "음란물":"사진이나 내용에 음란성 내용이 포함되어 있습니다",\
                    "무단도용":"무단 도용 여부가 있는 게시글 입니다"}
class ReportAdmin(admin.ModelAdmin):
    list_display = ['image_post','reporter', 'post_owner', 'comment_owner', 'post','post_caption','detail','comment_contents','handling']
    # list_display_links = ['pk', 'contents', 'views', 'problem', 'is_active']
    list_filter = ['reason','handling']
    search_fields = ['post_owner', 'comment_owner', 'post_owner', 'detail', 'post_caption','comment_contents' ]
    date_hierarchy = 'created_date'
    inlines = [VillainInline]
    def save_model(self, request, obj, form, change):
        post_obj = Post.objects.get(id = obj.post.id)
        post_obj.problem = True
        post_obj.save()
        print(f"request: {request} obj:{obj} , change: {change}")
        super(ReportAdmin, self).save_model(request, obj, form, change)
    # readonly_fields = ['user', 'posts_image', 'back_image', 'latitude', 'longitude', 'contents', 'modify_date']
    actions = ('action_problem','action_no_problem')
    def action_problem(modeladmin, request, queryset):
        print(f"asdasdasdasdasd{request}")
        post_set = Post.objects.all()
        comment_set = Comment.objects.all()
        for obj in queryset:
            obj.handling = True

            if not obj.comment:
                post_obj = post_set.get(id = obj.post.id)
                obj.handling = 2
                post_obj.problem = True
                if obj.reason == 1:
                    Notice.objects.create(receiver = obj.post.user, post = obj.post,report = obj , kind = 22004, reason_detail = detail_reason2['spam'])
                elif obj.reason == 2:
                    Notice.objects.create(receiver = obj.post.user, post = obj.post,report = obj , kind = 22004, reason_detail = detail_reason2['욕설 및 비방'])
                elif obj.reason == 3:
                    Notice.objects.create(receiver = obj.post.user, post = obj.post,report = obj , kind = 22004, reason_detail = detail_reason2['음란물'])
                else:
                    Notice.objects.create(receiver = obj.post.user, post = obj.post,report = obj , kind = 22004, reason_detail = detail_reason2['무단도용'])
                post_obj.save()
            else:
                comment_obj = comment_set.get(id = obj.comment.id)
                obj.handling = 4
                comment_obj.is_problem = True
                if obj.reason == 1:
                    Notice.objects.create(receiver = obj.post.user, post = obj.post,report = obj , kind = 22004, reason_detail = detail_reason2['spam'])
                elif obj.reason == 2:
                    Notice.objects.create(receiver = obj.post.user, post = obj.post,report = obj , kind = 22004, reason_detail = detail_reason2['욕설 및 비방'])
                elif obj.reason == 3:
                    Notice.objects.create(receiver = obj.post.user, post = obj.post,report = obj , kind = 22004, reason_detail = detail_reason2['음란물'])
                else:
                    Notice.objects.create(receiver = obj.post.user, post = obj.post,report = obj , kind = 22004, reason_detail = detail_reason2['무단도용'])
                comment_obj.save()
            obj.save()
        messages.success(request, "부적절 게시글 신고 처리 완료")

    def action_no_problem(modeladmin, request, queryset):
        print(f"asdasdasdasdasd{request}")
        post_set = Post.objects.all()
        comment_set = Comment.objects.all()
        for obj in queryset:
            if not obj.comment:
                post_obj = post_set.get(id = obj.post.id)
                obj.handling = 2
                post_obj.problem = False
                post_obj.save()
            else:
                comment_obj = comment_set.get(id = obj.comment.id)
                comment_obj.is_problem = False
                obj.handling = 4
                comment_obj.save()
            obj.save()
        messages.success(request, "문제 없는 게시물 신고 처리 완료")


    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    # def is_locked(self, obj):  # Get Image url
    #     yes_icon = mark_safe('<img src="/static/admin/img/icon-yes.svg" alt="True"/>')
    #     no_icon = mark_safe('<img src="/static/admin/img/icon-no.svg" alt="False"/>')
    #     obj.handling = not obj.handling
    #     obj.save()
    #     if obj.handling:
    #         return mark_safe('<a target="_blank" href="%s/change/">%s</a>' % (obj.pk, yes_icon))
    #     else:
    #         return mark_safe('<a target="_blank" href="%s/change/">%s</a>' % (obj.pk, no_icon))
    # is_locked.allow_tags = True
    # is_locked.short_description = 'Locked'

    # def change(modeladmin, request, queryset):
    #     # queryset.update(views = 1)
    #     print(str(request))
    #     print(str(queryset))
    #     user = User.objects.get(email = 'baek5@seunghyun.com')
    #     user.nickname = 'asdasd'
    #     user.save()
    #     messages.success(request, "배송상태로 변경")
def change(modeladmin, request, queryset):
    # queryset.update(views = 1)
    print(str(request))
    print(str(queryset))
    user = User.objects.get(email = 'baek5@seunghyun.com')
    user.nickname = 'asdasd'
    user.save()
    messages.success(request, "배송상태로 변경")

class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','user','post','contents']

admin.site.register(User, UserAdmin)
# admin.site.register(UserData)
admin.site.register(Post,PostsAdmin)
admin.site.register(HashTag)
admin.site.register(PostTag)
admin.site.register(Comment,CommentAdmin)
admin.site.register(PostLike)
admin.site.register(Scrapt)
admin.site.register(Report,ReportAdmin)
admin.site.register(Notice)
