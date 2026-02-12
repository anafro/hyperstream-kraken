from datetime import timedelta

import boto3
from botocore.exceptions import ClientError
from mypy_boto3_s3 import S3Client
from mypy_boto3_s3.type_defs import CreateBucketConfigurationTypeDef

from hyperstreamkraken.utils.s3 import get_error_code


class SongFilesStorage:
    s3: S3Client
    bucket: str

    def __init__(
        self,
        s3_host: str,
        access_key: str,
        secret_key: str,
        bucket: str,
        region: str,
    ) -> None:
        self.bucket = bucket
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            endpoint_url=s3_host,
            region_name=region,
        )

        try:
            _ = self.s3.head_bucket(Bucket=bucket)
        except ClientError as e:
            if get_error_code(e) in ("404", "NoSuchBucket"):
                if region == "us-east-1":
                    _ = self.s3.create_bucket(Bucket=bucket)
                else:
                    configuration: CreateBucketConfigurationTypeDef = {
                        "LocationConstraint": region
                    }
                    _ = self.s3.create_bucket(
                        Bucket=bucket,
                        CreateBucketConfiguration=configuration,
                    )
            else:
                raise

    def exists(self, song_id: str) -> bool:
        try:
            _ = self.s3.head_object(Bucket=self.bucket, Key=song_id)
            return True
        except ClientError as e:
            if get_error_code(e) == "404":
                return False
            raise

    def upload(self, song_id: str, song_bytes: bytes) -> None:
        if self.exists(song_id):
            return

        _ = self.s3.put_object(
            Body=song_bytes, Bucket=self.bucket, Key=song_id, ContentType="audio/mpeg"
        )

    def presign_s3_url(self, song_id: str, expires_in: timedelta | None = None) -> str:
        if expires_in is None:
            expires_in = timedelta(minutes=30)

        expires_in_millis: int = int(expires_in.total_seconds() * 1000)
        return self.s3.generate_presigned_url(
            "get_object",
            Params={"Key": song_id, "Bucket": self.bucket},
            ExpiresIn=expires_in_millis,
        )
