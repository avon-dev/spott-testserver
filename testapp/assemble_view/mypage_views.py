from testapp.assemble_view.__init__ import *


from random import *




class MypageViewSet(APIView):

    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        # string = request.headers["Authorization"]
        # decodedPayload = jwt.decode(string[4:],None,None)
        # user = User.objects.get(is_active = True, user_uid = decodedPayload["id"])
        user = orm.get_myself(self, request)
        post = Post.objects.filter(problem = False, is_active = True, user = user).order_by('-id')
        post_serializers = MypageSerializer(post, many = True)
        user_serializers = MyUserSerializer(user)

        notice = Notice.objects.filter(receiver = user.id, confirmation = False)

        is_confirmation = notice.count()
        result = Return_Module.ReturnPattern.success_text\
        ("show mypage", user = user_serializers.data, posts = post_serializers.data,\
         myself = True, is_confirmation = is_confirmation)
        return Response(result)


#게시물 공게 비공개 설정
    @transaction.atomic
    def patch(self, request, format=None):
        request_data_key = ['is_public']
        # sending으로 안 묶여 있으면 에러 처리
        try:
            request_data = Return_Module.string_to_dict(request.data) #sending 파라미터에서 value 추출해서 dict 형태로 변형
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
            is_public = request_data[request_data_key[0]]


        user = orm.get_myself(self, request)

        user.is_public = is_public
        post = Post.objects.filter(user = user).update(is_public = is_public)
        user.save()
        # print(str(post.values()))
        if is_public:
            result = Return_Module.ReturnPattern.success_text\
            ("public account" , is_public = True)
            return Response(result)
        else:
            result = Return_Module.ReturnPattern.success_text\
            ("private account" , is_public = False)
            return Response(result)




class UserMypageViewSet(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        my_email = req.my_email(self, request)
        action_search = 1201
        action_user_mypage = 1202
        request_data_key = ['action']

        # sending으로 안 묶여 있으면 에러 처리
        try:
            request_data = Return_Module.string_to_dict(request.GET) #sending 파라미터에서 value 추출해서 dict 형태로 변형
        except KeyError as e:
            # print(f"key error: missing key name {e}") #에러 로그
            result = Error_Module.ErrorHandling.none_bundle(req.request_bundle, e) #클라이언트에 보낼 에러 메시지
            return Response(result,status = status.HTTP_400_BAD_REQUEST)

        print("request.GET"+str(request.GET))
        #필드에 필수 키가 있는지 확인 후 없을 경우 에러 반환
        try:
            for key in request_data_key:
                request_data[key]
        except KeyError as e:
            error_dict = Error_Module.ErrorHandling.none_feild(request_data_key,request_data.keys(), e)
            result = Return_Module.ReturnPattern.error_text(error_dict)
            return Response(result,status = status.HTTP_400_BAD_REQUEST)
        else:
            action = request_data[req.action]

        user = orm.get_user_pk(self, pk)


        myself = True if my_email == user.user_uid else False #불러올 계정과 로그인 유저가 같으면 true 다르면 false 반환

        post = Post.objects.filter(handling = Post.no_problem, is_active = True, problem = False, user = user).order_by('-id')\
        if myself else Post.objects.filter(handling = Post.no_problem, is_public = True, is_active = True, problem = False, user = user).order_by('-id')

        post_serializers = MypageSerializer(post,many=True)
        user_serializers = MyUserSerializer(user)

        # result = Return_Module.ReturnPattern.success_text("Send success",result=True,code=random_number)
        result = Return_Module.ReturnPattern.success_text\
        ("show user mypage", user = user_serializers.data, posts = post_serializers.data, myself = myself)
        # dict = {"payload":{"user":user_serializers.data,"posts":post_serializers.data},"message":"success"}
        # result = json.dumps(dict)

        if action == action_search:
            user = orm.get_myself(self, request)
            recent_search_word = user.recent_search
            print(decodedPayload['id'])
            count = 0
            for obj in recent_search_word:
                if obj['user_pk'] == pk:
                    break
                else:
                    count += 1

            if count == len(recent_search_word):
                user.recent_search.insert(0,{"action":1202,"tag_name":"", "user_pk":pk})
                user.save()
            else:
                del user.recent_search[count]
                user.recent_search.insert(0,{"action":1202,"tag_name":"", "user_pk":pk})
                user.save()

            result = Return_Module.ReturnPattern.success_text\
            ("search success", user = user_serializers.data, posts = post_serializers.data, myself = myself)
            return Response(result,status=status.HTTP_201_CREATED)
        return Response(result)
