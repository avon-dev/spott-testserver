from testapp.assemble_view.__init__ import *



from rest_framework import viewsets
from django.core.serializers.json import DjangoJSONEncoder
from django.db import IntegrityError
from random import *

class PostViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)


    def list(self,request):
        actions = ['action']
        # sending으로 안 묶여 있으면 에러 처리
        try:
            request_data = Return_Module.string_to_dict(request.GET) #sending 파라미터에서 value 추출해서 dict 형태로 변형
        except KeyError as e:
            # print(f"key error: missing key name {e}") #에러 로그
            result = Error_Module.ErrorHandling.none_bundle(req.request_bundle, e) #클라이언트에 보낼 에러 메시지
            return Response(result,status = status.HTTP_400_BAD_REQUEST)

        try:
            request_data[actions[0]]
        except KeyError as e:
            error_dict = Error_Module.ErrorHandling.none_feild(actions,request_data.keys(), e)
            result = Return_Module.ReturnPattern.error_text(error_dict)
            return Response(result,status = status.HTTP_400_BAD_REQUEST)
        else:
            action = request_data[actions[0]] #####수정


        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        user = User.objects.get(is_active = True, user_uid = decodedPayload["user_uid"])
        report = Report.objects.filter(handling = Report.before_posts, reporter= user)


        if action == req.show_posts_home:

            posts_show_list_keys = ["created_time", "page"]



            #필드에 필수 키가 있는지 확인 후 없을 경우 에러 반환
            try:
                for key in posts_show_list_keys:
                    request_data[key]
            except KeyError as e:
                error_dict = Error_Module.ErrorHandling.none_feild(posts_show_list_keys,request_data.keys(), e)
                result = Return_Module.ReturnPattern.error_text(error_dict)
                return Response(result,status = status.HTTP_400_BAD_REQUEST)
            else:
                page = request_data[posts_show_list_keys[1]] #클라이언트에서 보내주는 page count
                craeted_time = request_data[posts_show_list_keys[0]] #클라이언트에서 보내주는 최신 게시물 생성 날짜



            #페이징
            begin_item = page
            last_index = page + 30
            print(Report.rel_name)
            #생성일 넘겨주는 부분

            posts_obj = Post.objects.filter(handling = Post.no_problem, is_active = True,problem = False, is_public = True, post_kind = Post.basic_post)\
                        .exclude(phopo_reports_post_related__in = report)\
                        .order_by('-id')[begin_item:last_index]\
                        if craeted_time == ""\
                        else Post.objects.filter(handling = Post.no_problem, is_active = True, problem = False,\
                         is_public = True, created__lte=craeted_time, post_kind = Post.basic_post).\
                         exclude(phopo_reports_post_related__in = report).\
                         order_by('-id')[begin_item:last_index]
