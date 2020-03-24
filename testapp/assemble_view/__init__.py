from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes, authentication_classes
# api_view 데코레이터 사용
from rest_framework.permissions import IsAuthenticated
# 로그인 여부를 확인할 때 사용합니다.
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# JWT 인증을 확인하기 위해 사용합니다.
from testapp.models import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import jwt
import json
from rest_framework.parsers import JSONParser
import io
from ast import literal_eval

import datetime
from testapp.myserializers import *
from django.shortcuts import get_object_or_404
from django.http import Http404
from function import random as ran
from function import email as Email_Module
from function import errors as Error_Module
from function import returns as Return_Module
from function import request as req
from function import string as string_get
from function import orm
from function import security
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
