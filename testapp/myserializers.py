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



##############################################

class UserProfile(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('nickname','profile_image',)

class HashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTag
        fields = ('tag_name',)

class PostDetailSerializer(serializers.ModelSerializer):
    user = UserProfile(read_only=True)
    hashtag = HashTagSerializer(read_only=True,many=True)
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
