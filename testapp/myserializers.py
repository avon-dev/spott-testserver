from rest_framework import serializers
from .models import *

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')
        # extra_kwargs = {"password": {"write_only": True}}

        # def create(self, validated_data):
        #     user = User(email=validated_data['email'],nickname=validated_data['nickname'])
        #     user.set_password(validated_data['password'])
        #     user.save()
        #     return user

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
