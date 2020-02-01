from testapp.assemble_model.__init__ import *
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.mail import send_mail
from testapp.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin): #나중에 널 값 처리
    user_uid = models.CharField(max_length=255, unique = True) #이메일 해싱
    email = models.EmailField(_('email address'))
    password = models.CharField(_('password'), max_length=200)
    nickname = models.CharField(max_length=150)
    profile_image = models.ImageField(max_length=150, default="basic_image")
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True) #생성날짜
    is_active = models.BooleanField(_('active'), default=True) #아이디 활성화 상태인지(삭제여부)
    is_login = models.BooleanField(default = False) #로그인 여부
    modify_date = models.DateTimeField()
    delete_date = models.DateTimeField()
    is_staff = models.BooleanField(_('is staff'), default = False)

    objects = UserManager()

    USERNAME_FIELD = 'user_uid'
    REQUIRED_FIELDS = ['nickname']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        return self.email

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.nickname

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
