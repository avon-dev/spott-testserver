from testapp.assemble_view.__init__ import *

from django.contrib.auth.hashers import make_password, is_password_usable, check_password

##############################
#########이메일 인증###########
##############################
class EmailAuthentication(APIView):
    permission_classes = []

    def get(self, request, format=None):
        user_exist = None
        random_number = ""


        # sending으로 안 묶여 있으면 에러 처리
        try:
            request_data = Return_Module.string_to_dict(request.GET) #sending 파라미터에서 value 추출해서 dict 형태로 변형
        except KeyError as e:
            # print(f"key error: missing key name {e}") #에러 로그
            result = Error_Module.ErrorHandling.none_bundle(req.request_bundle,e) #클라이언트에 보낼 에러 메시지
            return Response(result,status = status.HTTP_400_BAD_REQUEST)

        print("request.GET"+str(request.GET))
        #필드에 필수 키가 있는지 확인 후 없을 경우 에러 반환
        try:
            for key in req.email_auth_req_key:
                request_data[key]
        except KeyError as e:
            error_dict = Error_Module.ErrorHandling.none_feild(req.email_auth_req_key,request_data.keys(), e)
            result = Return_Module.ReturnPattern.error_text(error_dict)
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
        #가입 되지 않은  이메일 일 경우에는 false 가입 된 이메일 일 경우에는 true로 user_exist를 변경 해 주고 이 값은 분기처리시 활용
        try:
            user = orm.get_user_email(self, email)
        except ObjectDoesNotExist as e:
            user_exist = False
        else:
            user_exist = True

        random_number = ran.RanStrCraete.number(4) #4자리 수의 랜덤 숫자 생성

        if action == req.sign_up_email_auth: #회원가입 이메일 인증 분기
            if not user_exist:
                print("send success")

                auth_email = Email_Module.email_setting(self, string_get.send_email_text, random_number, email)

                result = Return_Module.ReturnPattern.success_text\
                ("Send success", duplication=False,code=random_number)


                if auth_email.send() == 1: #이메일 보내기 성공시
                    return Response(result)
                else:
                    return Response({"error":"Email failed to send"}) #클라이언트와 회의 하여 다시 작성
            else:
                print("send fail")
                result = Return_Module.ReturnPattern.success_text\
                ("Duplicate email", duplication=True, code="")
                return Response(result)

        elif action == req.forgot_user_password: #패스워드 찾기 이메일 인증 분기

            if user_exist:
                auth_email = Email_Module.email_setting(self, string_get.send_email_text, random_number, email)

                result = Return_Module.ReturnPattern.success_text\
                ("Send success", registration=True,code=random_number)


                if auth_email.send() == 1: #이메일 보내기 성공시
                    return Response(result)
                else:
                    return Response({"error":"Email failed to send"}) #클라이언트와 회의 하여 다시 작성
                result = Return_Module.ReturnPattern.success_text\
                ("This email is not registration", registration=False, code=random_number)
                return Response(result)

            else:
                result = Return_Module.ReturnPattern.success_text\
                ("This email is not registration", registration=False, code="")
                return Response(result)

        else:
            result = Return_Module.ReturnPattern.success_text\
            ("not find action value")
            return Response(result, status = status.HTTP_400_BAD_REQUEST)





##############################
###########회원가입############
##############################






class AccountView(APIView):
    permission_classes = []
    @transaction.atomic
    def post(self, request, format=None):
        # 에러 처리부분 성공 조건이 아니면 함수 리턴

        # sending으로 안 묶여 있으면 에러 처리
        try:
            request_data = Return_Module.string_to_dict(request.data) #sending 파라미터에서 value 추출해서 dict 형태로 변형
        except KeyError as e:
            # print(f"key error: missing key name {e}") #에러 로그
            result = Error_Module.ErrorHandling.none_bundle(req.request_bundle, e) #클라이언트에 보낼 에러 메시지
            return Response(result,status = status.HTTP_400_BAD_REQUEST)

        #필수키가 없을 경우 400 에러 반환
        try:
            print(str(request.data))
            for key in req.sign_req_keys:
                request_data[key]
        except KeyError as e:
            error_dict = Error_Module.ErrorHandling.none_feild(req.sign_req_keys,request_data.keys(), e)
            result = Return_Module.ReturnPattern.error_text(error_dict)
            return Response(result,status = status.HTTP_400_BAD_REQUEST)
        else:
            email = request_data[req.email]
            password = security.RSAPublicKey().out_password(request_data['password'])
            nickname = request_data[req.nickname]


        try:
            nickname_check = orm.get_user_with_nickname(self,nickname)
        except ObjectDoesNotExist as e:
                #레코드 생성
            orm.user_create(self ,email, password, nickname)
            result = Return_Module.ReturnPattern.success_text("Create success",sign_up=True)
            return Response(result, status= status.HTTP_201_CREATED)

        else:
            result = Return_Module.ReturnPattern.success_text\
            (sign_up=False, message="Create fail")
            return Response(result, status = status.HTTP_200_OK)


    @transaction.atomic
    def patch(self, request, format = None):

        # sending으로 안 묶여 있으면 에러 처리
        try:
            request_data = Return_Module.string_to_dict(request.data) #sending 파라미터에서 value 추출해서 dict 형태로 변형
        except KeyError as e:
            # print(f"key error: missing key name {e}") #에러 로그
            result = Error_Module.ErrorHandling.none_bundle(req.request_bundle, e) #클라이언트에 보낼 에러 메시지
            return Response(result,status = status.HTTP_400_BAD_REQUEST)

        #필수키가 없을 경우 400 에러 반환
        try:
            print(str(request.data))
            for key in req.find_password_req_keys:
                request_data[key]
        except KeyError as e:
            error_dict = Error_Module.ErrorHandling.none_feild(req.find_password_req_keys,request_data.keys(), e)
            result = Return_Module.ReturnPattern.error_text(error_dict)
            return Response(result,status = status.HTTP_400_BAD_REQUEST)
        else:
            email = request_data[req.email]
            password = security.RSAPublicKey().out_password(request_data['password'])




        try:
            result = Return_Module.ReturnPattern.success_text("update success password",result=True)
            user = orm.get_user_email(self, email)
        except ObjectDoesNotExist as e:
            result = Return_Module.ReturnPattern.error_text(str(e))
            return Response(result, status = status.HTTP_404_NOT_FOUND)

        else:
            user.set_password(password)
            user.save()
            return Response(result, status = status.HTTP_200_OK)



