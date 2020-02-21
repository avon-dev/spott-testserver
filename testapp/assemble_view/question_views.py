from testapp.assemble_view.__init__ import *



from rest_framework import viewsets
from django.core.serializers.json import DjangoJSONEncoder
from django.db import IntegrityError
from random import *



class ReportView(APIView):

#포스트 넘버만 받아서 해당 게시물 신고
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        request_data = Return_Module.string_to_dict(request.data)
        # contents =  {"contents":request_data['contents']}
        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        post_url = request_data.get('post_url')
        post_caption = request_data.get('post_caption')
        comment_contents = request_data.get('comment_contents')
        reason = request_data.get('reason')
        detail = request_data.get('detail')

        reporter = User.objects.get(user_uid = decodedPayload['id'])
        post = Post.objects.get(pk = request_data['post_id'])

        if post_url:
            report = Report.objects.create(reporter = reporter, post = post, post_owner = post.user.email,\
            post_url = post_url, post_caption = post_caption, reason = reason, detail = detail, handling = 1)
            result = Return_Module.ReturnPattern.success_text\
            ("report post success",result=True)
            return Response(result)
        elif comment_contents:
            comment = Comment.objects.get(pk = request_data['comment_id'])
            report = Report.objects.create(reporter = reporter, post = post, post_owner = post.user.email,\
            comment_owner = comment.user.email, comment = comment ,comment_contents = comment_contents ,reason = reason, detail = detail, handling = 3)
            result = Return_Module.ReturnPattern.success_text\
            ("comment post success",result=True)
            return Response(result)
        else:
            result = Return_Module.ReturnPattern.success_text\
            ("comment post success",result=True)
            return Response(result, status = status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        post = Comment.objects.get(id = 1)
        return Response(post.user.email)