# .exclude(id = report_post)\
            posts_obj_cached = posts_obj

            pageable = False if posts_obj_cached.count() < 30 else True

            try:
                created_time = str(posts_obj_cached[0].created) if craeted_time == "" else craeted_time
            except IndexError as e:
                result = Return_Module.ReturnPattern.success_text\
                ("empty list",items = [], created_time = "", pageable = pageable)
                return Response(result,status=status.HTTP_200_OK)
            else:
                home_serializers = HomeSerializer(posts_obj_cached[0:29],many=True)
                result = Return_Module.ReturnPattern.success_text\
                ("show posts list", items = home_serializers.data, created_time = created_time, pageable = pageable)
                return Response(result,status=status.HTTP_200_OK)


        else:

            posts_show_list_keys = ["lat_ne", "lat_sw", "lng_ne", "lng_sw" ]
            # sending으로 안 묶여 있으면 에러 처리
            try:
                request_data = Return_Module.string_to_dict(request.GET) #sending 파라미터에서 value 추출해서 dict 형태로 변형
            except KeyError as e:
                # print(f"key error: missing key name {e}") #에러 로그
                result = Error_Module.ErrorHandling.none_bundle(req.request_bundle, e) #클라이언트에 보낼 에러 메시지
                return Response(result,status = status.HTTP_400_BAD_REQUEST)


            #필드에 필수 키가 있는지 확인 후 없을 경우 에러 반환
            try:
                for key in posts_show_list_keys:
                    request_data[key]
            except KeyError as e:
                error_dict = Error_Module.ErrorHandling.none_feild(posts_show_list_keys,request_data.keys(), e)
                result = Return_Module.ReturnPattern.error_text(error_dict)
                return Response(result,status = status.HTTP_400_BAD_REQUEST)
            else:
                lat_ne = request_data[posts_show_list_keys[0]]
                lng_ne = request_data[posts_show_list_keys[2]]
                lat_sw = request_data[posts_show_list_keys[1]]
                lng_sw = request_data[posts_show_list_keys[3]]

            posts_data = Post.objects.filter(handling = 22001 ,is_active = True, problem = False, \
            is_public = True, latitude__range=[lat_sw,lat_ne],longitude__range=[lng_sw,lng_ne]).\
            exclude(phopo_reports_post_related__in = report).\
            order_by('-like_count')
            serializers = PostSerializer(posts_data, many = True)
            result = Return_Module.ReturnPattern.success_list_text\
            ("show posts list(lat,long)", *serializers.data)
            return Response(result)


    def retrieve(self, request, pk=None):
        result_dict = {"success":1200,"report":1201,"failed 404":1404}
        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)

        user = User.objects.get(is_active = True, user_uid = decodedPayload["user_uid"]) #나중에 에러처리 넣어야됨

        try:

            posts = Post.objects.get(problem = False, is_active = True, pk = pk)
        except Post.DoesNotExist as e:
            result = Return_Module.ReturnPattern.error_text(str(e))
            return Response(result, status = status.HTTP_404_NOT_FOUND)

        report_all = Report.objects.all()
        comment = Comment.objects.filter(post = posts)
        report_comment = report_all.filter(reporter_id = decodedPayload['user_uid'],comment__in = comment, handling = Report.before_comment).values('comment_id')
        report_post = report_all.filter(reporter_id = decodedPayload['user_uid'], post = posts, handling = Report.before_posts)
        print(f'레포트 코멘트: {report_comment}')
        print(f'레포트 포스트: {report_post}')

        if report_post:#내가 신고 한 게시물일 경우
            result = Return_Module.ReturnPattern.success_text\
            ("reported posts",result = result_dict["report"])
            return Response(result)
        else:
            serializers = PostDetailSerializer(posts)
            user = User.objects.get(is_active = True, user_uid = decodedPayload["user_uid"])
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

            if serializers.data['user']['email'] == user.email:
                myself = True
            else:
                myself = False

            serial_dumps = Return_Module.jsonDumpsLoads(self,**serializers.data)
            serial_dumps['comment'] = comment_count
            serial_dumps['count'] = serializers.data['like_count']
            serial_dumps['like_checked'] = like_checked
            serial_dumps['scrap_checked'] = scrap_checked
            serial_dumps['myself'] = myself
            serial_dumps['is_superuser'] = user.is_superuser
            result = Return_Module.ReturnPattern.success_text\
            ("show posts detail success",**serial_dumps, result = result_dict["success"])
            return Response(result)



    @transaction.atomic
    def create(self, request):
        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        posts_required_keys = ["latitude", "longitude", "contents"]

        # sending으로 안 묶여 있으면 에러 처리
        try:
            request_data = Return_Module.multi_string_to_dict(request.data) #sending 파라미터에서 value 추출해서 dict 형태로 변형
        except KeyError as e:
            # print(f"key error: missing key name {e}") #에러 로그
            result = Error_Module.ErrorHandling.none_bundle(req.request_bundle, e) #클라이언트에 보낼 에러 메시지
            return Response(result,status = status.HTTP_400_BAD_REQUEST)

        try:
            for key in posts_required_keys:
                request_data[key]
        except KeyError as e:
            error_dict = Error_Module.ErrorHandling.none_feild(posts_required_keys,request_data.keys(), e)
            result = Return_Module.ReturnPattern.error_text(error_dict)
            return Response(result,status = status.HTTP_400_BAD_REQUEST)
        else:
            lat = request_data[posts_required_keys[0]]
            lng = request_data[posts_required_keys[1]]
            contents = request_data[posts_required_keys[2]]
            posts_image = request.FILES.get('posts_image',None)
            back_image = request.FILES.get('back_image',None)

        # testdd = test.objects.create(latitude = request_data["latitude"] ,testfield = request_data["testfield"], photo = request.FILES["photo"], photo2 = request.FILES["photo2"], dummy = request_data["dummy"])
        user = User.objects.get(user_uid=decodedPayload["user_uid"])

        if user.is_superuser:
            posts = Post.objects.create(user = user,\
            post_kind = Post.admin_post,\
            latitude = lat,\
            longitude = lng,\
            contents = contents,\
            posts_image = posts_image,\
            back_image = back_image,\
            handling = Post.no_problem,\
            is_public = True)
        else:
            posts = Post.objects.create(user = user,\
            latitude = lat,\
            longitude = lng,\
            contents = contents,\
            posts_image = posts_image,\
            back_image = back_image,\
            handling = Post.no_problem,\
            is_public = True)

        result = Return_Module.ReturnPattern.success_text\
        ("create success",success=True)

        try:
            hash_tag_name_list = request_data['tag'][1:].split("#")
            print(str(hash_tag_name_list))
        except Exception as e:
            return Response(result, status=status.HTTP_201_CREATED)


        for tag_name in hash_tag_name_list:
            tag_exist = orm.tag_exist(self, tag_name.lower())
            if tag_exist:
                hashTag_obj = HashTag.objects.get(name = tag_name.lower())
                PostTag.objects.create(post = posts, tag = hashTag_obj)
                hashTag_obj.count += 1
                hashTag_obj.save()
            else:
                hashTag_obj = HashTag.objects.create(name = tag_name.lower())
                PostTag.objects.create(post = posts, tag = hashTag_obj)
                hashTag_obj.count += 1
                hashTag_obj.save()


        return Response(result, status=status.HTTP_201_CREATED)



    @transaction.atomic
    def partial_update(self, request, pk=None):
        posts_required_keys = ["contents"]

        # sending으로 안 묶여 있으면 에러 처리
        try:
            request_data = Return_Module.multi_string_to_dict(request.data) #sending 파라미터에서 value 추출해서 dict 형태로 변형
        except KeyError as e:
            # print(f"key error: missing key name {e}") #에러 로그
            result = Error_Module.ErrorHandling.none_bundle(req.request_bundle, e) #클라이언트에 보낼 에러 메시지
            return Response(result,status = status.HTTP_400_BAD_REQUEST)

        try:
            for key in posts_required_keys:
                request_data[key]
        except KeyError as e:
            error_dict = Error_Module.ErrorHandling.none_feild(posts_required_keys,request_data.keys(), e)
            result = Return_Module.ReturnPattern.error_text(error_dict)
            return Response(result,status = status.HTTP_400_BAD_REQUEST)
        else:
            contents =  {"contents":request_data['contents']}


        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        user = User.objects.get(user_uid = decodedPayload["user_uid"])
        posts = Post.objects.get(pk=pk, user_id=user.id)
        serializers = PostsContentsSerializer(posts, data = contents, partial=True)

        result = Return_Module.ReturnPattern.success_text\
        ("partial_update success",result=True)

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
            print(f"연결된 태그 {post_hash_list}")
            hash_tag_list = HashTag.objects.all() #태그 테이블 데이터 불러오기
            print(f" 태그 리스트{hash_tag_list}")
            for post_hash in post_hash_list.values():
                hash_obj = hash_tag_list.get(id = post_hash['tag_id'])

                hash_count = hash_obj.count - 1
                if hash_count <= 0:
                    hash_obj.delete()
                else:
                    hash_obj.count = hash_count
                    hash_obj.save()
            post_hash_list.delete()
            print("for 문 끝나는 부분")
            # print(hash_tag_name_list)

            for tag_name in hash_tag_name_list:
                tag_exist = orm.tag_exist(self, tag_name.lower())
                if tag_exist:
                    hashTag_obj = HashTag.objects.get(name = tag_name.lower())
                    PostTag.objects.create(post = posts, tag = hashTag_obj)
                    hashTag_obj.count += 1
                    hashTag_obj.save()
                else:
                    hashTag_obj = HashTag.objects.create(name = tag_name.lower())
                    PostTag.objects.create(post = posts, tag = hashTag_obj)
                    hashTag_obj.count += 1
                    hashTag_obj.save()
            print("태그 처리 완료")

            if serializers.is_valid():
                print("게시물 수정 완료")
                serializers.save()
                return Response(result, status=status.HTTP_201_CREATED)
            result = Return_Module.ReturnPattern.success_text\
            ("partial_update fail",result=False)
            return Response(result, status=status.HTTP_404_NOT_FOUND)



    @transaction.atomic
    def destroy(self, request, pk=None):
        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)

        try:
            user = User.objects.get(user_uid = decodedPayload["user_uid"])
            posts = Post.objects.get(pk=pk, user_id=user.id)
        except ObjectDoesNotExist as e:
            result = Return_Module.ReturnPattern.error_text(str(e))
            return Response(result,status = status.HTTP_404_NOT_FOUND)
        else:
            result = Return_Module.ReturnPattern.success_text\
            ("delete success",result=True)
            notice = Notice.objects.filter(post = posts, kind = Notice.created_comment).delete()
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






class PhopoRecommendationViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)


    def list(self,request):

        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        user = User.objects.get(is_active = True, user_uid = decodedPayload["user_uid"])

        psot = Post.objects.filter(is_active = True, problem = False, is_public = True, post_kind = Post.admin_post).order_by('-id')



        home_serializers = HomeSerializer(psot,many=True)
        result = Return_Module.ReturnPattern.success_text\
        ("show recommendation list", items = home_serializers.data)
        return Response(result,status=status.HTTP_200_OK)
































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
