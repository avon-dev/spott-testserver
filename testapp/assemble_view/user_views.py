from testapp.assemble_view.__init__ import *

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
        serializers = MyUserSerializer(user)
        result = Return_Module.ReturnPattern.success_text("user info get",result=True, **serializers.data)
        return Response(result)


    def delete(self, request, format=None):
        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        user = User.objects.get(user_uid = decodedPayload["id"])
        user.is_active = False
        user.save()
        serializers =UserCreateSerializer(user)
        return Response(serializers.data)
