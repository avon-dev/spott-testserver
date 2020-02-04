from testapp.assemble_view.__init__ import *

from django.contrib.auth.hashers import make_password, is_password_usable, check_password

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

        #sending 파라미터에서 value 추출해서 dict 형태로 변형
        request_data = Return_Module.string_to_dict(request.GET)

        #필드에 이메일이 없을 경우
        if not feild_name in request_data.keys():
            dict = Error_Module.ErrorHandling.none_feild(feild_name,**request.GET.dict())
            result = Return_Module.ReturnPattern.error_text(**dict)
            return Response(result,status = status.HTTP_404_NOT_FOUND)

        #이메일 필드의 형식이 이메일이 아닐경우
        elif Email_Module.is_valid(request_data["email"]):
            dict = {feild_name:"Not an email pattern"}
            result = Return_Module.ReturnPattern.error_text(**dict)
            return Response(result,status = status.HTTP_404_NOT_FOUND)

        #데이터베이스 User 테이블에서 동일한 이메일이 있는지 검색
        # user = User.objects.get(email=request_data['email'])
        #
        #     random_number = ran.RanStrCraete.number(4) #4자리 난수 생성

        try:
            user = User.objects.get(email=request_data['email'])
        except ObjectDoesNotExist:
            random_number = ran.RanStrCraete.number(4) #4자리 수의 랜덤 숫자 생성

            subject = '서버에서 발송된 이메일'
            message = '인증코드: '+ random_number
            user_email = request_data["email"]
            email = EmailMessage(subject,message,to=[user_email])

            result = Return_Module.ReturnPattern.success_text\
            ("Send success",result=True,code=random_number)


            if email.send() == 1: #이메일 보내기 성공시
                return Response(result)
            else:
                return Response({"error":"Email failed to send"}) #클라이언트와 회의 하여 다시 작성
        else:

            result = Return_Module.ReturnPattern.success_text\
            ("Duplicate email",result=False, code=random_number)
            return Response(result)






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

        request_data = Return_Module.string_to_dict(request.data)

        for required in parameter_list: #필수 필드가 포함이 되어 있는지 확인
            if not required in request_data.keys():
                dict = Error_Module.ErrorHandling.none_feild(*parameter_list,**request_data)
                result = Return_Module.ReturnPattern.error_text(**dict)
                return Response(result,status = status.HTTP_404_NOT_FOUND)

        user = User.objects.filter(nickname=request_data['nickname'])



        if user: #유저의 닉네임이 중복이 되는지 검사
            result = Return_Module.ReturnPattern.success_text\
            (result=False, message="Duplicate nickname")
            return Response(result)

        serializer = UserCreateSerializer(data=request_data)
        if serializer.is_valid():

            #레코드 생성
            user = User.objects.create(email = request_data["email"]\
            , user_uid = request_data["user_uid"]\
            , password = request_data["password"]\
            , nickname = request_data["nickname"])
            # user.user_uid = make_password(request_data["user_uid"])
            user.set_password(request_data["password"])
            user.save()

            result = Return_Module.ReturnPattern.success_text("Create success",result=True)
            return Response("success", status= status.HTTP_201_CREATED)
        else:
            return Response("failed", status= status.HTTP_404_NOT_FOUND)

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
