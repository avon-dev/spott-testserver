from testapp.assemble_view.__init__ import *

from django.contrib.auth.hashers import make_password, is_password_usable, check_password

##############################
#########이메일 인증###########
##############################
class EmailAuthentication(APIView):
    permission_classes = []

    def get(self, request, format=None):
        random_number = ""
        # sending으로 안 묶여 있으면 에러 처리
        try:
            request_data = Return_Module.string_to_dict(request.GET) #sending 파라미터에서 value 추출해서 dict 형태로 변형
        except KeyError as e:
            # print(f"key error: missing key name {e}") #에러 로그
            result = Error_Module.ErrorHandling.none_bundle(req.request_bundle) #클라이언트에 보낼 에러 메시지
            return Response(result,status = status.HTTP_400_BAD_REQUEST)


        #필드에 이메일이 없을 경우
        try:
            for key in req.email_auth_req_key:
                request_data[key]
        except KeyError as e:
            dict = Error_Module.ErrorHandling.none_feild(req.email_auth_req_key,request_data.keys())
            result = Return_Module.ReturnPattern.error_text(dict)
            return Response(result,status = status.HTTP_400_BAD_REQUEST)
        else:
            email = request_data[req.email]
            action = request_data[req.action]

            #이메일 패턴이 아닐경우 오류 반환
            if Email_Module.is_valid(email):
                error_dict = {req.email : req.pattern_error %req.email}
                result = Return_Module.ReturnPattern.error_text(error_dict)
                return Response(result,status = status.HTTP_400_BAD_REQUEST)

        # print(self.request_data_key)
        if action == req.sign_up_email_auth:

            try:
                user = User.objects.get(email=email)
            except ObjectDoesNotExist:
                print("send success")
                random_number = ran.RanStrCraete.number(4) #4자리 수의 랜덤 숫자 생성

                subject = string_get.send_email_text
                message = string_get.auth_code_text + random_number
                auth_email = EmailMessage(subject,message,to=[email])

                result = Return_Module.ReturnPattern.success_text\
                ("Send success", duplication=False,code=random_number)


                if auth_email.send() == 1: #이메일 보내기 성공시
                    return Response(result)
                else:
                    return Response({"error":"Email failed to send"}) #클라이언트와 회의 하여 다시 작성
            else:
                print("send fail")
                result = Return_Module.ReturnPattern.success_text\
                ("Duplicate email", duplication=True, code=random_number)
                return Response(result)

        elif action == req.forgot_user_password:

            try:
                user = User.objects.get(email=email)

            except ObjectDoesNotExist:
                result = Return_Module.ReturnPattern.success_text\
                ("This email is not registration", registration=False, code=random_number)
                return Response(result)

            else:
                random_number = ran.RanStrCraete.number(4) #4자리 수의 랜덤 숫자 생성

                subject = string_get.send_email_text
                message = string_get.auth_code_text + random_number
                auth_email = EmailMessage(subject,message,to=[email])

                result = Return_Module.ReturnPattern.success_text\
                ("Send success", registration=True,code=random_number)


                if auth_email.send() == 1: #이메일 보내기 성공시
                    return Response(result)
                else:
                    return Response({"error":"Email failed to send"}) #클라이언트와 회의 하여 다시 작성
        else:
            result = Return_Module.ReturnPattern.success_text\
            ("not find action value")
            return Response(result, status = status.HTTP_400_BAD_REQUEST)





##############################
###########회원가입############
##############################






class AccountView(APIView):
    permission_classes = []
    def post(self, request, format=None):

        parameter_list = ["email", "password", "nickname"]

        # 에러 처리부분 성공 조건이 아니면 함수 리턴
        # sending으로 안 묶여 있으면 에러 처리
        try:
            request_data = Return_Module.string_to_dict(request.data) #sending 파라미터에서 value 추출해서 dict 형태로 변형
        except KeyError as e:
            print(f"key error: missing key name {e}") #에러 로그
            result = Error_Module.ErrorHandling.none_bundle(request_bundle) #클라이언트에 보낼 에러 메시지
            return Response(result,status = status.HTTP_400_BAD_REQUEST)

        for required in parameter_list: #필수 필드가 포함이 되어 있는지 확인
            if not required in request_data.keys():
                dict = Error_Module.ErrorHandling.none_feild(*parameter_list,**request_data)
                result = Return_Module.ReturnPattern.error_text(**dict)
                return Response(result,status = status.HTTP_404_NOT_FOUND)

        try:
            nickname_check = User.objects.get(nickname=request_data['nickname'])
        except ObjectDoesNotExist as e:
                #레코드 생성
            user = User.objects.create(email = request_data["email"]\
            , user_uid = request_data["email"]\
            , password = request_data["password"]\
            , nickname = request_data["nickname"])
            # user.user_uid = make_password(request_data["user_uid"])
            user.set_password(request_data["password"])
            user.save()

            result = Return_Module.ReturnPattern.success_text("Create success",sign_up=True)
            return Response(result, status= status.HTTP_201_CREATED)

        else:
            result = Return_Module.ReturnPattern.success_text\
            (sign_up=False, message="Create fail")
            return Response(result, status = status.HTTP_200_OK)

    def patch(self, request, format = None):
        request_data = Return_Module.string_to_dict(request.data)
        email = request_data['email']
        password = request_data['password']
        try:
            result = Return_Module.ReturnPattern.success_text("update success password",result=True)
            user = User.objects.get(is_active = True, email = email)
        except Exception as e:
            result = Return_Module.ReturnPattern.success_text("update fail password",result=False)
            return Response(result, status = status.HTTP_200_OK)

        else:
            user.set_password(password)
            user.save()
            return Response(result, status = status.HTTP_200_OK)




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
        user = User.objects.get(user_uid = decodedPayload["id"])
        user.is_login = True
        user.last_login = datetime.datetime.now()
        user.save()
        serializers = LoginSerializer(user)
        result = Return_Module.ReturnPattern.success_text("Login success",result=True, **serializers.data)
        return Response(result)
