from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe
from django.contrib import messages
from function import string as string_get
from django.db import transaction


class PhotoInline(admin.TabularInline):
    model = Report
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['pk','email','nickname', 'joined_date','is_staff','is_active',]


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

    #부정확한 위치
    @transaction.atomic
    def action_bad_location(modeladmin, request, queryset):

        for obj in queryset:
            obj.handling = Post.bad_location
            obj.problem = True
            obj.is_active = False
            obj.reason_detail = "부정확한 위치정보"
            obj.save()
            Notice.objects.create(receiver_id = obj.user.id, post = obj, \
            kind = Notice.picture_return)
        # __str__ : "위치정보"
        messages.success(request, "게시물 반려(부정확한 위치)")

    #부적절한 사진
    @transaction.atomic
    def action_bad_image(modeladmin, request, queryset):

        for obj in queryset:
            obj.handling = Post.bad_picture
            obj.problem = True
            obj.is_active = False
            obj.reason_detail = "부적절한 사진"
            obj.save()
            Notice.objects.create(receiver_id = obj.user.id, post = obj,\
             kind = Notice.picture_return)
        messages.success(request, "게시물 반려(부적절한 사진)")

    #부적절한 내용
    @transaction.atomic
    def action_bad_caption(modeladmin, request, queryset):

        for obj in queryset:
            obj.handling = Post.bad_contents
            obj.problem = True
            obj.is_active = False
            obj.reason_detail = "부적절한 내용"
            obj.save()
            Notice.objects.create(receiver_id = obj.user.id, post = obj,\
             kind = Notice.picture_return)
        messages.success(request, "게시물 반려(부적절한 내용)")

    @transaction.atomic
    def action_no_problem(modeladmin, request, queryset):

        for obj in queryset:
            obj.handling = Post.no_problem
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

# detail_reason2 = {"spam":"스팸광고가 포함되어 있는 게시물 입니다","욕설 및 비방":"사진의 설명에 욕설 및 비방 문구가 포함되어 있습니다.",\
#                     "음란물":"사진이나 내용에 음란성 내용이 포함되어 있습니다",\
#                     "무단도용":"무단 도용 여부가 있는 게시글 입니다"}
class ReportAdmin(admin.ModelAdmin):
    list_display = ['image_post','reporter_email','comment' ,'post','post_caption','detail','comment_contents','handling']
    # list_display_links = ['pk', 'contents', 'views', 'problem', 'is_active']
    list_filter = ['reason','handling']
    search_fields = ['detail', 'post_caption','comment_contents' ]
    date_hierarchy = 'created_date'
    # fields = (('reporter','post_owner'),'comment_owner',)
    # raw_id_fields = ("post",)
    save_on_top = True #저장 버튼 윗 쪽에도 생성
    autocomplete_fields = ['post']



    @transaction.atomic
    def save_model(self, request, obj, form, change):

        obj.handling = True
        print(f"시작")
        if not obj.comment:
            post_obj = Post.objects.get(id = obj.post.id)
            obj.handling = Report.after_posts
            post_obj.problem = True
            print(f"게시물")
            Notice.objects.create(receiver = obj.post.user, report = obj, kind = Notice.violation_posts)
            post_obj.save()
        else:
            print(f"코멘트")
            comment_obj = Comment.objects.get(id = obj.comment.id)
            print(f"코멘트{comment_obj}")
            obj.handling = Report.after_comment
            comment_obj.is_problem = True
            Notice.objects.create(receiver = obj.comment.user, report = obj, kind = Notice.violation_comment)
            comment_obj.save()
        obj.save()
        print(f"request: {request} obj:{obj} , change: {change}")
        super(ReportAdmin, self).save_model(request, obj, form, change)
    # readonly_fields = ['user', 'posts_image', 'back_image', 'latitude', 'longitude', 'contents', 'modify_date']
    actions = ('action_problem','action_no_problem')

    @transaction.atomic
    def action_problem(modeladmin, request, queryset):
        print(f"asdasdasdasdasd{request}")

        post_set = Post.objects.all()
        comment_set = Comment.objects.all()
        for obj in queryset:
            obj.handling = True

            if not obj.comment:
                post_obj = post_set.get(id = obj.post.id)
                obj.handling = Report.after_posts
                post_obj.problem = True
                Notice.objects.create(receiver = obj.post.user, report = obj, kind = Notice.violation_posts)
                if obj.reason == Report.spam:
                    obj.reason_detail = string_get.spam
                elif obj.reason == Report.slander:
                    obj.reason_detail = string_get.slander
                elif obj.reason == Report.porno:
                    obj.reason_detail = string_get.porno
                else:
                    obj.reason_detail = string_get.steal
                post_obj.save()
            else:
                comment_obj = comment_set.get(id = obj.comment.id)
                obj.handling = Report.after_comment
                comment_obj.is_problem = True
                Notice.objects.create(receiver = obj.comment.user, report = obj, kind = Notice.violation_comment)
                if obj.reason == Report.spam:
                    obj.reason_detail = string_get.spam
                elif obj.reason == Report.slander:
                    obj.reason_detail = string_get.slander
                elif obj.reason == Report.porno:
                    obj.reason_detail = string_get.porno
                else:
                    obj.reason_detail = string_get.steal
                comment_obj.save()
            obj.save()
        messages.success(request, "부적절 게시글 신고 처리 완료")



    @transaction.atomic
    def action_no_problem(modeladmin, request, queryset):

        post_set = Post.objects.all()
        comment_set = Comment.objects.all()
        for obj in queryset:
            if not obj.comment:
                post_obj = post_set.get(id = obj.post.id)
                obj.handling = Report.no_problem
                post_obj.problem = False
                post_obj.save()
            else:
                comment_obj = comment_set.get(id = obj.comment.id)
                comment_obj.is_problem = False
                obj.handling = Report.no_problem
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


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','user','post','contents', 'created']

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
admin.site.register(AppNotices)