class SocialAccountView(APIView):
    permission_classes = []




    def get(self, request, format=None):
        # sending으로 안 묶여 있으면 에러 처리
        try:
            request_data = Return_Module.string_to_dict(request.GET) #sending 파라미터에서 value 추출해서 dict 형태로 변형
        except KeyError as e:
            # print(f"key error: missing key name {e}") #에러 로그
            result = Error_Module.ErrorHandling.none_bundle(req.request_bundle, e) #클라이언트에 보낼 에러 메시지
            return Response(result,status = status.HTTP_400_BAD_REQUEST)

        try:
            for key in req.social_check_req_keys:
                request_data[key]
        except KeyError as e:
            error_dict = Error_Module.ErrorHandling.none_feild(req.social_check_req_keys,request_data.keys(), e)
            result = Return_Module.ReturnPattern.error_text(error_dict)
            return Response(result,status = status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email = request_data['email'], user_type = request_data['user_type'])
        except User.DoesNotExist as e:
            result = Return_Module.ReturnPattern.success_text("Go to sign up",sign_up=True)
        else:
            result = Return_Module.ReturnPattern.success_text("Go to create token",sign_up=False)
        return Response(result)



    @transaction.atomic
    def post(self, request, format=None):
        # 에러 처리부분 성공 조건이 아니면 함수 리턴

        # sending으로 안 묶여 있으면 에러 처리
        try:
            request_data = Return_Module.string_to_dict(request.data) #sending 파라미터에서 value 추출해서 dict 형태로 변형
        except KeyError as e:
            # print(f"key error: missing key name {e}") #에러 로그
            result = Error_Module.ErrorHandling.none_bundle(req.request_bundle, e) #클라이언트에 보낼 에러 메시지
            return Response(result,status = status.HTTP_400_BAD_REQUEST)

        try:
            print(str(request.data))
            for key in req.social_sign_req_keys:
                request_data[key]
        except KeyError as e:
            error_dict = Error_Module.ErrorHandling.none_feild(req.social_sign_req_keys,request_data.keys(), e)
            result = Return_Module.ReturnPattern.error_text(error_dict)
            return Response(result,status = status.HTTP_400_BAD_REQUEST)
        else:
            email = request_data[req.email]
            if request_data['user_type'] == User.google:
                user_type = User.google
                password = "google"
            else:
                user_type = User.facebook
                password = "facebook"
            nickname = request_data[req.nickname]


        try:
            nickname_check = orm.get_user_with_nickname(self,nickname)
        except ObjectDoesNotExist as e:
                #레코드 생성
            orm.social_user_create(self, email, password, nickname, user_type)
            result = Return_Module.ReturnPattern.success_text("Create success",sign_up=True)
            return Response(result, status= status.HTTP_201_CREATED)

        else:
            result = Return_Module.ReturnPattern.success_text\
            (sign_up=False, message="Create fail")
            return Response(result, status = status.HTTP_200_OK)
##############################
###########Legacy############
##############################
# class Login(APIView):
#     # authentication_classes = [JSONWebTokenAuthentication,]
#     permission_classes = ()
#     def get(self, request, format=None):
#         # post_list = UserSerializer(posts, many=True)
#         # string = request.headers["Authorization"]
#         # decodedPayload = jwt.decode(string[4:],None,None)
#         # user = User.objects.get(user_uid = decodedPayload["user_uid"])
#         # user.is_login = True
#         # user.last_login = datetime.datetime.now()
#         # user.save()
#         # serializers = LoginSerializer(user)
#         # result = Return_Module.ReturnPattern.success_text("Login success",result=True, **serializers.data)
#
#         result = Return_Module.ReturnPattern.success_text("success",result=True)
#         return Response(result)


class PublicKeyView(APIView):
    # authentication_classes = [JSONWebTokenAuthentication,]
    permission_classes = ()
    def get(self, request, format=None):
        # post_list = UserSerializer(posts, many=True)
        # string = request.headers["Authorization"]
        # decodedPayload = jwt.decode(string[4:],None,None)
        # user = User.objects.get(user_uid = decodedPayload["user_uid"])
        # user.is_login = True
        # user.last_login = datetime.datetime.now()
        # user.save()
        # serializers = LoginSerializer(user)
        # result = Return_Module.ReturnPattern.success_text("Login success",result=True, **serializers.data)

        result = Return_Module.ReturnPattern.success_text("success",result=True)
        return Response(result)
