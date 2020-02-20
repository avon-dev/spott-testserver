from testapp.assemble_view.__init__ import *



from rest_framework import viewsets
from django.core.serializers.json import DjangoJSONEncoder
from django.db import IntegrityError
from random import *



class NoticeView(APIView):
    permission_classes = ()


    def get(self,request, format = None):
        data = Return_Module.string_to_dict(request.GET) #sending으로 묶여서 오는 파라미터 데이터 추출
        page = data['page'] #클라이언트에서 보내주는 page count
        craeted_time = data['created_time'] #클라이언트에서 보내주는 최신 게시물 생성 날짜
        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        user = User.objects.get(email = decodedPayload['id'])
        #페이징
        begin_item = page
        last_index = page + 21

        # 생성일 넘겨주는 부분
        notice_queryset = Notice.objects.filter(receiver = user).order_by('-id')[begin_item:last_index]\
                    if craeted_time == ""\
                    else Notice.objects.filter(receiver = user, created_date__lte=craeted_time).order_by('-id')[begin_item:last_index]
        notice_list = list(notice_queryset.values())
        count = 0
        for obj in notice_queryset:
            if obj.kind == 22001:
                notice_list[count]['post_image'] = obj.post.posts_image.url
                notice_list[count]['reason'] = obj.post.get_handling_display()

            elif obj.kind == 22002:#통과
                notice_list[count]['post_image'] = obj.post.posts_image.url
            elif obj.kind == 22003:#댓글 남김
                notice_list[count]['comment_user_nick'] = obj.comment.user.nickname
                notice_list[count]['comment_user_image'] = obj.comment.user.profile_image.url
                notice_list[count]['post_id'] = obj.comment.post.id
                notice_list[count]['post_image'] = obj.comment.post.posts_image.url
                notice_list[count]['comment_user_id'] = obj.comment.user.id
            elif obj.kind == 22004:#규칙 위반 게시물
                notice_list[count]['reason'] = obj.report.get_reason_display()
                notice_list[count]['post_image'] = obj.report.post_url
            else:
                notice_list[count]['reason'] = obj.report.get_reason_display()
            count += 1


        pageable = False if len(notice_list) < 21 else True

        created_time = str(notice_list[0]['created_date']) if craeted_time == "" else craeted_time
        # home_serializers = HomeSerializer(notice_obj_cached[0:20],many=True)

        result = Return_Module.ReturnPattern.success_text\
        ("show mypage", items = notice_list, created_time = created_time, pageable = pageable)

        return Response(result,status=status.HTTP_200_OK)


class NoticeDetailView(APIView):

    def get(self ,request ,pk ,format=None):
        data = Return_Module.string_to_dict(request.GET)
        actions = {'return_posts':22001,'violation_posts':22004, "violation_comment":22005}
        notice = Notice.objects.get(pk = pk)
        kind = notice.kind
        if kind == actions['violation_posts']: #규칙위반 게시물
            report = Report.objects.get(id = notice.report.id)
            print(report.id)
            image_url = report.post_url
            caption = report.post_caption
            result = Return_Module.ReturnPattern.success_text\
            ("show mypage", image_url = image_url, caption = caption)
            return Response(result)
        elif kind == actions['return_posts']:
            post = Post.objects.get(id = notice.post.id)
            image_url = post.posts_image.url
            caption = post.contents
            result = Return_Module.ReturnPattern.success_text\
            ("show mypage", image_url = image_url, caption = caption)
            return Response(result)
        else:
            report = Report.objects.get(id = notice.report.id)
            caption = report.comment_contents
            result = Return_Module.ReturnPattern.success_text\
            ("show mypage", caption = caption)
            return Response(result)






    # def retrieve(self, request, pk=None):
    #     result_dict = {"success":12000,"report":12001,"failed 404":14040}
    #     string = request.headers["Authorization"]
    #     decodedPayload = jwt.decode(string[4:],None,None)
    #     try:
    #         posts = Post.objects.get(problem = False, is_active = True, pk = pk)
    #     except Exception as e:
    #         result = Return_Module.ReturnPattern.success_text\
    #         ("posts_get fail",result=result_dict['failed 404'])
    #         return Response(result, status = status.HTTP_404_NOT_FOUND)
    #     report_all = Report.objects.all()
    #     comment = Comment.objects.filter(post = posts)
    #     report_comment = report_all.filter(reporter_id = decodedPayload['id'],comment__in = comment, handling = 3).values('comment_id')
    #     report_post = report_all.filter(reporter_id = decodedPayload['id'], post = posts, handling = 1)
    #     if report_post:
    #         result = Return_Module.ReturnPattern.success_text\
    #         ("reported posts",result = result_dict["report"])
    #         return Response(result)
    #     else:
    #         serializers = PostDetailSerializer(posts)
    #         user = User.objects.get(is_active = True, user_uid = decodedPayload["id"])
    #         # print("posts" + str(posts))
    #         # print("serial" + str(serializers.data))
    #         comment_count = len(Comment.objects.filter(is_active = True,\
    #         post_id = pk, is_problem = False).exclude(id__in= report_comment))
    #
    #         try:
    #             like = PostLike.objects.get(post = posts, user = user)
    #         # success
    #         except PostLike.DoesNotExist:
    #             like_checked = False
    #         else:
    #             like_checked = True
    #
    #         try:
    #             scrap = Scrapt.objects.get(post = posts, user = user)
    #         # success
    #         except Scrapt.DoesNotExist:
    #             scrap_checked = False
    #         else:
    #             scrap_checked = True
    #
    #         if serializers.data['user']['user_uid'] == decodedPayload["id"]:
    #             myself = True
    #         else:
    #             myself = False
    #
    #         serial_dumps = Return_Module.jsonDumpsLoads(self,**serializers.data)
    #         serial_dumps['comment'] = comment_count
    #         serial_dumps['count'] = len(serializers.data['like_user'])
    #         serial_dumps['like_checked'] = like_checked
    #         serial_dumps['scrap_checked'] = scrap_checked
    #         serial_dumps['myself'] = myself
    #         result = Return_Module.ReturnPattern.success_text\
    #         ("show posts detail success",**serial_dumps, result = result_dict["success"])
    #         return Response(result)
