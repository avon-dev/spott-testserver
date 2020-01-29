from .__init__ import *

class Posts(APIView):
    permission_classes = []
    def get(self, request, format=None):
        data = Return_Module.string_to_dict(request.GET)
        lat_ne = data['lat_ne']
        lng_ne = data['lng_ne']
        lat_sw = data['lat_sw']
        lng_sw = data['lng_sw']
        posts_data = Post.objects.filter(latitude__range=[lat_sw,lat_ne],longitude__range=[lng_sw,lng_ne]).\
        order_by('id')
        serializers = PostSerializer(posts_data, many = True)
        dict = {"payload":serializers.data}
        posts_json = json.dumps(dict)
        return Response(posts_json)

    def post(self, request, format=None):

        request_data = Return_Module.multi_string_to_dict(request.data)

        # testdd = test.objects.create(latitude = request_data["latitude"] ,testfield = request_data["testfield"], photo = request.FILES["photo"], photo2 = request.FILES["photo2"], dummy = request_data["dummy"])
        posts = Post.objects.create(latitude = request_data["latitude"], longitude = request_data["longitude"],contents = request_data["contents"] ,posts_image = request.FILES['posts_image'], back_image = request.FILES['back_image'])
        # posts = Post.objects.create(latitude = request.data["latitude"], longitude = request.data["longitude"],text = request.data["text"] ,posts_image = request.FILES['posts_image'], back_image = request.FILES['back_image'])
        # posts.save()
        # serializers = PostsSerializer(data = request.data)
        # if serializers.is_valid():
        #      serializers.save()
        #      asd = str(request.FILES['posts_image'].name)
        # asd = request_data["text"]
        # file = request.FILES['back_image'].content_type = 'image/jpeg'
        return Response("success", status=status.HTTP_201_CREATED)
