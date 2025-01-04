from pydantic import BaseModel
from functools import lru_cache
import yaml


class ServerConfig(BaseModel):
    host: str
    port: int


class MongoConfig(BaseModel):
    host: str
    port: int
    username: str
    password: str
    db: str
    collection_name: str


class SecurityConfig(BaseModel):
    token_expires_delta: int


class ValidationConfig(BaseModel):
    max_email_length: int
    max_name_length: int
    max_description_length: int


class S3Config(BaseModel):
    hostname: str
    bucket_name: str
    access_key: str
    secret_key: str


class AppConfig(BaseModel):
    name: str
    version: str
    debug: bool = False
    server_config: ServerConfig
    mongo_config: MongoConfig
    security_config: SecurityConfig
    validation_config: ValidationConfig
    s3_config: S3Config
    categories: list[str]


@lru_cache()
def get_config(config_path: str = "config/default.yaml") -> AppConfig:
    with open(config_path, "r") as f:
        config_data = yaml.safe_load(f)
    return AppConfig(**config_data)
