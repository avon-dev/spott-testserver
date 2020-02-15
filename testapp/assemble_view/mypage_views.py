from testapp.assemble_view.__init__ import *


from random import *




class MypageViewSet(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        user = User.objects.get(is_active = True, user_uid = decodedPayload["id"])
        post = Post.objects.filter(problem = False, is_active = True, user=user).order_by('-id')

        post_serializers = MypageSerializer(post, many = True)
        user_serializers = MyUserSerializer(user)


        result = Return_Module.ReturnPattern.success_text\
        ("show mypage", user = user_serializers.data, posts = post_serializers.data)
        return Response(result)


class UserMypageViewSet(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):

        user = User.objects.get(is_active = True, pk = pk)
        post = Post.objects.filter(is_active = True, problem = False, public = True, user = user).order_by('-id')

        post_serializers = MypageSerializer(post,many=True)
        user_serializers = MyUserSerializer(user)

        # result = Return_Module.ReturnPattern.success_text("Send success",result=True,code=random_number)
        result = Return_Module.ReturnPattern.success_text\
        ("show user mypage", user = user_serializers.data, posts = post_serializers.data)
        # dict = {"payload":{"user":user_serializers.data,"posts":post_serializers.data},"message":"success"}
        # result = json.dumps(dict)
        return Response(result)
