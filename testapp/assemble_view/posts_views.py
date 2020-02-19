from testapp.assemble_view.__init__ import *



from rest_framework import viewsets
from django.core.serializers.json import DjangoJSONEncoder
from django.db import IntegrityError
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
        posts_obj = Post.objects.filter(is_active = True, problem = False, is_public = True).order_by('-id')[begin_item:last_index]\
                    if craeted_time == ""\
                    else Post.objects.filter(is_active = True, problem = False, is_public = True, created__lte=craeted_time).order_by('-id')[begin_item:last_index]

        posts_obj_cached = posts_obj

        pageable = False if posts_obj_cached.count() < 21 else True

        created_time = str(posts_obj_cached[0].created) if craeted_time == "" else craeted_time
        home_serializers = HomeSerializer(posts_obj_cached[0:20],many=True)

        result = Return_Module.ReturnPattern.success_text\
        ("show mypage", items = home_serializers.data, created_time = created_time, pageable = pageable)

        return Response(result,status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        result_dict = {"success":12000,"report":12001,"failed 404":14040}
        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        try:
            posts = Post.objects.get(problem = False, is_active = True, pk = pk)
        except Exception as e:
            result = Return_Module.ReturnPattern.success_text\
            ("posts_get fail",result=result_dict['failed 404'])
            return Response(result, status = status.HTTP_404_NOT_FOUND)
        report_all = Report.objects.all()
        comment = Comment.objects.filter(post = posts)
        report_comment = report_all.filter(reporter_id = decodedPayload['id'],comment__in = comment, handling = 3).values('comment_id')
        report_post = report_all.filter(reporter_id = decodedPayload['id'], post = posts, handling = 1)
        if report_post:
            result = Return_Module.ReturnPattern.success_text\
            ("reported posts",result = result_dict["report"])
            return Response(result)
        else:
            serializers = PostDetailSerializer(posts)
            user = User.objects.get(is_active = True, user_uid = decodedPayload["id"])
            # print("posts" + str(posts))
            # print("serial" + str(serializers.data))
            comment_count = len(Comment.objects.filter(is_active = True,\
            post_id = pk, is_problem = False).exclude(id__in= report_comment))

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
            result = Return_Module.ReturnPattern.success_text\
            ("show posts detail success",**serial_dumps, result = result_dict["success"])
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
        is_public = True)

        result = Return_Module.ReturnPattern.success_text\
        ("create success",success=True)

        try:
            hash_tag_name_list = request_data['tag'][1:].split("#")
            print(str(hash_tag_name_list))
        except Exception as e:
            return Response(result, status=status.HTTP_201_CREATED)


        for tag_name in hash_tag_name_list:
            try:
                hash_tag_list = HashTag.objects.create(name = tag_name)
            except  IntegrityError:
                hash_tag_list = HashTag.objects.get(name = tag_name)
                PostTag.objects.create(post = posts, tag = hash_tag_list)
                hash_tag_list.count += 1
                hash_tag_list.save()
                # return Response("ex")
            else:
                PostTag.objects.create(post = posts, tag = hash_tag_list)
                hash_tag_list.count += 1
                hash_tag_list.save()


        return Response(result, status=status.HTTP_201_CREATED)



#
    def partial_update(self, request, pk=None):
        request_data = Return_Module.multi_string_to_dict(request.data)
        contents =  {"contents":request_data['contents']}
        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        user = User.objects.get(user_uid = decodedPayload["id"])
        posts = Post.objects.get(pk=pk, user_id=user.id)
        serializers = PostsContentsSerializer(posts, data = contents, partial=True)

        result = Return_Module.ReturnPattern.success_text\
        ("partial_update success",result=True)

        print(request_data['contents'])
        try:
            hash_tag_name_list = request_data['tag'][1:].split("#")
        except Exception as e:
            if serializers.is_valid():
                post_hash_list = PostTag.objects.filter(post = posts)#연결된 태그 말소
                hash_tag_list = HashTag.objects.all() #태그 테이블 데이터 불러오기

                for post_hash in post_hash_list.values():
                    hash_obj = hash_tag_list.get(id = post_hash['tag_id'])

                    hash_count = hash_obj.count - 1
                    if hash_count <= 0:
                        hash_obj.delete()
                    else:
                        hash_obj.count = hash_count
                        hash_obj.save()
                post_hash_list.delete()
                serializers.save()
                return Response(result, status=status.HTTP_201_CREATED)
            result = Return_Module.ReturnPattern.success_text\
            ("partial_update fail",result=False)
            return Response(result, status=status.HTTP_404_NOT_FOUND)

        else:
            post_hash_list = PostTag.objects.filter(post = posts)#연결된 태그 말소
            hash_tag_list = HashTag.objects.all() #태그 테이블 데이터 불러오기

            for post_hash in post_hash_list.values():
                hash_obj = hash_tag_list.get(id = post_hash['tag_id'])

                hash_count = hash_obj.count - 1
                if hash_count <= 0:
                    hash_obj.delete()
                else:
                    hash_obj.count = hash_count
                    hash_obj.save()
            post_hash_list.delete()

            # print(hash_tag_name_list)
            for tag_name in hash_tag_name_list:
                try:
                    hash_tag_list = HashTag.objects.create(name = tag_name)
                except  IntegrityError:
                    hash_tag_list = HashTag.objects.get(name = tag_name)
                    PostTag.objects.create(post = posts, tag = hash_tag_list)
                    hash_tag_list.count += 1
                    hash_tag_list.save()
                    # return Response("ex")
                else:
                    PostTag.objects.create(post = posts, tag = hash_tag_list)
                    hash_tag_list.count += 1
                    hash_tag_list.save()





            if serializers.is_valid():
                serializers.save()
                return Response(result, status=status.HTTP_201_CREATED)
            result = Return_Module.ReturnPattern.success_text\
            ("partial_update fail",result=False)
            return Response(result, status=status.HTTP_404_NOT_FOUND)




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
            posts.is_active = False
            posts.save()


            post_hash_list = PostTag.objects.filter(post = posts)#연결된 태그 조회
            hash_tag_list = HashTag.objects.all() #태그 테이블 데이터 불러오기

            for post_hash in post_hash_list.values():
                hash_obj = hash_tag_list.get(id = post_hash['tag_id'])

                hash_count = hash_obj.count - 1
                if hash_count <= 0:
                    hash_obj.delete()
                else:
                    hash_obj.count = hash_count
                    hash_obj.save()

            post_hash_list.delete()
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
