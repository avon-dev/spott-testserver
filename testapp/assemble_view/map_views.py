from .__init__ import *

class Posts(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        data = Return_Module.string_to_dict(request.GET)
        lat_ne = data['lat_ne']
        lng_ne = data['lng_ne']
        lat_sw = data['lat_sw']
        lng_sw = data['lng_sw']
        posts_data = Post.objects.filter(handling = 22001 ,is_active = True, problem = False, is_public = True, latitude__range=[lat_sw,lat_ne],longitude__range=[lng_sw,lng_ne]).\
        order_by('-id')
        serializers = PostSerializer(posts_data, many = True)
        dict = {"payload":serializers.data}
        posts_json = json.dumps(dict)
        return Response(posts_json)
