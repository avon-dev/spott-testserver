from testapp.assemble_view.__init__ import *


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



# class Home(APIView):
#페이징 번호, 정렬 방식,
