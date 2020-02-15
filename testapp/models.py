# from testapp.assemble_model.user_model import *
# from testapp.assembel_model.hashtag_model import *
# from testapp.assembel_model.post_model import *
# from testapp.assembel_model.comment_model import *
# from testapp.assembel_model.postlike_model import *
# from testapp.assembel_model.scrap_model import *












from django.db import models
from django.utils.translation import ugettext_lazy as _
from pytz import timezone
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.mail import send_mail
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin): #나중에 널 값 처리
    user_uid = models.CharField(max_length=255, unique = True) #이메일 해싱
    email = models.EmailField(_('email address'))
    password = models.CharField(_('password'), max_length=200)
    nickname = models.CharField(max_length=150)
    profile_image = models.ImageField(upload_to = 'usr', null = True, blank = True)
    joined_date = models.DateTimeField(_('date joined'), auto_now_add=True) #생성날짜
    is_active = models.BooleanField(_('active'), default=True) #아이디 활성화 상태인지(삭제여부)  판별
    is_login = models.BooleanField(default = False) #로그인 여부
    modify_date = models.DateTimeField(null = True, blank = True)
    is_staff = models.BooleanField(_('is staff'), default = False)
    objects = UserManager()
    USEREMAIL_FIELD = 'email'
    USERNAME_FIELD = 'user_uid'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        return self.user_uid

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All superusers are staff
        return self.is_superuser

    def created_at_korean_time(self):
        korean_timezone = timezone(settings.TIME_ZONE)
        return self.created_at.astimezone(korean_timezone)

# 스크랩을 취소 한다는건 해당 스크랩 테이블에서 레코드가 지워진다는 것을 뜻함
# 게시물이 지워졌을 때 연결 돼 있는 해당 스크랩까지 지워지도록 구현
# 스크랩 날짜를 구해야 될까??? 딱히??? 안 구해도 될거 같다.
# class Hashtag(models.Model): #! !댓글, !작성일, !수정일, !삭제일, !삭제여부
#     name = models.CharField(max_length = 255)
#
#
#     def __str__(self):
#         return self.name



class Post(models.Model): #!내용(conents), !작성일, !수정일, !공개여부(public),
                            # !게시물 신고 여부, !신고 날짜, 부적절 게시물 여부(problem), !삭제여부, !삭제 날짜
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name= 'get_user') #get_post로 변경
    posts_image = models.ImageField(upload_to = 'post') #R
    back_image = models.ImageField(upload_to = 'postb') #R
    latitude = models.FloatField() #R
    longitude = models.FloatField() #R
    contents = models.TextField(verbose_name = '내용') #내용
    views = models.IntegerField(default = 0)
    created = models.DateTimeField(auto_now_add=True) #작성일
    modify_date = models.DateTimeField(null = True, blank = True) #게시글 수정일
    public = models.BooleanField(default = True) #공개여부
    report = models.BooleanField(default = False) #신고여부
    report_date = models.DateTimeField(null = True, blank = True) #신고 날짜
    problem = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    hashtag = models.ManyToManyField('User', through='HashTag',related_name='get_hashtag')
    like_user = models.ManyToManyField('User', through = 'PostLike',related_name= 'get_like')
    comment = models.ManyToManyField('User', through='Comment',related_name='get_comment')
    scrap_users = models.ManyToManyField('User', through = 'Scrapt',related_name= 'get_scrap')
    #좋아요가 1000개 이상 넘어가면 카운트로 조회
    def __str__(self):
        return str(self.id)

# class UserData(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE,related_name= 'user_data')
#     scrap_users = models.ManyToManyField('Post', through = 'Scrap',related_name= 'get_scrap')
#     objects = UserManager()


class HashTag(models.Model): #! !댓글, !작성일, !수정일, !삭제일, !삭제여부
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name= 'user_hashtag')
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name= 'post_hashtag')
    tag_name = models.CharField(max_length=250,verbose_name = '태그명') #태그
    count = models.IntegerField(default = 0)
    is_tag = models.BooleanField(default = True)
    created = models.DateTimeField(auto_now_add=True) #작성일

    def __str__(self):
        return self.tag_name



class HashTag(models.Model): #! !댓글, !작성일, !수정일, !삭제일, !삭제여부
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name= 'user_hashtag')
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name= 'post_hashtag')
    tag_name = models.CharField(max_length=250,verbose_name = '태그명') #태그
    is_tag = models.BooleanField(default = True)
    created = models.DateTimeField(auto_now_add=True) #작성일

    def __str__(self):
        return self.tag_name


class Comment(models.Model): #! !댓글, !작성일, !수정일, !삭제일, !삭제여부
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'user_comment')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name= 'post_comment')
    contents = models.TextField(verbose_name = '내용') #내용
    created = models.DateTimeField(auto_now_add=True) #작성일
    modify_date = models.DateTimeField(null = True, blank = True) #댓글 수정일
    is_active = models.BooleanField(default = True)


    def __str__(self):
        return self.contents


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name= 'post_like')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'user_like')
    created_date = models.DateTimeField(auto_now_add=True,)

    def __str__(self):
        return str(self.post.id)


class Scrapt(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name= 'post_scrap')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'user_scrap')
    created_date = models.DateTimeField(auto_now_add=True,)


    class Meta:
        ordering = ('-created_date',)

    # def __str__(self):
    #     return self.user
