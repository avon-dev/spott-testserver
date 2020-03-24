from django.http import HttpResponse
from django.shortcuts import render
from testapp.assemble_view.__init__ import *

def guide(request):
    return render(request, 'spotts/guide.html')

def guideEn(request):
    return render(request, 'spotts/guide_en.html')

def guideCn(request):
    return render(request, 'spotts/guide_cn.html')


def personalInformationProcessingPolicy(request):
    return render(request, 'spotts/personal_information_processing_policy.html')


def locationBasedServiceTermsAndConditions(request):
    return render(request, 'spotts/location_based_service_terms_and_conditions.html')


def termsAndConditions(request):
    return render(request, 'spotts/terms_and_conditions.html')


def firstNotice(request):
    return render(request, 'spotts/app_notice.html')

def openSource(request):
    return render(request, 'spotts/open_source.html')


class AppNoticesView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        app_notice = AppNotices.objects.all()

        serializers = AppNoticeSerializer(app_notice, many = True)
        result = Return_Module.ReturnPattern.success_list_text\
        ("Show AppNotices list success",*serializers.data)
        return Response(result)
