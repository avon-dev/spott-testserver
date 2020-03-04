
from testapp.assemble_view.__init__ import *
from settings import settings
from pytz import timezone
from django.core.serializers.json import DjangoJSONEncoder



class CommentView(APIView):
    permission_classes = (IsAuthenticated,)



    # def get(self, request, post_pk, pk, format=None):
    #     string = request.headers["Authorization"]
    #     decodedPayload = jwt.decode(string[4:],None,None)
    #     user = User.objects.get(user_uid = decodedPayload['id'])
    #     comment = Comment.objects.filter(pk = pk, user_id = user.id)
    #     return Response(comment.values())

    @transaction.atomic
    def delete(self, request, post_pk, pk, format=None):
        # post = Post.objects.get(pk = post_pk) #해당 포스트 가져오기

        #접속한 유저 가져오기
        user = orm.get_myself(self, request)

        result = Return_Module.ReturnPattern.success_dict\
        (string_get.successful_delete,result=True)

        try:
            comment = Comment.objects.get(is_active = True,pk = pk, user_id = user.id)
        except ObjectDoesNotExist:
            result['message'] = string_get.impossible_deleted
            result['payload']['result'] = False
            result = json.dumps(result)
            return Response(result)
        else:
            comment.is_active = False
            comment.save()
            result = json.dumps(result)
            return Response(result)

    @transaction.atomic
    def patch(self, request, post_pk, pk, format=None):
        my_email = req.my_email(self, request)

        # sending으로 안 묶여 있으면 에러 처리
        try:
            request_data = Return_Module.string_to_dict(request.data) #sending 파라미터에서 value 추출해서 dict 형태로 변형
        except KeyError as e:
            # print(f"key error: missing key name {e}") #에러 로그
            result = Error_Module.ErrorHandling.none_bundle(req.request_bundle, e) #클라이언트에 보낼 에러 메시지
            return Response(result,status = status.HTTP_400_BAD_REQUEST)

        #필드에 필수 키가 있는지 확인 후 없을 경우 에러 반환
        try:
            for key in req.comment_update_keys:
                request_data[key]
        except KeyError as e:
            error_dict = Error_Module.ErrorHandling.none_feild(req.comment_update_keys,request_data.keys(), e)
            result = Return_Module.ReturnPattern.error_text(error_dict)
            return Response(result,status = status.HTTP_400_BAD_REQUEST)

        result = Return_Module.ReturnPattern.success_dict\
        (string_get.successful_update,result=True)

        try:
            user = User.objects.get(email = my_email)
            comment = Comment.objects.get(is_active = True,pk = pk, user_id = user.id)
        except ObjectDoesNotExist:
            result['message'] = string_get.update_failed
            result['payload']['result'] = False
            result = json.dumps(result)
            return Response(result)
        else:
            time = datetime.datetime.now(timezone(settings.TIME_ZONE))
            request_data['modify_date'] = time
            serializer = CommentSerializer(comment,data = request_data, partial=True)
            # print(serializer.data)

            if serializer.is_valid():
                serializer.save()
                result = json.dumps(result)
                return Response(result)





