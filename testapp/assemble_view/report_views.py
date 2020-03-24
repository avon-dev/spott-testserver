from testapp.assemble_view.__init__ import *



from rest_framework import viewsets
from django.core.serializers.json import DjangoJSONEncoder
from django.db import IntegrityError
from random import *



class ReportView(APIView):

#포스트 넘버만 받아서 해당 게시물 신고

    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def post(self, request, format=None):
        report_required_keys = ["detail", "reason", "detail"]

        # sending으로 안 묶여 있으면 에러 처리
        try:
            request_data = Return_Module.string_to_dict(request.data) #sending 파라미터에서 value 추출해서 dict 형태로 변형
        except KeyError as e:
            # print(f"key error: missing key name {e}") #에러 로그
            result = Error_Module.ErrorHandling.none_bundle(req.request_bundle, e) #클라이언트에 보낼 에러 메시지
            return Response(result,status = status.HTTP_400_BAD_REQUEST)

        try:
            for key in report_required_keys:
                request_data[key]
        except KeyError as e:
            error_dict = Error_Module.ErrorHandling.none_feild(report_required_keys,request_data.keys(), e)
            result = Return_Module.ReturnPattern.error_text(error_dict)
            return Response(result,status = status.HTTP_400_BAD_REQUEST)
        else:
            post_url = request_data.get('post_url')
            post_caption = request_data.get('post_caption')
            comment_contents = request_data.get('comment_contents')
            reason = request_data.get('reason')
            detail = request_data.get('detail')

        # contents =  {"contents":request_data['contents']}
        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)

        try:
            reporter = User.objects.get(user_uid = decodedPayload['user_uid'])
            print(request_data['post_id'])
            post = Post.objects.get(pk = request_data['post_id'])
        except ObjectDoesNotExist as e:
            result = Return_Module.ReturnPattern.error_text(str(e))
            return Response(result, status = status.HTTP_404_NOT_FOUND)


        if post_url:
            report = Report.objects.create(reporter = reporter, post = post, post_url = post_url, \
            post_caption = post_caption, reason = reason, detail = detail, handling = 1)
            result = Return_Module.ReturnPattern.success_text\
            ("Report post successful",result=True)
            return Response(result)
        elif comment_contents:
            comment = Comment.objects.get(pk = request_data['comment_id'])
            report = Report.objects.create(reporter = reporter, post = post, \
            comment = comment ,comment_contents = comment_contents ,reason = reason, detail = detail, handling = 3)
            result = Return_Module.ReturnPattern.success_text\
            ("Report comment successful",result=True)
            return Response(result)
        else:
            result = Return_Module.ReturnPattern.error_text("error : 미구현")
            return Response(result, status = status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        post = Comment.objects.get(id = 1)
        return Response(post.user.email)
