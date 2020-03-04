from testapp.assemble_view.__init__ import *
from random import *

class Test(APIView):
    permission_classes = []
    def post(self, request, format=None):
        # repl = Return_Module.ReturnPattern.string_to_dict(request.data)
        # repl['nickname'] = "asdasd"
        # asd = repl['nickname']
        # result = Return_Module.ReturnPattern.success_text("Create success",**repl)
        # bb = repl.replace("'",'"')
        # json = json.loads(repl)
        # json = json.loads(aa)
        # json = json.loads(aa)
        # asd = json.loads(request.data)
        # load = json.loads(request.data)
        # loads
        # asd = json.dumps(request.data.dict())
        # serializer = TestSerializer(asd)
        # aa = request.data['sending']
        for count in range(2,12):
            user = User.objects.get(id = count)
            user_data = UserData.objects.create(user=user)
        return Response("success")


class Test2(APIView):
    permission_classes = []
    def get(self, request, format=None):
        # repl = Return_Module.ReturnPattern.string_to_dict(request.data)
        # repl['nickname'] = "asdasd"
        # asd = repl['nickname']
        # result = Return_Module.ReturnPattern.success_text("Create success",**repl)
        # bb = repl.replace("'",'"')
        # json = json.loads(repl)
        # json = json.loads(aa)
        # json = json.loads(aa)
        # asd = json.loads(request.data)
        # load = json.loads(request.data)
        # loads
        # asd = json.dumps(request.data.dict())
        # serializer = TestSerializer(asd)
        # aa = request.data['sending']
        posts_data = Post.objects.all()
        asd = posts_data.count()
        posts_data = posts_data[0:5].values()
        return Response([asd,posts_data])
            # return Response(random_string)


    @transaction.atomic
    def post(self, request, format=None):

        # request_data = Return_Module.multi_string_to_dict(request.data)
        # testdd = test.objects.create(latitude = request_data["latitude"] ,testfield = request_data["testfield"], photo = request.FILES["photo"], photo2 = request.FILES["photo2"], dummy = request_data["dummy"])
        for count in range(1,10):
            lat = uniform(35.204104,37.722390) #전국
            long = uniform(126.706945,128.983172)
            # lat = uniform(37.489324,37.626495) #서울
            # long = uniform(126.903712,127.096659)
            id = randint(2,11)
            stt = ""
            _LENGTH = 8 # 몇자리?
            string_pool = "가나다라마바사아자차카타파하거너더러머버서어저처커터퍼허"
            result = "" # 결과 값
            for i in range(_LENGTH) :
                stt += choice(string_pool)
            user = User.objects.get(id=10)
            posts = Post.objects.create(user=user,\
            latitude = lat,\
            longitude = long,\
            contents = stt,\
            posts_image = request.FILES[f'{count}'],\
            # back_image = request.FILES[f'{count}b'],\
            is_public = True)
        # posts = Post.objects.create(latitude = request.data["latitude"], longitude = request.data["longitude"],text = request.data["text"] ,posts_image = request.FILES['posts_image'], back_image = request.FILES['back_image'])
        # posts.save()
        # serializers = PostsSerializer(data = request.data)
        # if serializers.is_valid():
        #      serializers.save()
        #      asd = str(request.FILES['posts_image'].name)
        # asd = request_data["text"]
        # file = request.FILES['back_image'].content_type = 'image/jpeg'
        return Response("success", status=status.HTTP_201_CREATED)
