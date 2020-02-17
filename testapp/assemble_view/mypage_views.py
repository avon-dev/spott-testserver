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

        user = User.objects.get(is_active = True, pk = pk)
        post = Post.objects.filter(is_active = True, problem = False, is_public = True, user = user).order_by('-id')

        post_serializers = MypageSerializer(post,many=True)
        user_serializers = MyUserSerializer(user)

        # result = Return_Module.ReturnPattern.success_text("Send success",result=True,code=random_number)
        result = Return_Module.ReturnPattern.success_text\
        ("show user mypage", user = user_serializers.data, posts = post_serializers.data)
        # dict = {"payload":{"user":user_serializers.data,"posts":post_serializers.data},"message":"success"}
        # result = json.dumps(dict)
        return Response(result)
