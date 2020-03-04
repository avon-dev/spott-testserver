from testapp.assemble_view.__init__ import *

class Scrap(APIView):
    permission_classes = (IsAuthenticated,)


    # def get(self, request, pk, format=None):
    #     post = Post.objects.get(pk = pk)
    #     string = request.headers["Authorization"]
    #     decodedPayload = jwt.decode(string[4:],None,None)
    #     user = User.objects.get(user_uid = decodedPayload["id"])
    #     return Response(str(user.get_like.all().count()))

    @transaction.atomic
    def post(self, request, pk, format=None):
        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        try:
            user = User.objects.get(user_uid = decodedPayload["id"])
            post = Post.objects.get(pk=pk)
        except ObjectDoesNotExist as e:
            result = Return_Module.ReturnPattern.error_text(str(e))
            return Response(result,status = status.HTTP_404_NOT_FOUND)
        print(decodedPayload['id'])
        # user_data = UserData.objects.get(user = user)

        try:
            result = Return_Module.ReturnPattern.success_text\
            ("success create",result=True, count=1)
            scrap = Scrapt.objects.get(user = user, post = post)
        # success
        except ObjectDoesNotExist:
            scrap = Scrapt.objects.create(post = post, user=user)
            return Response(result, status = status.HTTP_201_CREATED)
        else:
            result = json.loads(result)
            result['message'] = "already created"
            result['payload']['count'] = 0
            result = json.dumps(result)

        print(str(scrap))
        return Response(result)


        #포스트에서 유저 아이디가 있으면
    @transaction.atomic
    def delete(self, request, pk, format=None):

        #접속한 유저의 id 가져오기
        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)

        try:
            user = User.objects.get(user_uid = decodedPayload["id"])
            post = Post.objects.get(pk = pk) #해당 포스트 가져오기
        except ObjectDoesNotExist as e:
            result = Return_Module.ReturnPattern.error_text(str(e))
            return Response(result,status = status.HTTP_404_NOT_FOUND)


        # user_data = UserData.objects.get(user = user)
        print(decodedPayload['id'])
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

        try:
            user = User.objects.get(user_uid = decodedPayload["id"])
        except User.DoesNotExist as e:
            result = Return_Module.ReturnPattern.error_text(str(e))
            return Response(result,status = status.HTTP_404_NOT_FOUND)

        scrap = Scrapt.objects.filter(user_id = user.id)
        # serial = ScrapAllSerializer(user.get_scrap.all().order_by('scrap_users__id'),many=True)
        serial = ScrapSerializer(scrap,many=True)
        result = Return_Module.ReturnPattern.success_list_text\
        ("Show scrap list success",*serial.data)
        return Response(result)

        #아이디 값을 받아 온 뒤 리스트에서 뽑아서 딜리트
    def delete(self, request, format=None):
        scrap_required_keys = ['ids']
        # sending으로 안 묶여 있으면 에러 처리
        try:
            request_data = Return_Module.multi_string_to_dict(request.data) #sending 파라미터에서 value 추출해서 dict 형태로 변형
        except KeyError as e:
            # print(f"key error: missing key name {e}") #에러 로그
            result = Error_Module.ErrorHandling.none_bundle(req.request_bundle, e) #클라이언트에 보낼 에러 메시지
            return Response(result,status = status.HTTP_400_BAD_REQUEST)

        try:
            for key in scrap_required_keys:
                request_data[key]
        except KeyError as e:
            error_dict = Error_Module.ErrorHandling.none_feild(scrap_required_keys,request_data.keys(), e)
            result = Return_Module.ReturnPattern.error_text(error_dict)
            return Response(result,status = status.HTTP_400_BAD_REQUEST)
        else:
            ids = request_data['ids'].split(',')

        for num in range(0,len(ids)):
            ids[num]=int(ids[num])

        scrap = Scrapt.objects.filter(post_id__in = ids).delete() #해당 포스트 가져오기
        result = Return_Module.ReturnPattern.success_text\
        ("Successful delete", result = True)
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