class CommentListView(APIView):
    permission_classes = (IsAuthenticated,)


    def get(self, request, post_pk, format=None):


        # sending으로 안 묶여 있으면 에러 처리
        try:
            request_data = Return_Module.string_to_dict(request.GET) #sending 파라미터에서 value 추출해서 dict 형태로 변형
        except KeyError as e:
            # print(f"key error: missing key name {e}") #에러 로그
            result = Error_Module.ErrorHandling.none_bundle(req.request_bundle, e) #클라이언트에 보낼 에러 메시지
            return Response(result,status = status.HTTP_400_BAD_REQUEST)

        #필드에 필수 키가 있는지 확인 후 없을 경우 에러 반환
        try:
            for key in req.comment_show_list_keys:
                request_data[key]
        except KeyError as e:
            error_dict = Error_Module.ErrorHandling.none_feild(req.comment_show_list_keys,request_data.keys(), e)
            result = Return_Module.ReturnPattern.error_text(error_dict)
            return Response(result,status = status.HTTP_400_BAD_REQUEST)
        else:
            page = request_data[req.page] #클라이언트에서 보내주는 page count
            craeted_time = request_data[req.created_time] #클라이언트에서 보내주는 최신 게시물 생성 날짜
            action = request_data[req.action] #클라이언트에서 보내주는 page count



        my_email = req.my_email(self, request)


        #페이징 넘버
        begin_item = page
        last_index = page + 21

        comment = Comment.objects.all()
        report = Report.objects.filter(reporter_id = my_email,\
        comment__in = comment, handling = Report.before_comment).values('comment_id')

        comment = comment.filter(is_active = True,\
        post_id = post_pk, is_problem = False).exclude(id__in= report).\
        order_by('-id')[begin_item:last_index]\
        if craeted_time == ""\
        else comment.filter(is_active = True,\
        post_id = post_pk,\
        created__lte=craeted_time, is_problem = False).exclude(id__in= report).\
        order_by('-id')[begin_item:last_index]

        comment_obj_cached = comment

        pageable = False if comment_obj_cached.count() < 21 else True

        try:
            comment_created_time = comment_obj_cached[0].created

        except IndexError:
            result = Return_Module.ReturnPattern.success_text\
            ("comment blank",result=False)
            return Response(result)


        #데이터 베이스 안의 정보와 비교가 안 돼 str을 이용해 스트링으로 변환을 해 주었다.
        created_time = str(comment_created_time) if craeted_time == "" else craeted_time

        # comment = Comment.objects.filter(user = post.comment.)

        comment_serial = CommentSerializer(comment_obj_cached[0:20], many=True)

        # user = User.objects.filter(id=comment.user_id)

        comment_dump = json.dumps(comment_serial.data)
        comment_dict = json.loads(comment_dump)
        count = 0
        for data in comment_dict:
            if data['user']['user_uid'] == my_email:
                comment_dict[count]['myself'] = True
            else:
                comment_dict[count]['myself'] = False
            count = count + 1

        if action == req.notice_to_comment:
            post = Post.objects.filter(id=post_pk)
            notice_list = list(post.values('user', 'contents', "created"))
            notice_list[0]['user_nickname'] = post[0].user.nickname
            notice_list[0]['user_profile_image'] = post[0].user.profile_image.url
            # notice_list
            result = Return_Module.ReturnPattern.success_text\
            ("show comment list(from notice page)",items = comment_dict, created_time = created_time, pageable = pageable, notice_data = notice_list[0])
            # result = {"payload":{"items":comment_dict, "created_time":created_time, "pageable":pageable, "notice_data":notice_list[0]}}
            # print(dict)
            return Response(result)
        else:
            result = Return_Module.ReturnPattern.success_text\
            ("show comment list",items = comment_dict, created_time = created_time, pageable = pageable)
            # print(dict)
            return Response(result)


    def post(self, request, post_pk, format=None):
        post = Post.objects.get(pk = post_pk)
        user_myself = orm.get_myself(self,request)


        # sending으로 안 묶여 있으면 에러 처리
        try:
            request_data = Return_Module.string_to_dict(request.data) #sending 파라미터에서 value 추출해서 dict 형태로 변형
        except KeyError as e:
            # print(f"key error: missing key name {e}") #에러 로그
            result = Error_Module.ErrorHandling.none_bundle(req.request_bundle, e) #클라이언트에 보낼 에러 메시지
            return Response(result,status = status.HTTP_400_BAD_REQUEST)

        #필드에 필수 키가 있는지 확인 후 없을 경우 에러 반환
        try:
            for key in req.comment_create_keys:
                request_data[key]
        except KeyError as e:
            error_dict = Error_Module.ErrorHandling.none_feild(req.comment_create_keys,request_data.keys(), e)
            result = Return_Module.ReturnPattern.error_text(error_dict)
            return Response(result,status = status.HTTP_400_BAD_REQUEST)
        else:
            contents = request_data[req.caption] #댓글의 내용

        # success
        comment = Comment.objects.create(post = post, user=user_myself, \
        contents=request_data['caption'])
        if not post.user.email ==user_myself.email:
            Notice.objects.create(receiver =post.user, comment = comment, kind = 22003)
        result = Return_Module.ReturnPattern.success_text\
        (string_get.successful_creation,result=True)
        return Response(result)
