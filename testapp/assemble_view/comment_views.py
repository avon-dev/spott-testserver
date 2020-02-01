from testapp.assemble_view.__init__ import *


from rest_framework import viewsets


class CommentViewSet(viewsets.ViewSet):
    permission_classes = []


    def retrieve(self, request, pk=None):
        queryset = Post.objects.all()
        posts = Post.objects.get(pk=pk)
        serializers = PostDetailSerializer(posts)
        # user = User.objects.get(id=3).get_user.all()
        # user.post_set.all()
        asd = serializers.data['comment']
        return Response(asd)

    def create(self, request):
        user = User.objects.get(id = 5)
        post = Post.objects.get(id = 20)
        comment = Comment.objects.create(user=user, post = post, contents="5번 유저가 20번 게시물에 등록")
        return Response("success", status=status.HTTP_201_CREATED)
