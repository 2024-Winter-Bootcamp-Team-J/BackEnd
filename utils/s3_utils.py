import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from django.conf import settings


def upload_to_s3(file, bucket_name, file_name, acl="public-read"):
    """
    S3에 파일 업로드
    """
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )
    try:
        s3.upload_fileobj(file, bucket_name, file_name)
        s3_url = f"https://{bucket_name}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{file_name}"
        print(type(s3_url))
        return s3_url
    except NoCredentialsError:
        raise ValueError("AWS credentials not available")
    except ClientError as e:
        raise ValueError(f"Failed to upload to S3: {e}")