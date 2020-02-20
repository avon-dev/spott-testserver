from testapp.assemble_view.__init__ import *


from django.core.serializers.json import DjangoJSONEncoder



# class Home(APIView):
#     permission_classes = (IsAuthenticated,)
#     # permission_classes = []
#     def get(self, request, format=None):
#         data = Return_Module.string_to_dict(request.GET) #sending으로 묶여서 오는 파라미터 데이터 추출
#         page = data['page'] #클라이언트에서 보내주는 page count
#         craeted_time = data['created_time'] #클라이언트에서 보내주는 최신 게시물 생성 날짜
#
#         #페이징
#         begin_item = page
#         last_index = page + 21
#
#         #생성일 넘겨주는 부분
#         posts_obj = Post.objects.all().order_by('-id')[begin_item:last_index]\
#                     if craeted_time == ""\
#                     else Post.objects.filter(created__lte=craeted_time).order_by('-id')[begin_item:last_index]
#
#         posts_obj_cached = posts_obj
#
#         pageable = False if posts_obj_cached.count() < 21 else True
#
#         created_time = str(posts_obj_cached[0].created) if craeted_time == "" else craeted_time
#         home_serializers = HomeSerializer(posts_obj_cached[0:20],many=True)
#
#         dict = {"payload":{"items":home_serializers.data, "created_time":created_time, "pageable":pageable}}
#         posts_json = json.dumps(dict,cls=DjangoJSONEncoder)
#         # string = request.headers["Authorization"]
#         # decodedPayload = jwt.decode(string[4:],None,None)
#         return Response(posts_json,status=status.HTTP_200_OK)




class aaa(APIView):
    permission_classes = []
    def post(self, request, format=None):
        # a = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTg2ODY3MjI1LCJqdGkiOiJmNWFkMDU1NjU4Mzc0MmIzYjQyMWY4MGM4ZTg3NzRjOSIsImlkIjoidXNlcjhAbmF2ZXIuY29tIn0.5tJdXcBDl_AIyjzmu9ZHfrvHtugmRi-_NFUsNDKdvic"
        b = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTg4MjYwNjg4LCJqdGkiOiI3ODk2ZTVmNTYxMGY0OTBiOTQzNzBjYjNjNzBjZjI3MiIsImlkIjoidXNlcjNAbmF2ZXIuY29tIn0.Ao_nVTPMxxz0L4lHMAQT5eljrYRGAD35qgqWDI4FONg"
        # jsond = json.dumps(a)
        return Response(b)
