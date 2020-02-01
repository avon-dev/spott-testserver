from testapp.assemble_view import map_views
from testapp.assemble_view import account_views
from testapp.assemble_view import test_views
from testapp.assemble_view import home_views
from testapp.assemble_view import posts_views
from testapp.assemble_view import comment_views
from testapp.assemble_view import mypage_views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
# from testapp.assemble_view.map_views import *
router = DefaultRouter(trailing_slash=False)
router.register('posts', posts_views.PostViewSet, basename='posts')
router.register('comments', comment_views.CommentViewSet, basename='comments')

urlpatterns = [
    path('login', account_views.Login.as_view(), name='user'),
    path('', include(router.urls)),
    path('mypage', mypage_views.MypageViewSet.as_view()),
    path('user', account_views.UserCreate.as_view()),
    path('email-authen', account_views.EmailAuthentication.as_view()),
    path('map/posts', map_views.Posts.as_view()),
    path('home/posts', home_views.Home.as_view()),
    path('test', test_views.Test.as_view()),
    path('test2', test_views.Test2.as_view()),
    # path('auto', views.AutoCreate.as_view()),
]
# urlpatterns = format_suffix_patterns(urlpatterns)
