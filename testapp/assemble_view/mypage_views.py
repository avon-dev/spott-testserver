from testapp.assemble_view.__init__ import *


from random import *




class MypageViewSet(APIView):

    permission_classes = (IsAuthenticated,)
    request_data_key = ['is_public']
    def get(self, request, format=None):
        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        user = User.objects.get(is_active = True, user_uid = decodedPayload["id"])
        post = Post.objects.filter(problem = False, is_active = True, user = user).order_by('-id')

        post_serializers = MypageSerializer(post, many = True)
        user_serializers = MyUserSerializer(user)


        result = Return_Module.ReturnPattern.success_text\
        ("show mypage", user = user_serializers.data, posts = post_serializers.data)
        return Response(result)

    def patch(self, request, format=None):
        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        request_data = Return_Module.string_to_dict(request.data) #sending으로 묶여서 오는 파라미터 데이터 추출

        user = User.objects.get(is_active = True, user_uid = decodedPayload["id"]).update(is_public = request_data[self.request_data_key[0]])
        post = Post.objects.filter(user = user).update(is_public = request_data[self.request_data_key[0]])

        if request_data[self.request_data_key[0]]:
            result = Return_Module.ReturnPattern.success_text\
            ("account public" , public = True)
            return Response(result)
        else:
            result = Return_Module.ReturnPattern.success_text\
            ("account private" , public = False)
            return Response(result)




class UserMypageViewSet(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):

        request_data = Return_Module.string_to_dict(request.GET) #sending으로 묶여서 오는 파라미터 데이터 추출
        action = request_data['action']
        action_search = 1201
        action_user_mypage = 1202
        user = User.objects.get(is_active = True, pk = pk)
        post = Post.objects.filter(is_active = True, problem = False, is_public = True, user = user).order_by('-id')

        post_serializers = MypageSerializer(post,many=True)
        user_serializers = MyUserSerializer(user)

        # result = Return_Module.ReturnPattern.success_text("Send success",result=True,code=random_number)
        result = Return_Module.ReturnPattern.success_text\
        ("show user mypage", user = user_serializers.data, posts = post_serializers.data)
        # dict = {"payload":{"user":user_serializers.data,"posts":post_serializers.data},"message":"success"}
        # result = json.dumps(dict)

        if action == action_search:
            string = request.headers["Authorization"]
            decodedPayload = jwt.decode(string[4:],None,None)
            user = User.objects.get(user_uid = decodedPayload['id'])
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
            ("search success", user = user_serializers.data, posts = post_serializers.data)
            return Response(result,status=status.HTTP_201_CREATED)
        return Response(result)
