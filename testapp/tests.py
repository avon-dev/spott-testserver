from django.test import TestCase
# import sys
# sys.path.append("../")
# from function import errors
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# # Create your tests here.
# class EmailAuthentication(APIView):
#
#     def get(self, request, format=None):
#
#         if not 'email' in request.GET.keys(): #필드에 이메일이 없을 경우
#             return Response({"error":"Email field is required"},status = status.HTTP_404_NOT_FOUND)
#         ######################난수 생성
#         elif Email_Module.is_valid(request.GET["email"]): #이메일 필드의 형식이 이메일이 아닐경우
#             return Response({"error":"Not an email pattern"},status = status.HTTP_404_NOT_FOUND)
#
#         random_number = randomes.RanStrCraete.number(4) #4자리 난수 생성
#
#         subject = '서버에서 발송된 이메일'
#         message = '인증코드: '+ random_number
#         user_email = request.GET["email"]
#
#         email = EmailMessage(subject,message,to=[user_email])
#
#         code = '{"payload": {"code":\"%s\"}}'%random_number # 이스케이프 방법이랑 포맷팅 방법 때문에 조금 해맴
#         code_dict = json.loads(code)
#         if email.send() == 1:
#             return Response(code_dict)
#         else:
#             return Response({"error":"Email failed to send"})
