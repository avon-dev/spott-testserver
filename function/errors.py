


class ErrorHandling:

    def none_feild(*keynames,**request):
        dict ={}
        for key in keynames: #인자값으로 받은 keynames을 하나씩 대입
            if not key in request.keys(): #리퀘스트의 키값에 키값이 있는지 확인
                dict[key] = "%s field is required" %key
        return dict
