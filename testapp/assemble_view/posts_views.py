from testapp.assemble_view.__init__ import *



from rest_framework import viewsets


from random import *

class PostViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)


    def retrieve(self, request, pk=None):
        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        posts = Post.objects.get(pk=pk)
        serializers = PostDetailSerializer(posts)
        user = User.objects.get(user_uid = decodedPayload["id"])

        comment_count = len(serializers.data['comment'])

        try:
            like = PostLike.objects.get(post = posts, user = user)
        # success
        except PostLike.DoesNotExist:
            like_checked = False
        else:
            like_checked = True

        try:
            scrap = Scrapt.objects.get(post = posts, user = user)
        # success
        except Scrapt.DoesNotExist:
            scrap_checked = False
        else:
            scrap_checked = True

        if serializers.data['user']['user_uid'] == decodedPayload["id"]:
            myself = True
        else:
            myself = False

        serial_dumps = Return_Module.jsonDumpsLoads(self,**serializers.data)
        serial_dumps['comment'] = comment_count
        serial_dumps['count'] = len(serializers.data['like_user'])
        serial_dumps['like_checked'] = like_checked
        serial_dumps['scrap_checked'] = scrap_checked
        serial_dumps['myself'] = myself
        dict = {"payload":serial_dumps,"message":"okok"}
        result = json.dumps(dict)
        #해시태그, 좋아요, 스크랩
        return Response(result)


    def create(self, request):
        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        request_data = Return_Module.multi_string_to_dict(request.data)
        # testdd = test.objects.create(latitude = request_data["latitude"] ,testfield = request_data["testfield"], photo = request.FILES["photo"], photo2 = request.FILES["photo2"], dummy = request_data["dummy"])
        user = User.objects.get(user_uid=decodedPayload["id"])
        posts = Post.objects.create(user = user,\
        latitude = request_data["latitude"],\
        longitude = request_data["longitude"],\
        contents = request_data["contents"],\
        posts_image = request.FILES['posts_image'],\
        back_image = request.FILES['back_image'],\
        public = request_data["public"])
        # posts = Post.objects.create(latitude = request.data["latitude"], longitude = request.data["longitude"],text = request.data["text"] ,posts_image = request.FILES['posts_image'], back_image = request.FILES['back_image'])
        # posts.save()
        # serializers = PostsSerializer(data = request.data)
        # if serializers.is_valid():
        #      serializers.save()
        #      asd = str(request.FILES['posts_image'].name)
        # asd = request_data["text"]
        # file = request.FILES['back_image'].content_type = 'image/jpeg'
        return Response("success", status=status.HTTP_201_CREATED)



#
    def partial_update(self, request, pk=None):
        request_data = Return_Module.string_to_dict(request.data)

        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        user = User.objects.get(user_uid = decodedPayload["id"])
        posts = Post.objects.get(pk=pk, user_id=user.id)
        serializers = PostsContentsSerializer(posts, data = request_data, partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.data, status=status.HTTP_200_CREATED)




    def destroy(self, request, pk=None):
        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)

        try:
            user = User.objects.get(user_uid = decodedPayload["id"])
            posts = Post.objects.get(pk=pk, user_id=user.id)
        except ObjectDoesNotExist:
            return Response("실패")
        else:
            posts.delete()
            return Response("성공")

    # def create(self, request):
    #
    #     # request_data = Return_Module.multi_string_to_dict(request.data)
    #     # testdd = test.objects.create(latitude = request_data["latitude"] ,testfield = request_data["testfield"], photo = request.FILES["photo"], photo2 = request.FILES["photo2"], dummy = request_data["dummy"])
    #     for count in range(1,11):
    #         lat = uniform(35.204104,37.722390) #전국
    #         long = uniform(126.706945,128.983172)
    #         # lat = uniform(37.489324,37.626495) #서울
    #         # long = uniform(126.903712,127.096659)
    #         id = randint(2,11)
    #         stt = ""
    #         _LENGTH = 8 # 몇자리?
    #         string_pool = "가나다라마바사아자차카타파하거너더러머버서어저처커터퍼허"
    #         result = "" # 결과 값
    #         for i in range(_LENGTH) :
    #             stt += choice(string_pool)
    #         user = User.objects.get(id=id)
    #         posts = Post.objects.create(user=user,\
    #         latitude = lat,\
    #         longitude = long,\
    #         contents = stt,\
    #         posts_image = request.FILES[f'{count}'],\
    #         back_image = request.FILES[f'{count}b'],\
    #         public = True)
    #     # posts = Post.objects.create(latitude = request.data["latitude"], longitude = request.data["longitude"],text = request.data["text"] ,posts_image = request.FILES['posts_image'], back_image = request.FILES['back_image'])
    #     # posts.save()
    #     # serializers = PostsSerializer(data = request.data)
    #     # if serializers.is_valid():
    #     #      serializers.save()
    #     #      asd = str(request.FILES['posts_image'].name)
    #     # asd = request_data["text"]
    #     # file = request.FILES['back_image'].content_type = 'image/jpeg'
    #     return Response("success", status=status.HTTP_201_CREATED)
