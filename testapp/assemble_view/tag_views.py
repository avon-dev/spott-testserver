from testapp.assemble_view.__init__ import *



class HashTagView(APIView):

    permission_classes = (IsAuthenticated,)
#

#검색된 태그로 포스트의 객체들을 가져온다
#유효한 게시물만 가져오도록 하게끔
    def get(self, request, format=None):
        tag_name = request.GET["tag_name"]
        tag = HashTag.objects.filter(tag_name = tag_name)
        tag_list = TagListSerializer(tag, many = True)
        # post = Post.objects.filter(id__in = tag_list).distinct('id')
        # serializers = PostSerializer(post, many = True)
        result = Return_Module.ReturnPattern.success_list_text\
        ("success",tag_list.data)
        return Response(result)


    def post(self, request, format=None):

        # string = request.headers["Authorization"]
        # decodedPayload = jwt.decode(string[4:],None,None)
        # testdd = test.objects.create(latitude = request_data["latitude"] ,testfield = request_data["testfield"], photo = request.FILES["photo"], photo2 = request.FILES["photo2"], dummy = request_data["dummy"])
        user = User.objects.get(id=8)
        posts = Post.objects.get(id = 1655)
        # hash_tag_list = request.GET['tag'][1:].split("#")
        hash_tag_name_list = ["이치원", "지코", "지아코", "치아코", "아이유"]
        hash_tag = []
        for count in range(0,len(hash_tag_name_list)):
            hash_tag.append(HashTag(user = user, post = posts, tag_name = hash_tag_name_list[count]))


        create_hash = HashTag.objects.bulk_create(hash_tag)

        return Response("success")
