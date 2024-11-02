from datetime import timedelta, timezone, datetime
from typing import Annotated, Optional
import jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Response, HTTPException, status, Depends, Request

from src.secrets.secrets import get_secret
from src.config.config import get_config
from src.db.db import MongoDB

ALGORITHM = 'HS256'
TOKEN_EXPIRATION = timedelta(seconds=get_config().security_config.token_expires_delta)
CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'}
)


class OAuth2PasswordBearerWithCookie(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        token = request.cookies.get("access_token")
        if not token:
            try:
                return await super().__call__(request)
            except HTTPException:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated"
                )
        return token


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl='token')
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = TOKEN_EXPIRATION):
    secret_key = get_secret('SECRET_KEY')

    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt


async def authenticate_user(email: str, password: str):
    cursor = MongoDB()
    user = await cursor.collection.find_one({'email': email})
    if not user:
        return False
    if not verify_password(password, user['password']):
        return False
    return user


def set_auth_cookies(response: Response, token: str):
    response.set_cookie(
        key='access_token',
        value=token,
        httponly=True,
        # secure=True, # TODO: enable this when using HTTPS
        samesite='lax',
        max_age=int(TOKEN_EXPIRATION.total_seconds()),
        path='/'
    )


def remove_auth_cookies(response: Response):
    response.delete_cookie(
        key='access_token',
        path='/'
    )


async def register_user(email: str, password: str):
    cursor = MongoDB()
    user = await cursor.collection.find_one({'email': email})
    if user:
        return False
    hashed_password = get_password_hash(password)
    cursor.collection.insert_one({'email': email, 'password': hashed_password})
    return True


def get_email(token: Annotated[str, Depends(oauth2_scheme)]):
    secret_key = get_secret('SECRET_KEY')

    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        email = payload.get('sub')
        if not email:
            raise CREDENTIALS_EXCEPTION
        return email
    except jwt.InvalidTokenError:
        raise CREDENTIALS_EXCEPTION


async def get_username(email: Annotated[str, Depends(get_email)]):
    cursor = MongoDB()
    user = await cursor.collection.find_one({'email': email})
    return user.get('username')
