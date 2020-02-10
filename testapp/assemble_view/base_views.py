
from testapp.assemble_view.__init__ import *

class BaseAPIView(APIView):

    def get(self, request, format=None):

        # 에러 처리부분 성공 조건이 아니면 함수 리턴
        if not 'sending' in request.GET.keys():
            dict = Error_Module.ErrorHandling.none_bundle()
            
            result = Return_Module.ReturnPattern.error_text(**dict)
            return Response(result,status = status.HTTP_404_NOT_FOUND)
