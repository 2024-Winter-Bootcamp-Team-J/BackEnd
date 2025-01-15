from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import PermissionsMixin


# 사용자 관리자 클래스
class UserManager(BaseUserManager):

    def create_user(self, email, password=None, nickname=None, **extra_fields):
        """
                   일반 사용자 생성 메소드
        """
        if not email:
            raise ValueError('The Email field must be set')
        if not nickname:
            raise ValueError('The Nickname field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, nickname=nickname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # 관리자 생성 메소드
    def create_superuser(self, email, password=None, nickname=None, **extra_fields):
        """
                슈퍼유저 생성 메소드
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, nickname, **extra_fields)


# 사용자 모델
class User(AbstractBaseUser, PermissionsMixin):
    """
        커스텀 유저 모델
    """
    user_id = models.BigAutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    nickname = models.CharField(max_length=50)

    profile_img = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    #식별 필드 pk?
    USERNAME_FIELD = 'user_id'
    #사용자 생성(슈퍼 유저) 시 필수로 요구되는 추가 필드
    REQUIRED_FIELDS = ['email', 'nickname']

    def __str__(self):
        return self.nickname