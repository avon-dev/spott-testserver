from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import exceptions, serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.state import User

# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#
#         # Add custom claims
#         token['name'] = user.name
#         # ...
#
#         return token
#
# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer



# class PasswordField(serializers.CharField):
#     def __init__(self, *args, **kwargs):
#         kwargs.setdefault('style', {})
#
#         kwargs['style']['input_type'] = 'password'
#         kwargs['write_only'] = True
#
#         super().__init__(*args, **kwargs)
#
#
# class MyTokenObtainSerializer(serializers.Serializer):
#     username_field = User.USEREMAIL_FIELD
#
#     default_error_messages = {
#         'no_active_account': _('No active account found with the given credentials')
#     }
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         self.fields[self.username_field] = serializers.CharField()
#         self.fields['password'] = PasswordField()
#
#     def validate(self, attrs):
#         authenticate_kwargs = {
#             self.username_field: attrs[self.username_field],
#             'password': attrs['password'],
#         }
#         try:
#             authenticate_kwargs['request'] = self.context['request']
#         except KeyError:
#             pass
#
#         self.user = authenticate(**authenticate_kwargs)
#
#         # Prior to Django 1.10, inactive users could be authenticated with the
#         # default `ModelBackend`.  As of Django 1.10, the `ModelBackend`
#         # prevents inactive users from authenticating.  App designers can still
#         # allow inactive users to authenticate by opting for the new
#         # `AllowAllUsersModelBackend`.  However, we explicitly prevent inactive
#         # users from authenticating to enforce a reasonable policy and provide
#         # sensible backwards compatibility with older Django versions.
#         if self.user is None or not self.user.is_active:
#             raise exceptions.AuthenticationFailed(
#                 self.error_messages['no_active_account'],
#                 'no_active_account',
#             )
#
#         return {}
#
#
# class MyTokenObtainPairSerializer(MyTokenObtainSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#
#
# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer
#
#
#
# from testapp.assemble_view.__init__ import *
#
#
# from rest_framework import generics, status
#
# from rest_framework_simplejwt.authentication import AUTH_HEADER_TYPES
# from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
#
#
# class asdasd(generics.GenericAPIView):
#     permission_classes = ()
#     authentication_classes = ()
#
#     serializer_class = MyTokenObtainPairSerializer
#
#     www_authenticate_realm = 'api'
#
#     def get_authenticate_header(self, request):
#         return '{0} realm="{1}"'.format(
#             AUTH_HEADER_TYPES[0],
#             self.www_authenticate_realm,
#         )
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#
#         # try:
#         #     serializer.is_valid(raise_exception=True)
#         # except TokenError as e:
#         #     raise InvalidToken(e.args[0])
#
#         return Response(str(serializer.is_valid), status=status.HTTP_200_OK)



class PasswordField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('style', {})

        kwargs['style']['input_type'] = 'password'
        kwargs['write_only'] = True

        super().__init__(*args, **kwargs)


class MyTokenObtainSerializer(serializers.Serializer):
    username_field = User.USERNAME_FIELD

    default_error_messages = {
        'no_active_account': _('No active account found with the given credentials')
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = PasswordField()

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'password': attrs['password'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        # Prior to Django 1.10, inactive users could be authenticated with the
        # default `ModelBackend`.  As of Django 1.10, the `ModelBackend`
        # prevents inactive users from authenticating.  App designers can still
        # allow inactive users to authenticate by opting for the new
        # `AllowAllUsersModelBackend`.  However, we explicitly prevent inactive
        # users from authenticating to enforce a reasonable policy and provide
        # sensible backwards compatibility with older Django versions.
        if self.user is None or not self.user.is_active:
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )

        return {}

    @classmethod
    def get_token(cls, user):
        raise NotImplementedError('Must implement `get_token` method for `TokenObtainSerializer` subclasses')


class MyTokenObtainPairSerializer(MyTokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data





from rest_framework import generics, status
from rest_framework.response import Response


from rest_framework_simplejwt.authentication import AUTH_HEADER_TYPES
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


class TokenViewBase(generics.GenericAPIView):
    permission_classes = ()
    authentication_classes = ()

    serializer_class = MyTokenObtainPairSerializer

    www_authenticate_realm = 'api'

    def get_authenticate_header(self, request):
        return '{0} realm="{1}"'.format(
            AUTH_HEADER_TYPES[0],
            self.www_authenticate_realm,
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(str(serializer), status=status.HTTP_200_OK)


class TokenObtainPairView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = MyTokenObtainPairSerializer


# token_obtain_pair = TokenObtainPairView.as_view()
