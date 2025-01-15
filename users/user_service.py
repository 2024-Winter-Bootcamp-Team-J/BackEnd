from django.contrib.auth import authenticate
from django.conf import settings
from utils.s3_utils import upload_to_s3
from .models import User


def register_user(email, password, nickname, profile_img_file=None):
    """
    회원가입 서비스
    """
    if User.objects.filter(email=email).exists():
        raise ValueError("이미 등록된 이메일입니다.")

    if profile_img_file:
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        file_name = f"profiles/{nickname}.jpg"
        profile_img_url = upload_to_s3(profile_img_file, bucket_name, file_name)
    else:
        profile_img_url = None

    user = User.objects.create_user(
        email=email, password=password, nickname=nickname, profile_img=profile_img_url
    )
    return user


def login_user(email, password):
    """
    로그인 서비스
    """
    user = User.objects.filter(email=email).first()
    if user is not None and user.check_password(password):  # 비밀번호 확인
        return user
    raise ValueError("잘못된 이메일 또는 비밀번호입니다.")