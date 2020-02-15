from testapp.assemble_view.__init__ import *



class SearchView(APIView):

    permission_classes = (IsAuthenticated,)
#




# #으로 검색을 했을 시에는 해쉬태그로 검색 아이템 하나로
    def get(self, request, format=None):
        request_data = Return_Module.string_to_dict(request.GET)
        word = request_data['search_word']
        is_tag = request_data['tag']
        if is_tag:
            tag_obj = HashTag.objects.filter(tag_name__istartswith = word).distinct('tag_name')[:16]
            tag_serializer = SearchTagSerializer(tag_obj, many = True)
            result = Return_Module.ReturnPattern.success_list_text\
            ("Search success", *tag_serializer.data)
            return Response(result)
        else:
            user_obj = User.objects.filter(is_active = True, nickname__istartswith = word)
            tag_obj = HashTag.objects.filter(tag_name__istartswith = word).distinct('tag_name')
            tag_serializer = SearchTagSerializer(tag_obj,many=True)
            user_serializer = SearchNameSerializer(user_obj,many=True)
            result = Return_Module.ReturnPattern.success_text\
            ("Search success", tag = tag_serializer.data, user = user_serializer.data)
            return Response(result)


        # user= User.objects.all()
        # user[0].user_hashtag.all()
        # # tag_obj = HashTag.objects.all().select_related()
        # # tag_serializer = SerialTest(tag_obj,many=True)
        # # print(str(tag_obj[0].query())
        # # print(tag_obj.query)
        # return Response(str(user))
