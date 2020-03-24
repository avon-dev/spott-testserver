from rest_framework.response import Response
from rest_framework import status
from .returns import ReturnPattern

class ErrorHandling:

    def none_feild(keyname_list,request_list, error):
        dict ={}
        for key in keyname_list: #인자값으로 받은 keynames을 하나씩 대입
            if not key in request_list: #리퀘스트의 키값에 키값이 있는지 확인
                dict[key] = "%s field is required" %key
        print(f"required_keys {error}")
        return dict

    def none_bundle(bundle_name, error):
        dict = {}
        message = "message"
        dict[message] = "Send it in a bundle name '%s'" %bundle_name
        print(f"sending bundle not found {error}")
        return ReturnPattern.error_text(dict)
