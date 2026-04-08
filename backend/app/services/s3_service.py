import boto3

from app.core.config import settings


class S3Service:
    def __init__(self, s3_client, bucket_name: str):
        self.s3_client = s3_client
        self.bucket_name = bucket_name

    def upload_file(self, file_stream, filename: str, content_type: str) -> str:
        self.s3_client.upload_fileobj(
            file_stream,
            self.bucket_name,
            filename,
            ExtraArgs={"ContentType": content_type},
        )
        return f"https://{self.bucket_name}.s3.amazonaws.com/{filename}"


def _create_s3_client():
    return boto3.client(
        "s3",
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID.get_secret_value(),
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY.get_secret_value(),
    )


s3_service = S3Service(
    s3_client=_create_s3_client(),
    bucket_name=settings.AWS_S3_BUCKET,
)

