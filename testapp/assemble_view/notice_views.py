from testapp.assemble_view.__init__ import *



from rest_framework import viewsets
from django.core.serializers.json import DjangoJSONEncoder
from django.db import IntegrityError
from random import *



class NoticeView(APIView):
    permission_classes = ()


    def get(self,request, format = None):

        request_data_key = ['page', 'created_time']
        # sending으로 안 묶여 있으면 에러 처리
        try:
            request_data = Return_Module.string_to_dict(request.GET) #sending 파라미터에서 value 추출해서 dict 형태로 변형
        except KeyError as e:
            # print(f"key error: missing key name {e}") #에러 로그
            result = Error_Module.ErrorHandling.none_bundle(req.request_bundle, e) #클라이언트에 보낼 에러 메시지
            return Response(result,status = status.HTTP_400_BAD_REQUEST)

        #필드에 필수 키가 있는지 확인 후 없을 경우 에러 반환
        try:
            for key in request_data_key:
                request_data[key]
        except KeyError as e:
            error_dict = Error_Module.ErrorHandling.none_feild(request_data_key,request_data.keys(), e)
            result = Return_Module.ReturnPattern.error_text(error_dict)
            return Response(result,status = status.HTTP_400_BAD_REQUEST)
        else:
            page = request_data[request_data_key[0]] #클라이언트에서 보내주는 page count
            created_time = request_data[request_data_key[1]] #클라이언트에서 보내주는 최신 게시물 생성 날짜

        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        user = User.objects.get(email = decodedPayload['id'])
        #페이징
        begin_item = page
        last_index = page + 21

        # 생성일 넘겨주는 부분
        notice_queryset = Notice.objects.filter(receiver = user).order_by('-id')[begin_item:last_index]\
                    if created_time == ""\
                    else Notice.objects.filter(receiver = user, created_date__lte=created_time).order_by('-id')[begin_item:last_index]
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
            notice_list[count]['confirmation'] = True
            count += 1
        Notice.objects.filter(receiver = user).update(confirmation = True)

        pageable = False if len(notice_list) < 21 else True

        created_time = str(notice_list[0]['created_date']) if created_time == "" else created_time
        # home_serializers = HomeSerializer(notice_obj_cached[0:20],many=True)

        result = Return_Module.ReturnPattern.success_text\
        ("show notice list", items = notice_list, created_time = created_time, pageable = pageable)

        return Response(result,status=status.HTTP_200_OK)


class NoticeDetailView(APIView):

    def get(self ,request ,pk ,format=None):

        actions = {'return_posts':22001,'violation_posts':22004, "violation_comment":22005}

        notice = Notice.objects.get(pk = pk)
        kind = notice.kind
        if kind == actions['violation_posts']: #규칙위반 게시물
            report = Report.objects.get(id = notice.report.id)
            print(report.id)
            image_url = report.post_url
            caption = report.post_caption
            result = Return_Module.ReturnPattern.success_text\
            ("show notice", image_url = image_url, caption = caption)
            return Response(result)
        elif kind == actions['return_posts']:
            post = Post.objects.get(id = notice.post.id)
            image_url = post.posts_image.url
            caption = post.contents
            result = Return_Module.ReturnPattern.success_text\
            ("show notice", image_url = image_url, caption = caption)
            return Response(result)
        else:
            report = Report.objects.get(id = notice.report.id)
            caption = report.comment_contents
            result = Return_Module.ReturnPattern.success_text\
            ("show notice", caption = caption)
            return Response(result)

    @transaction.atomic
    def delete(self, request, pk, format=None):
        try:
            notice = Notice.objects.get(pk = pk)
        except Notice.DoesNotExist as e:
            result = Return_Module.ReturnPattern.error_text(str(e))
            return Response(result, status = status.HTTP_404_NOT_FOUND)
        else:
            notice.delete()
            result = Return_Module.ReturnPattern.success_text\
            ("delete success", result = True)
            return Response(result)
