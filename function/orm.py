from testapp.models import *
import jwt
from django.db import transaction




def get_myself(self, request):
    string = request.headers["Authorization"]
    decodedPayload = jwt.decode(string[4:],None,None)

    return User.objects.get(email = decodedPayload['id'])


def get_user_pk(self, pk):
    return User.objects.get(pk = pk)

def get_user_email(self, email):
    return User.objects.get(email = email)




########################sign_up

def get_user_with_nickname(self, nickname):
    return User.objects.get(nickname=nickname)



def user_create(self, email, password, nickname):
    user = User.objects.create(email = email\
    , user_uid = email\
    , password = password\
    , nickname = nickname)
    # user.user_uid = make_password(request_data["user_uid"])
    user.set_password(request_data["password"])
    user.save()
    return True
