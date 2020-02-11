from testapp.assemble_view.__init__ import *



from rest_framework import viewsets
from django.core.serializers.json import DjangoJSONEncoder

from random import *

class PostViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)


    def list(self,request):
        data = Return_Module.string_to_dict(request.GET) #sending으로 묶여서 오는 파라미터 데이터 추출
        page = data['page'] #클라이언트에서 보내주는 page count
        craeted_time = data['created_time'] #클라이언트에서 보내주는 최신 게시물 생성 날짜

        #페이징
        begin_item = page
        last_index = page + 21

        #생성일 넘겨주는 부분
        posts_obj = Post.objects.all().order_by('-id')[begin_item:last_index]\
                    if craeted_time == ""\
                    else Post.objects.filter(created__lte=craeted_time).order_by('-id')[begin_item:last_index]

        posts_obj_cached = posts_obj

        pageable = False if posts_obj_cached.count() < 21 else True

        created_time = str(posts_obj_cached[0].created) if craeted_time == "" else craeted_time
        home_serializers = HomeSerializer(posts_obj_cached[0:20],many=True)

        dict = {"payload":{"items":home_serializers.data, "created_time":created_time, "pageable":pageable}}
        posts_json = json.dumps(dict,cls=DjangoJSONEncoder)
        # string = request.headers["Authorization"]
        # decodedPayload = jwt.decode(string[4:],None,None)
        return Response(posts_json,status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        posts = Post.objects.get(pk=pk)
        serializers = PostDetailSerializer(posts)
        user = User.objects.get(user_uid = decodedPayload["id"])
        print("posts" + str(posts))
        print("serial" + str(serializers.data))
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
        dict = {"payload":serial_dumps,"message":"show posts detail success"}
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

        result = Return_Module.ReturnPattern.success_text\
        ("create success",success=True)

        try:
            hash_tag_list = request_data['tag'][1:].split("#")
        except Exception as e:
            return Response(result, status=status.HTTP_201_CREATED)


        hash_tag_obj_list = []
        for count in range(0,len(hash_tag_list)):
            hash_tag.append(HashTag(user = user, post = posts, tag_name = hash_tag_list[count]))

        HashTag.objects.bulk_create(hash_tag)


        return Response(result, status=status.HTTP_201_CREATED)



#
    def partial_update(self, request, pk=None):
        request_data = Return_Module.string_to_dict(request.data)

        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        user = User.objects.get(user_uid = decodedPayload["id"])
        posts = Post.objects.get(pk=pk, user_id=user.id)
        serializers = PostsContentsSerializer(posts, data = request_data, partial=True)

        result = Return_Module.ReturnPattern.success_text\
        ("partial_update success",result=True)


        try:
            hash_tag_list = request_data['tag'][1:].split("#")
        except Exception as e:
            return Response(result, status=status.HTTP_201_CREATED)


        hash_tag_obj_list = []
        for count in range(0,len(hash_tag_list)):
            hash_tag.append(HashTag(user = user, post = posts, tag_name = hash_tag_list[count]))
        hash_t = HashTag.objects.filter(user_id = user.id, post = pk).delete()
        HashTag.objects.bulk_create(hash_tag)

        if serializers.is_valid():
            serializers.save()
            return Response(result, status=status.HTTP_201_CREATED)
        result = Return_Module.ReturnPattern.success_text\
        ("partial_update fail",result=False)
        return Response(result, status=status.HTTP_200_CREATED)




    def destroy(self, request, pk=None):
        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)

        try:
            user = User.objects.get(user_uid = decodedPayload["id"])
            posts = Post.objects.get(pk=pk, user_id=user.id)
        except ObjectDoesNotExist:
            result = Return_Module.ReturnPattern.success_text\
            ("delete fail",result=False)
            return Response(result)
        else:
            result = Return_Module.ReturnPattern.success_text\
            ("delete success",result=True)
            posts.delete()
            return Response(result)

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