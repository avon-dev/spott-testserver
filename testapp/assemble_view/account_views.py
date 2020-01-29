from testapp.assemble_view.__init__ import *



##############################
#########이메일 인증###########
##############################
class EmailAuthentication(APIView):
    permission_classes = []
    def get(self, request, format=None):
        feild_name = "email"
        random_number = ""

        # 에러 처리부분 성공 조건이 아니면 함수 리턴
        if not request_bundle in request.GET.keys():
            dict = Error_Module.ErrorHandling.none_bundle()
            result = Return_Module.ReturnPattern.error_text(**dict)
            return Response(result,status = status.HTTP_404_NOT_FOUND)

        parse = Return_Module.string_to_dict(request.GET)
        if not feild_name in parse.keys(): #필드에 이메일이 없을 경우
            dict = Error_Module.ErrorHandling.none_feild(feild_name,**request.GET.dict())
            result = Return_Module.ReturnPattern.error_text(**dict)
            return Response(result,status = status.HTTP_404_NOT_FOUND)
            ######################난수 생성
        elif Email_Module.is_valid(parse["email"]): #이메일 필드의 형식이 이메일이 아닐경우
            dict = {feild_name:"Not an email pattern"}
            result = Return_Module.ReturnPattern.error_text(**dict)
            return Response(result,status = status.HTTP_404_NOT_FOUND)

        user = User.objects.filter(email=parse['email'])
        if user:
            result = Return_Module.ReturnPattern.success_text("Duplicate email",result=False, code=random_number)
            return Response(result)
        else:
            random_number = ran.RanStrCraete.number(4) #4자리 난수 생성

            subject = '서버에서 발송된 이메일'
            message = '인증코드: '+ random_number
            user_email = parse["email"]

            email = EmailMessage(subject,message,to=[user_email])

            result = Return_Module.ReturnPattern.success_text("Send success",result=True,code=random_number)

            if email.send() == 1:
                return Response(result)
            else:
                return Response({"error":"Email failed to send"})


##############################
###########회원가입############
##############################
class UserCreate(APIView):
    permission_classes = []
    def post(self, request, format=None):

        parameter_list = ["email", "password", "nickname"]
        # 에러 처리부분 성공 조건이 아니면 함수 리턴
        if not request_bundle in request.data.keys():
            dict = Error_Module.ErrorHandling.none_bundle()
            result = Return_Module.ReturnPattern.error_text(**dict)
            return Response(result,status = status.HTTP_404_NOT_FOUND)



        parse = Return_Module.string_to_dict(request.data)

        for required in parameter_list: #필수 필드가 포함이 되어 있는지 확인
            if not required in parse.keys():
                dict = Error_Module.ErrorHandling.none_feild(*parameter_list,**parse)
                result = Return_Module.ReturnPattern.error_text(**dict)
                return Response(result,status = status.HTTP_404_NOT_FOUND)

        user = User.objects.filter(nickname=parse['nickname'])



        if user: #유저의 닉네임이 중복이 되는지 검사
            result = Return_Module.ReturnPattern.success_text(result=False, message="Duplicate nickname")
            return Response(result)

        serializer = UserCreateSerializer(data=parse)
        if serializer.is_valid():
            user = User.objects.create(email = parse["email"], password = parse["password"], nickname = parse["nickname"])
            user.set_password(parse['password'])
            user.save()

            result = Return_Module.ReturnPattern.success_text("Create success",result=True)
            return Response(result, status= status.HTTP_201_CREATED)


##############################
###########Legacy############
##############################
class Login(APIView):
    # authentication_classes = [JSONWebTokenAuthentication,]
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        # post_list = UserSerializer(posts, many=True)
        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        user = User.objects.get(id = decodedPayload["user_id"])
        user.is_login = True
        user.last_login = datetime.datetime.now()
        user.save()
        serializers = LoginSerializer(user)
        result = Return_Module.ReturnPattern.success_text("Login success",result=True, **serializers.data)
        return Response(result)
