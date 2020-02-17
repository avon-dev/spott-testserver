from testapp.assemble_view.__init__ import *



from rest_framework import viewsets
from django.core.serializers.json import DjangoJSONEncoder
from django.db import IntegrityError
from random import *

class SearchView(APIView):

    permission_classes = (IsAuthenticated,)
#




# #으로 검색을 했을 시에는 해쉬태그로 검색 아이템 하나로
# 검색을 할 때 그러면 객체의 수를 다 세어서
    def get(self, request, format=None):
        request_data = Return_Module.string_to_dict(request.GET)
        word = request_data['search_word']
        is_tag = request_data['is_tag']
        if is_tag:
            tag_obj = HashTag.objects.filter(name__istartswith = word).order_by('-count')[:16]
            tag_serializer = SearchTagSerializer(tag_obj, many = True)
            result = Return_Module.ReturnPattern.success_text\
            ("Search success", items = tag_serializer.data)
            return Response(result)
        else:
            user_obj = User.objects.filter(is_active = True, nickname__istartswith = word)
            tag_obj = HashTag.objects.filter(name__istartswith = word)
            tag_serializer = SearchTagSerializer(tag_obj,many=True)

            user_serializer = SearchNameSerializer(user_obj,many=True)

            user_json_dumps_loads = json.loads(json.dumps(user_serializer.data))
            count = 0
            for users in range(len(user_json_dumps_loads)):
                user_json_dumps_loads[count]['is_tag'] = False
                count += 1

            result_list = tag_serializer.data + user_json_dumps_loads
            result = Return_Module.ReturnPattern.success_text\
            ("Search success",items = result_list)
            return Response(result)


        # user= User.objects.all()
        # user[0].user_hashtag.all()
        # # tag_obj = HashTag.objects.all().select_related()
        # # tag_serializer = SerialTest(tag_obj,many=True)
        # # print(str(tag_obj[0].query())
        # # print(tag_obj.query)
        # return Response(str(user))



class RecentSearchView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    action_user = 1101
    action_tag = 1102
    def list(self,request):
        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        # request_data = Return_Module.string_to_dict(request.data)
        user = User.objects.all()
        tag = HashTag.objects.all()
        list = []
        myself = user.get(user_uid = decodedPayload['id'])

        for recent in myself.recent_search:
            if recent['action'] == 1101:
                list.append(SearchNameSerializer(user.get(pk = recent['user_pk'])).data)
            else:
                list.append(SearchTagSerializer(tag.get(name = recent['tag_name'])).data)



        return Response(list,status=status.HTTP_200_OK)



#사이즈가 16이상시 맨 마지막꺼 pop 시키는 코드 추가
    def create(self, request):
        request_data_key = ['action','tag_name', 'user_pk']

        string = request.headers["Authorization"]
        decodedPayload = jwt.decode(string[4:],None,None)
        request_data = Return_Module.string_to_dict(request.data)
        user = User.objects.get(user_uid = decodedPayload['id'])
        print(decodedPayload['id'])
        user.recent_search.insert(0,request_data)
        # del user.recent_search[0]
        user.save()

        result = Return_Module.ReturnPattern.success_text\
        ("create success",result = True)


        return Response(result, status=status.HTTP_201_CREATED)


#
# #
#     def partial_update(self, request, pk=None):
#
#             return Response(result, status=status.HTTP_404_NOT_FOUND)
#
#
#
#
#     def destroy(self, request, pk=None):
#
#             return Response(result)
