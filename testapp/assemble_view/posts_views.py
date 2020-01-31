from testapp.assemble_view.__init__ import *



from rest_framework import viewsets




class PostViewSet(viewsets.ViewSet):
    permission_classes = []
    def create(self, request):

        request_data = Return_Module.multi_string_to_dict(request.data)
        # testdd = test.objects.create(latitude = request_data["latitude"] ,testfield = request_data["testfield"], photo = request.FILES["photo"], photo2 = request.FILES["photo2"], dummy = request_data["dummy"])
        posts = Post.objects.create(latitude = request_data["latitude"],\
        longitude = request_data["longitude"],\
        contents = request_data["contents"],\
        posts_image = request.FILES['posts_image'],\
        back_image = request.FILES['back_image'],\
        public = request_data["public"])
        # posts = Post.objects.create(latitude = request.data["latitude"], longitude = request.data["longitude"],text = request.data["text"] ,posts_image = request.FILES['posts_image'], back_image = request.FILES['back_image'])
        # posts.save()
        # serializers = PostsSerializer(data = request.data)
        # if serializers.is_valid():
        #      serializers.save()
        #      asd = str(request.FILES['posts_image'].name)
        # asd = request_data["text"]
        # file = request.FILES['back_image'].content_type = 'image/jpeg'
        return Response("success", status=status.HTTP_201_CREATED)
