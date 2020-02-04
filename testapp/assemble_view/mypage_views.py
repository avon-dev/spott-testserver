from testapp.assemble_view.__init__ import *


from random import *




class MypageViewSet(APIView):
    permission_classes = []


    def get(self, request, format=None):

        user = User.objects.get(id=3)
        post = Post.objects.filter(user=user).order_by('-id')

        post_serializers = MypageSerializer(post,many=True)
        user_serializers = MyUserSerializer(user)

        # result = Return_Module.ReturnPattern.success_text("Send success",result=True,code=random_number)

        dict = {"payload":{"user":user_serializers.data,"posts":post_serializers.data},"message":"okok"}
        result = json.dumps(dict)
        return Response(result)
