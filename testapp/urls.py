from testapp.assemble_view import map_views
from testapp.assemble_view import account_views
from testapp.assemble_view import test_views
from testapp.assemble_view import home_views
from testapp.assemble_view import posts_views
from testapp.assemble_view import comment_views
from testapp.assemble_view import mypage_views
from testapp.assemble_view import posts_like_views
from testapp.assemble_view import scrap_views
from testapp.assemble_view import comment_views
from testapp.assemble_view import user_views
from testapp.assemble_view import tag_views
from testapp.assemble_view import search_views
from testapp.assemble_view import report_views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
# from testapp.assemble_view.map_views import *

router = DefaultRouter(trailing_slash=False)#라우터 마지막에 / 제거

router.register('posts', posts_views.PostViewSet, basename='posts')
router.register('recent', search_views.RecentSearchView, basename='recent')
# router.register('comments', comment_views.CommentViewSet, basename='comments')

urlpatterns = [
    path('email-authen', account_views.EmailAuthentication.as_view()), #이메일 인증
    path('account', account_views.AccountView.as_view()), #account로 바꾸기

    path('', include(router.urls)),

    # path('home/posts', home_views.Home.as_view()),

    path('login', account_views.Login.as_view(), name='user'),
    path('tag', tag_views.HashTagView.as_view(), name='tag'),
    path('mypage', mypage_views.MypageViewSet.as_view()),
    path('mypage/<int:pk>', mypage_views.UserMypageViewSet.as_view()),
    path('users', user_views.UserView.as_view()),
    path('users/password', user_views.PasswordView.as_view()),
    path('map/posts', map_views.Posts.as_view()), #post에서 분기처리
    path('like/<int:pk>', posts_like_views.Like.as_view()),
    path('scrap/<int:pk>', scrap_views.Scrap.as_view()),
    path('scrap/ids', scrap_views.MultiScrap.as_view()),
    path('test', test_views.Test.as_view()),
    path('test2', test_views.Test2.as_view()),
    path('home/token', home_views.aaa.as_view()),
    path('posts/<int:post_pk>/comment', comment_views.CommentListView.as_view()),
    path('posts/<int:post_pk>/comment/<int:pk>', comment_views.CommentView.as_view()),
    path('search', search_views.SearchView.as_view()),
    path('report', report_views.ReportView.as_view()),
]
# urlpatterns = format_suffix_patterns(urlpatterns)
