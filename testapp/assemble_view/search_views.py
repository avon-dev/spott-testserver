from testapp.assemble_view.__init__ import *



class SearchView(APIView):

    permission_classes = ()
#




# #으로 검색을 했을 시에는 해쉬태그로 검색
    def get(self, request, format=None):

        word = request.GET['search_word']
        is_tag = request.GET['tag']
        if is_tag:
            user = User.objects.filter(nickname__istartswith = word)
            tag = HashTag.objects.filter(tag_name__istartswith = word).distinct('tag_name')

        serializers = SearchTagSerializer(tag,many=True)
        nickname = SearchNameSerializer(user,many=True)
        return Response(nickname.data +serializers.data)
