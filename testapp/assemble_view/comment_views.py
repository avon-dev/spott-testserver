
from testapp.assemble_view.__init__ import *




class CommentView(APIView):
    permission_classes = (IsAuthenticated,)


#좋아요 상태인지 판별할 때
    def get(self, request, pk, format=None):
        post = Post.objects.get(pk = pk)

        return Response(str(post.comment))


    def post(self, request, pk, format=None):
        post = Post.objects.get(pk = pk)
        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        user = User.objects.get(user_uid = decodedPayload["id"])
        request_data = Return_Module.string_to_dict(request.data)

        # success
        comment = Comment.objects.create(post = post, user=user, contents=request_data['caption'])

        result = Return_Module.ReturnPattern.success_text\
        ("success create",result=True)
        return Response(result)


        #포스트에서 유저 아이디가 있으면
    def delete(self, request, pk, format=None):
        post = Post.objects.get(pk = pk) #해당 포스트 가져오기

        #접속한 유저의 id 가져오기
        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        user = User.objects.get(user_uid = decodedPayload["id"])
        # user_data = UserData.objects.get(user = user)

        result = Return_Module.ReturnPattern.success_text\
        ("success delete",result=False)
        try:
            comment = Comment.objects.get(post = post, user = user)
        except ObjectDoesNotExist:
            result = json.loads(result)
            result['message'] = "already deleted"
            result = json.dumps(result)
            return Response(result)
        else:
            comment.delete()
            return Response(result)
