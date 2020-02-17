from testapp.assemble_view.__init__ import *

from django.db import IntegrityError

class HashTagView(APIView):

    permission_classes = (IsAuthenticated,)
#

# 검색된 태그로 포스트의 객체들을 가져온다
# 유효한 게시물만 가져오도록 하게끔
    def get(self, request, format=None):
        request_data = Return_Module.string_to_dict(request.GET) #sending으로 묶여서 오는 파라미터 데이터 추출
        page = request_data['page'] #클라이언트에서 보내주는 page count
        craeted_time = request_data['created_time'] #클라이언트에서 보내주는 최신 게시물 생성 날짜
        tag_name = request_data["tag_name"]

        #페이징
        begin_item = page
        last_index = page + 31

        #생성일 넘겨주는 부분
        posts_obj = Post.objects.filter(is_active = True, problem = False, is_public = True, hashtag__name = tag_name).order_by('-id').distinct('id')[begin_item:last_index]\
                    if craeted_time == ""\
                    else Post.objects.filter(is_active = True, problem = False, is_public = True, hashtag__name = tag_name, created__lte=craeted_time).order_by('-id').distinct('id')[begin_item:last_index]

        posts_obj_cached = posts_obj

        pageable = False if posts_obj_cached.count() < 31 else True

        created_time = str(posts_obj_cached[0].created) if craeted_time == "" else craeted_time
        home_serializers = HomeSerializer(posts_obj_cached[0:30],many=True)

        result = Return_Module.ReturnPattern.success_text\
        ("show mypage", items = home_serializers.data, created_time = created_time, pageable = pageable)

        return Response(result,status=status.HTTP_200_OK)
# #페이징
# begin_item = page
# last_index = page + 21
#
# #생성일 넘겨주는 부분
# posts_obj = Post.objects.filter(is_active = True, problem = False, public = True).order_by('-id')[begin_item:last_index]\
#             if craeted_time == ""\
#             else Post.objects.filter(is_active = True, problem = False, public = True, created__lte=craeted_time).order_by('-id')[begin_item:last_index]
#
# posts_obj_cached = posts_obj
#
# pageable = False if posts_obj_cached.count() < 21 else True
#
# created_time = str(posts_obj_cached[0].created) if craeted_time == "" else craeted_time
# home_serializers = HomeSerializer(posts_obj_cached[0:20],many=True)
#
# result = Return_Module.ReturnPattern.success_text\
# ("show mypage", items = home_serializers.data, created_time = created_time, pageable = pageable)
#
# return Response(result,status=status.HTTP_200_OK)

    def post(self, request, format=None):

        # string = request.headers["Authorization"]
        # decodedPayload = jwt.decode(string[4:],None,None)
        # testdd = test.objects.create(latitude = request_data["latitude"] ,testfield = request_data["testfield"], photo = request.FILES["photo"], photo2 = request.FILES["photo2"], dummy = request_data["dummy"])

        for count in range(1600, 1680):
            try:
                posts = Post.objects.get(id =count)
            except Exception as e:
                print('잘못된 값을 넣었습니다!')
            else:
                hash_tag_name_list = ["쇼쇼"]
            # hash_tag = []

                tag_obj = HashTag.objects.all()
                tag_serial = HashTagSerializer(tag_obj, many = True)
                for list in hash_tag_name_list:
                    try:
                        hash_tag = HashTag.objects.create(name = list)
                    except  IntegrityError:
                        hash_tag = HashTag.objects.get(name = list)
                        PostTag.objects.create(post = posts, tag = hash_tag)
                        hash_tag.count += 1
                        hash_tag.save()
                        # return Response("ex")
                    else:
                        PostTag.objects.create(post = posts, tag = hash_tag)
                        hash_tag.count += 1
                        hash_tag.save()

        # hash_tag_list = request.GET['tag'][1:].split("#")
                # return Response("success")
        return Response("success")
        # create_hash = HashTag.objects.bulk_create(hash_tag)

    def patch(self, request, format=None):

        # string = request.headers["Authorization"]
        # decodedPayload = jwt.decode(string[4:],None,None)
        # testdd = test.objects.create(latitude = request_data["latitude"] ,testfield = request_data["testfield"], photo = request.FILES["photo"], photo2 = request.FILES["photo2"], dummy = request_data["dummy"])
        posts = Post.objects.get(id = 1684)
        # hash_tag_list = request.GET['tag'][1:].split("#")
        hash_tag_name_list = ['조커','머레이']
        # hash_tag = []
        # post_hash_obj = PostTag.objects.filter(post = pk).delete()
        post_hash_obj = PostTag.objects.filter(post = posts) #연결된 태그 말소
        hash_tag_list = HashTag.objects.all()

        for post_hash in post_hash_obj.values():
            hash_obj = hash_tag_list.get(id = post_hash['tag_id'])
            hash_obj.count -= 3
            hash_obj.save()
            return Response(hash_obj.count)
        # for tag_name in hash_tag_name_list:
        #     hash_tag_obj.get(name = tag_name)
        #     hash_tag_obj.count -= 1
        #     hash_tag_obj.save()
        return Response(post_hash_obj.values())
        # create_hash = HashTag.objects.bulk_create(hash_tag)
