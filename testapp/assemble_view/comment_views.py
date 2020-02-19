
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


    def delete(self, request, post_pk, pk, format=None):
        post = Post.objects.get(pk = post_pk) #해당 포스트 가져오기

        #접속한 유저의 id 가져오기
        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        user = User.objects.get(user_uid = decodedPayload['id'])

        result = Return_Module.ReturnPattern.success_text\
        ("success delete",result=True)

        try:
            comment = Comment.objects.get(pk = pk, user_id = user.id)
        except ObjectDoesNotExist:
            result = json.loads(result)
            result['message'] = "impossible deleted"
            result['payload']['result'] = False
            result = json.dumps(result)
            return Response(result)
        else:
            comment.is_active = False
            comment.save()

            return Response(result)


    def patch(self, request, post_pk, pk, format=None):
        request_data = Return_Module.string_to_dict(request.data)
        print(request_data)
        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)

        result = Return_Module.ReturnPattern.success_text\
        ("success update",result=True)

        try:
            user = User.objects.get(user_uid = decodedPayload['id'])
            comment = Comment.objects.get(pk = pk, user_id = user.id)
        except ObjectDoesNotExist:
            result = json.loads(result)
            result['message'] = "can not update"
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
                print("update")
                return Response(result)





class CommentListView(APIView):
    permission_classes = (IsAuthenticated,)



    def get(self, request, post_pk, format=None):
        data = Return_Module.string_to_dict(request.GET)
        page = data['page'] #클라이언트에서 보내주는 page count
        craeted_time = data['created_time'] #클라이언트에서 보내주는 최신 게시물 생성 날짜

        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        #페이징
        begin_item = page
        last_index = page + 21
        # print(craeted_time)
        # exclude(id__in= report).
        comment = Comment.objects.all()
        report = Report.objects.filter(reporter_id = decodedPayload['id'],comment__in = comment, handling = 3).values('comment_id')
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
            comment_obj_cached[0].created

        except IndexError:
            result = Return_Module.ReturnPattern.success_text\
            ("comment blank",result=False)
            return Response(result)

        created_time = str(comment_obj_cached[0].created) if craeted_time == "" else craeted_time

        # comment = Comment.objects.filter(user = post.comment.)

        comment_serial = CommentSerializer(comment_obj_cached[0:20], many=True)

        # user = User.objects.filter(id=comment.user_id)

        comment_dump = json.dumps(comment_serial.data)
        comment_dict = json.loads(comment_dump)
        count = 0
        for data in comment_dict:
            if data['user']['user_uid'] == decodedPayload['id']:
                comment_dict[count]['myself'] = True
            else:
                comment_dict[count]['myself'] = False
            count = count + 1
        result_dict = {"payload":{"items":comment_dict, "created_time":created_time, "pageable":pageable}}
        result = json.dumps(result_dict,cls=DjangoJSONEncoder)
        # print(dict)
        return Response(result)


    def post(self, request, post_pk, format=None):
        post = Post.objects.get(pk = post_pk)
        token_value = request.headers["Authorization"]
        decodedPayload = jwt.decode(token_value[4:],None,None)
        user = User.objects.get(user_uid = decodedPayload["id"])
        request_data = Return_Module.string_to_dict(request.data)

        # success
        comment = Comment.objects.create(post = post, user=user, contents=request_data['caption'])

        result = Return_Module.ReturnPattern.success_text\
        ("success create",result=True)
        return Response(result)
