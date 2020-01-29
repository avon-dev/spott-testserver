"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token #JWT 인증을 위해 필요한 요소를 불러온다
from rest_framework_simplejwt import views as jwt_views
from django.conf import settings
# from rest_framework_simplejwt.views import (
#     TokenObtainSlidingView,
#     TokenRefreshSlidingView,
# )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('spott/token', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('spott/token/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('spott/token/verify', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
    # path('api/token/', TokenObtainSlidingView.as_view(), name='token_obtain'),
    # path('api/token/refresh/', TokenRefreshSlidingView.as_view(), name='token_refresh'),
    path('spott/', include('testapp.urls'))
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
