from django.shortcuts import render
# from django.core import serializers
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
# api_view 데코레이터 사용
from rest_framework.permissions import IsAuthenticated
# 로그인 여부를 확인할 때 사용합니다.
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# JWT 인증을 확인하기 위해 사용합니다.
from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import jwt
import json
from rest_framework.parsers import JSONParser
import io
from ast import literal_eval

import datetime
from .myserializers import *
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.http import Http404
import sys
sys.path.append("../")
from function import randomes
from function import email as Email_Module
from function import errors as Error_Module
from function import returns as Return_Module

# @api_view(['GET'])
# # @api_view(['GET']): 위에서 언급한 데코레이터(Decorator)입니다. 하위에 있는 함수(def posts(request):)를 실행하기 전에 이 부분이 먼저 실행됩니다.
# # 이 데코레이터(Decorator)는 GET 요청인지 검증하고 GET이 아니면 에러를 JSON 타입으로 반환합니다.
# @permission_classes((IsAuthenticated, ))
# # 권한을 체크합니다. 여기서는 로그인 했는지 여부만 체크하도록 하였습니다.
# @authentication_classes((JSONWebTokenAuthentication,))
# # JWT 토큰을 확인합니다. 토큰이 이상이 있으면 에러를 JSON 형식으로 반환합니다.
# def posts(request):
#     posts = User.objects.all()
#     post_list = serializers.serialize('json', posts)
#     return HttpResponse(post_list, content_type="text/json-comment-filtered")
request_bundle = "sending"

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
            random_number = randomes.RanStrCraete.number(4) #4자리 난수 생성

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


class Test(APIView):
    permission_classes = []
    def post(self, request, format=None):
        repl = Return_Module.ReturnPattern.string_to_dict(request.data)
        repl['nickname'] = "asdasd"
        # asd = repl['nickname']
        result = Return_Module.ReturnPattern.success_text("Create success",**repl)
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
        return Response(str(result))


class Test2(APIView):
    permission_classes = []
    def get(self, request, format=None):
        repl = Return_Module.ReturnPattern.string_to_dict(request.data)
        repl['nickname'] = "asdasd"
        # asd = repl['nickname']
        result = Return_Module.ReturnPattern.success_text("Create success",**repl)
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
        return Response(str(result))
            # return Response(random_string)


class Posts(APIView):
    permission_classes = []
    def get(self, request, format=None):
        data = Return_Module.string_to_dict(request.GET)
        lat_ne = data['lat_ne']
        lng_ne = data['lng_ne']
        lat_sw = data['lat_sw']
        lng_sw = data['lng_sw']
        posts_data = Post.objects.filter(latitude__range=[lat_sw,lat_ne],longitude__range=[lng_sw,lng_ne])
        serializers = PostSerializer(posts_data, many = True)
        dict = {"payload":serializers.data}
        posts_json = json.dumps(dict)
        return Response(posts_json)

    def post(self, request, format=None):

        request_data = Return_Module.multi_string_to_dict(request.data)

        # testdd = test.objects.create(latitude = request_data["latitude"] ,testfield = request_data["testfield"], photo = request.FILES["photo"], photo2 = request.FILES["photo2"], dummy = request_data["dummy"])
        posts = Post.objects.create(latitude = request_data["latitude"], longitude = request_data["longitude"],contents = request_data["contents"] ,posts_image = request.FILES['posts_image'], back_image = request.FILES['back_image'])
        # posts = Post.objects.create(latitude = request.data["latitude"], longitude = request.data["longitude"],text = request.data["text"] ,posts_image = request.FILES['posts_image'], back_image = request.FILES['back_image'])
        # posts.save()
        # serializers = PostsSerializer(data = request.data)
        # if serializers.is_valid():
        #      serializers.save()
        #      asd = str(request.FILES['posts_image'].name)
        # asd = request_data["text"]
        # file = request.FILES['back_image'].content_type = 'image/jpeg'
        return Response("success", status=status.HTTP_201_CREATED)



# class Home(APIView):
