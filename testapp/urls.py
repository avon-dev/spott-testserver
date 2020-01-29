from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers

# router = DefaultRouter()
# router.register('user', views.UserCreate)



urlpatterns = [
    path('login', views.Login.as_view(), name='user'),
    # path('', include(router.urls)),
    path('user', views.UserCreate.as_view()),
    path('email-authen', views.EmailAuthentication.as_view()),
    path('posts', views.Posts.as_view()),
    path('test', views.Test.as_view()),
    path('test2', views.Test.as_view()),
    # path('auto', views.AutoCreate.as_view()),
]
# urlpatterns = format_suffix_patterns(urlpatterns)
