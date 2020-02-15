from testapp.assemble_view.__init__ import *
from django.contrib.auth.hashers import make_password, is_password_usable, check_password
from .base_views import BaseAPIView
class UserView(BaseAPIView):



    #내 정보 get 유저 프로필, 닉네임,
    #수정 프로필, 닉네임
    #회원 탈퇴
    #로그아웃 로그아웃을 하게 되면 토큰 블랙리스트에 추가
    permission_classes = (IsAuthenticated,)
    def get (self, request, format=None):
        # super().get(request)
        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        user = User.objects.get(user_uid = decodedPayload["id"])
        serializers = MyUserSerializer(user)
        result = Return_Module.ReturnPattern.success_text("user info get",result=True, **serializers.data)
        return Response(result)

    def patch (self, request, format=None):
        request_data = Return_Module.string_to_dict(request.data)
        is_key = False

        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        user = User.objects.get(user_uid = decodedPayload["id"])

        if 'profile_image' in request.FILES.keys() and 'nickname' in request_data.keys():
            user.profile_image = request.FILES['profile_image']
            user.nickname = request_data['nickname']
            user.save()
            is_key = True
        elif 'profile_image' in request.FILES.keys():
            user.profile_image = request.FILES['profile_image']
            user.save()
        elif 'nickname' in request_data.keys():
            user.nickname = request_data['nickname']
            user.save()
        else:
            result = Return_Module.ReturnPattern.success_text('update fail profile',result=False)
            return Response(result)

        # serializers = MyUserSerializer(user)
        result = Return_Module.ReturnPattern.success_text('update success profile',result=True)
        return Response(result)


    def delete(self, request, format=None):
        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        user = User.objects.get(user_uid = decodedPayload["id"])
        user.is_active = False
        user.save()
        result = Return_Module.ReturnPattern.success_text('delete success profile',result=True)
        return Response(result)




class PasswordView(APIView):
    permission_classes = (IsAuthenticated,)
    #password 겟
    def get(self, request, format = None):
        request_data = Return_Module.string_to_dict(request.GET)
        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        user = User.objects.get(is_active = True, user_uid = decodedPayload["id"])

        if check_password(request_data['password'], user.password):
            result = Return_Module.ReturnPattern.success_text("equals password",result=True)
            return Response(result, status = status.HTTP_200_OK)
        else:
            result = Return_Module.ReturnPattern.success_text("unconformable password",result=False)
            return Response(result, status = status.HTTP_200_OK)




    def patch(self, request, format = None):
        request_data = Return_Module.string_to_dict(request.data)
        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        try:
            result = Return_Module.ReturnPattern.success_text("update success password",result=True)
            user = User.objects.get(is_active = True, user_uid = decodedPayload["id"])
        except Exception as e:
            result = Return_Module.ReturnPattern.success_text("update fail password",result=False)
            return Response(result, status = status.HTTP_200_OK)

        else:
            user.set_password(request_data["password"])
            user.save()
            return Response(result, status = status.HTTP_200_OK)





    # def patch(self, request, format=None):
    #     string = request.headers["Authorization"]
    #     decodedPayload = jwt.decode(string[4:],None,None)
    #     request_data = Return_Module.string_to_dict(request.GET)
    #
    #     try:
    #         result = Return_Module.ReturnPattern.success_text("password update",result=True)
    #         user = User.objects.get(is_active = True, user_uid = decodedPayload["id"])
    #         post = Post.objects.filter(user=user).update(public = request_data['public'])
    #     except Exception as e:
    #         result['payload']['result'] = False
    #         result['message'] = "password update failed"
    #         return Response(result, status = status.HTTP_204_NO_CONTENT)
    #
    #     return Response(result, status = status.HTTP_201_CREATED)
