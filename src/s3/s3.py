import asyncio
import io
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from typing import Any, Coroutine

import minio.error
from minio import Minio

from src.config.config import get_config


class S3:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(S3, cls).__new__(cls)

            s3_config = get_config().s3_config

            cls._instance.client = Minio(
                s3_config.hostname,
                access_key=s3_config.access_key,
                secret_key=s3_config.secret_key,
                secure=False  # TODO: change to True when using https
            )
            cls._instance.bucket_name = s3_config.bucket_name
            cls._instance.executor = ThreadPoolExecutor()

            if not cls._instance.client.bucket_exists(cls._instance.bucket_name):
                cls._instance.client.make_bucket(cls._instance.bucket_name)

        return cls._instance

    async def send_object(self, object_name: str, data: bytes, content_type: str = 'application/octet-stream'):
        def _upload():
            self.client.put_object(
                self.bucket_name,
                object_name,
                io.BytesIO(data),
                len(data),
                content_type=content_type
            )
            return True

        return await asyncio.get_event_loop().run_in_executor(self.executor, _upload)

    async def get_object(self, object_name: str) -> BytesIO | None:
        def _download():
            response = self.client.get_object(self.bucket_name, object_name)
            img_data = io.BytesIO(response.read())
            response.close()
            response.release_conn()

            return img_data

        try:
            return await asyncio.get_event_loop().run_in_executor(self.executor, _download)
        except minio.error.S3Error:
            return None

    async def delete_object(self, object_name: str):
        def _delete():
            self.client.remove_object(self.bucket_name, object_name)
            return True

        return await asyncio.get_event_loop().run_in_executor(self.executor, _delete)


def get_s3() -> S3:
    return S3()
