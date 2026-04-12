import boto3
from urllib.parse import urlparse

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

    def get_presigned_image_url(self, object_url_or_key: str, expires_in: int = 3600) -> str:
        key = self._extract_key(object_url_or_key)
        return self.s3_client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": self.bucket_name, "Key": key},
            ExpiresIn=expires_in,
        )

    def _extract_key(self, object_url_or_key: str) -> str:
        if not object_url_or_key:
            return ""

        s3_prefix = f"https://{self.bucket_name}.s3.amazonaws.com/"
        if object_url_or_key.startswith(s3_prefix):
            return object_url_or_key[len(s3_prefix):]

        parsed = urlparse(object_url_or_key)
        if parsed.scheme and parsed.netloc:
            return parsed.path.lstrip("/")

        return object_url_or_key.lstrip("/")


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
