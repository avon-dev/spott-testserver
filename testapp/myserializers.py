from rest_framework import serializers
from .models import *
import datetime
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')
        # extra_kwargs = {"password": {"write_only": True}}
        #
        # def create(self, validated_data):
        #     user = User(email=validated_data['email'],nickname=validated_data['nickname'])
        #     user.set_password(validated_data['password'])
        #     user.save()
        #     return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')



class HomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id','posts_image',"created",)
        # read_only_fields = ('created_at',)




class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('is_login',)
        # read_only_fields = ('created_at',)

class EmailRertieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email','password','nickname',)
        # read_only_fields = ('created_at',)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id' ,'posts_image', 'latitude', 'longitude',)
        # read_only_fields = ('created_at',)


class PostAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('__all__')
        # read_only_fields = ('created_at',)


class PostsContentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('contents',)
        # read_only_fields = ('created_at',)
##############################################

class UserProfile(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','user_uid','nickname','profile_image',)

class HashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTag
        fields = ('__all__')

class PostDetailSerializer(serializers.ModelSerializer):
    user = UserProfile(read_only=True)
    # hashtag = HashTagSerializer(read_only=True,many=True)
    class Meta:
        model = Post
        # fields = ('user',)
        exclude = ('modify_date','delete_date','is_active','problem','report_date','report')
#################################################



##############################################


class MyUserSerializer(serializers.ModelSerializer):
    # user = UserProfile(read_only=True)
    class Meta:
        model = User
        # fields=('__all__')
        fields = ('nickname','profile_image',)
        # exclude = ('modify_date','delete_date','is_active','problem','report_date','report')

class MypageSerializer(serializers.ModelSerializer):
    # user = UserProfile(read_only=True)
    class Meta:
        model = Post
        # fields=('__all__')
        fields = ('id','posts_image','latitude','longitude',)
        # exclude = ('modify_date','delete_date','is_active','problem','report_date','report')
#################################################




class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ('__all__')
        # read_only_fields = ('created_at',)



class ScrapPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id','posts_image','back_image')
        # read_only_fields = ('created_at',)

class ScrapAllSerializer(serializers.ModelSerializer):
    hashtag = ScrapPostSerializer(read_only=True,many=True)
    class Meta:
        model = Post
        fields = ('__all__')
        # exclude = ('__all__')


class ScrapSerializer(serializers.ModelSerializer):
    post = ScrapPostSerializer(read_only=True)
    class Meta:
        model = Scrapt
        fields = ('post',)
#################################################


class MyUserCommentSerializer(serializers.ModelSerializer):
    # user = UserProfile(read_only=True)
    class Meta:
        model = User
        # fields=('__all__')
        fields = ('id','nickname','profile_image','user_uid')
        # exclude = ('modify_date','delete_date','is_active','problem','report_date','report')


class CommentSerializer(serializers.ModelSerializer):
    user = MyUserCommentSerializer(read_only=True)
    class Meta:
        model = Comment
        # fields = ('__all__')
        exclude = ('is_active','delete_date','post','modify_date')



class SearchNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ('__all__')
        fields = ('nickname',)


class SearchTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTag
        # fields = ('__all__')
        fields = ('tag_name',)


class TagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTag
        # fields = ('__all__')
        fields = ('post_id',)
