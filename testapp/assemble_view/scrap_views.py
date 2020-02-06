from testapp.assemble_view.__init__ import *

class Scrap(APIView):
    permission_classes = (IsAuthenticated,)


#좋아요 상태인지 판별할 때
    def get(self, request, pk, format=None):
        post = Post.objects.get(pk = pk)
        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        user = User.objects.get(user_uid = decodedPayload["id"])
        return Response(str(user.get_like.all().count()))


    def post(self, request, pk, format=None):
        post = Post.objects.get(pk = pk)
        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        user = User.objects.get(user_uid = decodedPayload["id"])
        # user_data = UserData.objects.get(user = user)

        try:
            result = Return_Module.ReturnPattern.success_text\
            ("success create",result=True, count=1)
            scrap = Scrapt.objects.get(user = user, post = post)
        # success
        except ObjectDoesNotExist:
            scrap = Scrapt.objects.create(post = post, user=user)
            return Response(result)
        else:
            result = json.loads(result)
            result['message'] = "already created"
            result['payload']['count'] = 0
            result = json.dumps(result)
        return Response(result)


        #포스트에서 유저 아이디가 있으면
    def delete(self, request, pk, format=None):
        post = Post.objects.get(pk = pk) #해당 포스트 가져오기

        #접속한 유저의 id 가져오기
        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        user = User.objects.get(user_uid = decodedPayload["id"])
        # user_data = UserData.objects.get(user = user)

        result = Return_Module.ReturnPattern.success_text\
        ("success delete",result=False ,count=-1)
        try:
            scrap = Scrapt.objects.get(post = post, user = user)
        except ObjectDoesNotExist:
            result = json.loads(result)
            result['message'] = "already deleted"
            result['payload']['count'] = 0
            result = json.dumps(result)
            return Response(result)
        else:
            scrap.delete()
            return Response(result)



class MultiScrap(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        user = User.objects.get(user_uid = decodedPayload["id"])
        scrap = Scrapt.objects.filter(user_id = user.id)
        # serial = ScrapAllSerializer(user.get_scrap.all().order_by('scrap_users__id'),many=True)
        serial = ScrapSerializer(scrap,many=True)
        dict = {"payload":serial.data,"message":"success"}
        result = json.dumps(dict)
        return Response(result)

        #아이디 값을 받아 온 뒤 리스트에서 뽑아서 딜리트
    def delete(self, request, format=None):

        request_data = Return_Module.string_to_dict(request.GET)
        ids = request_data['ids'].split(',')

        for num in range(0,len(ids)):
            ids[num]=int(ids[num])

        post = Post.objects.filter(pk__in = ids).delete() #해당 포스트 가져오기
        dict = {"payload":post,"message":"success"}
        result = json.dumps(dict)
        return Response(result)

        # result = Return_Module.ReturnPattern.success_text\
        # ("success delete",result=False ,count=-1)
        # try:
        #     scrap = Scrapt.objects.get(post = post, user = user)
        # except ObjectDoesNotExist:
        #     result = json.loads(result)
        #     result['message'] = "already deleted"
        #     result['payload']['count'] = 0
        #     result = json.dumps(result)
        #     return Response(result)
        # else:
        #     scrap.delete()
        #     return Response(result)
