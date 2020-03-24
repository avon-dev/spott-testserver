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
from testapp.assemble_view import notice_views
from testapp.assemble_view import html_views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
# from testapp.assemble_view.map_views import *

router = DefaultRouter(trailing_slash=False)#라우터 마지막에 / 제거

router.register('posts', posts_views.PostViewSet, basename='posts')
router.register('posts-recommendation', posts_views.PhopoRecommendationViewSet, basename='recommendation')
router.register('recent', search_views.RecentSearchView, basename='recent')
# router.register('comments', comment_views.CommentViewSet, basename='comments')

urlpatterns = [
    path('email-auth', account_views.EmailAuthentication.as_view()), #이메일 인증

    #이메일 인증
    path('account', account_views.AccountView.as_view()), #account로 바꾸기

    #이메일 인증
    path('social-account', account_views.SocialAccountView.as_view()), #account로 바꾸기

    #댓글
    path('posts/<int:post_pk>/comment', comment_views.CommentListView.as_view()),
    path('posts/<int:post_pk>/comment/<int:pk>', comment_views.CommentView.as_view()),

    #유저 마이페이지
    path('users/<int:pk>/posts', mypage_views.UserMypageViewSet.as_view()),

    #마이페이지 (이쪽 부분이 url이 약간 애매하다)
    path('users/my-posts', mypage_views.MypageViewSet.as_view()),

    #알림
    path('notice', notice_views.NoticeView.as_view()),
    path('notice/<int:pk>', notice_views.NoticeDetailView.as_view()),

    #게시글 좋아요
    path('posts/<int:pk>/likes', posts_like_views.Like.as_view()),

    #게시글 스크랩
    path('posts/<int:pk>/scrap', scrap_views.Scrap.as_view()),

    #유저 스크랩 화면
    path('users/my-scrap', scrap_views.MultiScrap.as_view()),

    path('', include(router.urls)),

    # path('home/posts', home_views.Home.as_view()),


    path('guide', html_views.guide, name='guide'),
    path('guide-en', html_views.guideEn, name='guide-en'),
    path('guide-cn', html_views.guideCn, name='guide-cn'),
    path('personal-Information-processing-policy', html_views.personalInformationProcessingPolicy, name='personalInformationProcessingPolicy'),
    path('location-based-service-terms-and-conditions', html_views.locationBasedServiceTermsAndConditions, name='locationBasedServiceTermsAndConditions'), ##위치정보
    path('terms-and-conditions', html_views.termsAndConditions, name='termsAndConditions'), ##이용약관
    path('first-notice', html_views.firstNotice, name='firstNotice'),
    path('app-notices', html_views.AppNoticesView.as_view(), name='AppNotices'),
    path('open-source', html_views.openSource, name='openSource'),

    path('publickey', account_views.PublicKeyView.as_view(), name='public'),
    path('tag', tag_views.HashTagView.as_view(), name='tag'),
    path('users', user_views.UserView.as_view()),
    path('users/password', user_views.PasswordView.as_view()),
    path('test', test_views.Test.as_view()),
    path('test2', test_views.Test2.as_view()),
    path('home/token', home_views.aaa.as_view()),
    path('search', search_views.SearchView.as_view()),
    path('report', report_views.ReportView.as_view()),





    # path('map/posts', map_views.Posts.as_view()), #post에서 분기처리
]
# urlpatterns = format_suffix_patterns(urlpatterns)
