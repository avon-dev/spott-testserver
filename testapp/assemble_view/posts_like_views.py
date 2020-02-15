from testapp.assemble_view.__init__ import *


class Like(APIView):
    permission_classes = (IsAuthenticated,)


#좋아요 상태인지 판별할 때
    # def get(self, request, pk, format=None):
    #     post = Post.objects.get(pk = pk)
    #     post1 = Post.objects.get(pk = 2)
    #     # post.like_user.all()
    #     string = request.headers["Authorization"]
    #     decodedPayload = jwt.decode(string[4:],None,None)
    #     user = User.objects.get(user_uid = decodedPayload["id"])
    #     # user1 = User.objects.get(user_uid = 4)
    #     # user.get_like.all()
    #     user.get_like.all().values()
    #     like = PostLike.objects.filter(post = post1)
    #     return Response(str(user.get_like.all().count()))


    def post(self, request, pk, format=None):
        post = Post.objects.get(pk = pk)
        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        user = User.objects.get(user_uid = decodedPayload["id"])


        try:
            result = Return_Module.ReturnPattern.success_text\
            ("success create",result=True,count=1)
            like = PostLike.objects.get(post = post, user = user)
        # success
        except PostLike.DoesNotExist:
            like = PostLike.objects.create(post = post, user=user)
            return Response(result)
        else:
            result = json.loads(result)
            result['message'] = "already created"
            result['count'] = 0
            result = json.dumps(result)
            return Response(result)


        #포스트에서 유저 아이디가 있으면
    def delete(self, request, pk, format=None):
        post = Post.objects.get(pk = pk) #해당 포스트 가져오기

        #접속한 유저의 id 가져오기
        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        user = User.objects.get(user_uid = decodedPayload["id"])

        result = Return_Module.ReturnPattern.success_text\
        ("success delete",result=False,count=int(-1))
        try:
            like = PostLike.objects.get(post = post, user = user)
        except PostLike.DoesNotExist:
            result = json.loads(result)
            result['message'] = "already deleted"
            result['count'] = 0
            result = json.dumps(result)
            return Response(result)
        else:
            like.delete()
            return Response(result)
