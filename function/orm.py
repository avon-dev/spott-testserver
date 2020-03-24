from testapp.models import *
import jwt
from django.db import transaction
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password, is_password_usable, check_password
def tag_exist(self, tag_name):
    try:
        HashTag.objects.get(name = tag_name)
    except ObjectDoesNotExist as e:
        tag_exist = False
    else:
        tag_exist = True
    return tag_exist


def get_myself(self, request):
    string = request.headers["Authorization"]
    decodedPayload = jwt.decode(string[4:],None,None)

    return User.objects.get(user_uid = decodedPayload['user_uid'])


def get_user_pk(self, pk):
    return User.objects.get(pk = pk)

def get_user_email(self, email):
    return User.objects.get(is_active = True, email = email, user_type = User.basic)




########################sign_up

def get_user_with_nickname(self, nickname):
    return User.objects.get(is_active = True, nickname=nickname)



def user_create(self, email, password, nickname):
    user = User.objects.create(email = email\
    , user_uid = make_password(email)\
    , password = password\
    , nickname = nickname)
    user.set_password(password)
    user.save()
    return True


def social_user_create(self, email, password, nickname, type):
    user = User.objects.create(email = email\
    , user_uid = make_password(email)\
    , password = password\
    , nickname = nickname\
    , user_type = type)
    user.set_password(password)
    user.save()
    return True
